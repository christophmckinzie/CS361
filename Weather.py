import numpy as np
import pandas as pd
import re
import urllib.request
import json
# import gmaps # for embedding googlemap in jupyter nb
from geopy import geocoders
import googlemaps
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import polyline
import folium
# from IPython.display import display
from folium import IFrame
import webbrowser
import math
import io
import datetime


class WeatherMapping:
    def __init__(self, start_address, end_address, weather_type, travel_date=datetime.date.today().strftime("%Y-%m-%d"), num_of_checks=5):
        # initialize endpoints and api keys
        self.endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        self.gmaps_key = 'AIzaSyDgnzt-edsvazLF4S7XWOMcK78PAOy2i_g'
        self.googlemaps = googlemaps.Client(self.gmaps_key)
        self.owm_key = "54df9da64ee34a820bf3312390615de6"

        self.start_address = start_address.replace(' ', '+')
        self.end_address = end_address.replace(' ', '+')
        self.weather_type = weather_type
        self.date_of_travel = travel_date
        self.num_of_checks = num_of_checks

        self.nav_request = None
        self.request = None
        self.response = None
        self.directions = None
        self.route_gps_coords = None
        self.steps_in_route = None
        self.possible_marker_locations = None
        self.map = None
        self.weather_at_checkpoint = None
        self.popup_info = None
        self.gps_coords = None
        self.Row_list = None

    def get_route_coords(self):
        """
        makes request to google directions api and creates a pandas dataframe to hold lat/lon pairs of route
        """

        # make request and get response
        self.nav_request = f"""origin={self.start_address}&destination={self.end_address}&key={self.gmaps_key}"""
        self.request = self.endpoint + self.nav_request
        self.response = urllib.request.urlopen(self.request).read()
        self.directions = json.loads(self.response)

        # create empty dataframe. lat = 0, lng = 1
        self.route_gps_coords = pd.DataFrame(columns=[0, 1])

        # determine number of steps in route
        self.steps_in_route = len(
            self.directions['routes'][0]['legs'][0]['steps'])

        # put gps coords and add to dataframe
        for i in range(self.steps_in_route):
            self.route_gps_coords = pd.concat([self.route_gps_coords,
                                               pd.DataFrame(polyline.decode((self.directions['routes'][0]['legs'][0]['steps'][i]['polyline']['points'])))])

        # reset index
        self.route_gps_coords = self.route_gps_coords.reset_index(drop=True)

        return (self.route_gps_coords)

    def extract_weather(self, weather_response):
        """
        input weather response from openweathermap's api
        date_of_travel is a string of the travel date yyyy-mm-dd
        output is dataframe temp, weather description, city id and date as index
        """

        # create empty dataframe. lat = 0, lng = 1
        self.weather_at_checkpoint = pd.DataFrame(
            columns=['date', 'temp', 'description', 'city_id'])

        len_of_forecast = len(weather_response['list'])

        city_id = int(weather_response['city']['id'])

        # extract gps coords and add to dataframe
        for i in range(len_of_forecast):
            # get description
            description = weather_response['list'][i]['weather'][0]['main']

            # get datetime
            date = weather_response['list'][i]['dt_txt']

            # get temp
            temp = weather_response['list'][i]['main']['temp']
            temp = (temp - 273.15) * 9/5 + 32

            # make list
            row_i = pd.DataFrame([[date, temp, description, city_id]], columns=[
                                 'date', 'temp', 'description', 'city_id'])

            # append to dataframe
            self.weather_at_checkpoint = pd.concat(
                [self.weather_at_checkpoint, row_i])

            # reset index
            self.weatheweather_at_checkpointr_df = self.weather_at_checkpoint.reset_index(
                drop=True)
            self.weather_at_checkpoint['city_id'] = self.weather_at_checkpoint['city_id']

        self.weather_at_checkpoint.set_index(pd.to_datetime(
            self.weather_at_checkpoint['date'].values), inplace=True)
        self.weather_at_checkpoint.drop('date', axis=1, inplace=True)
        self.weather_at_checkpoint = self.weather_at_checkpoint.loc[self.date_of_travel]

        return (self.weather_at_checkpoint)

    def get_all_weather(self):
        """
        Docstring
        """
        self.gps_coords = self.get_route_coords()

        self.Row_list = []

        # Iterate over each row
        for rows in self.gps_coords.itertuples():
            # Create list for the current row
            my_list = [rows[1], rows[2]]

            # append the list to the final list
            self.Row_list.append(my_list)

        self.possible_marker_locations = []

        for i in range(1, len(self.gps_coords),  math.floor(len(self.gps_coords)/self.num_of_checks)):
            self.possible_marker_locations.append({'name': '{}'.format(i),
                                                   'location': (self.gps_coords.iloc[i].values[0], self.gps_coords.iloc[i].values[1])})

        self.all_checkpoints_weather = []

        for i in range(self.num_of_checks):
            owm_request = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'.format(
                self.possible_marker_locations[i]['location'][0], self.possible_marker_locations[i]['location'][1], self.owm_key)

            owm_response = urllib.request.urlopen(owm_request).read()
            weather_response = json.loads(owm_response)

            self.all_checkpoints_weather.append(
                self.extract_weather(weather_response))

        return (self.all_checkpoints_weather)

    def popup_locations(self):
        # format for inserting into folium popup: '<a href=" [URL LINK HERE] "target="_blank"> [TEXT GOES HERE]' </a>'

        self.get_all_weather()
        self.popup_info = []

        for i in range(len(self.all_checkpoints_weather)):
            # if self.all_checkpoints_weather[i]['description'].str.contains(self.weather_type).any():
            if (self.all_checkpoints_weather[i]['description'] == self.weather_type).any():
                # The above code is the original code. i tried removing the .str
                popup_location = self.possible_marker_locations[i]['location']
                popup_city_id = self.all_checkpoints_weather[i]['city_id'][0]
                url = 'https://openweathermap.org/city/{}'.format(
                    self.all_checkpoints_weather[i]['city_id'][0])
                weblink = '<a href=" {} "target="_blank"> {} {}'.format(
                    url, 'Link to weather 5 day forecast', '</a>')
                self.popup_info.append(
                    [popup_location, popup_city_id, weblink])

        return (self.popup_info)

    def create_map(self):

        # popup_locations function collects weather from all checkpoints and returns information for producing popup on map
        self.popup_locations()

        # center map at center of route
        self.map = folium.Map(location=self.Row_list[round(
            len(self.route_gps_coords)/2)], zoom_start=8)

        # starting marker
        folium.Marker(self.Row_list[0], popup='Origin').add_to(self.map)

        # ending marker
        folium.Marker(self.Row_list[-1],
                      popup='Destination').add_to(self.map)

        # add marker for weather location
        for i in range(len(self.popup_info)):
            iframe = folium.IFrame(
                html=self.popup_info[i][2], width=200, height=75)
            popup = folium.Popup(iframe, max_width=2650)

            folium.Marker(self.popup_info[i][0],
                          popup=popup).add_to(self.map)

        folium.PolyLine(locations=self.Row_list,
                        line_opacity=0.5).add_to(self.map)

        return self.map


def weather_map(origin, destination, weather_type, travel_date, num_of_checks):
    # create WeatherMapping object
    w = WeatherMapping(origin, destination, weather_type,
                       travel_date, num_of_checks)

    map = w.create_map()

    # save map data
    map.save('map.html', close_file=False)

    # get map data
    webbrowser.open('map.html')


WeatherMapping.produce_map(
    "Seattle, WA", "Moses Lake, WA", "Snow", "2/6/2023", 10)
