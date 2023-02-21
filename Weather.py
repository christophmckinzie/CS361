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
import math
import config


class WeatherMapping:
    def __init__(self, start_address, end_address, weather_type, travel_date=datetime.date.today().strftime("%Y-%m-%d")):
        # initialize endpoints and api keys
        self.endpoint = "https://maps.googleapis.com/maps/api/directions/json?"
        self.googlemaps = googlemaps.Client(config.gmaps_key)
        self.owm_key = config.owm_key

        self.start_address = start_address.replace(' ', '+')
        self.end_address = end_address.replace(' ', '+')
        self.weather_type = weather_type
        self.date_of_travel = travel_date

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

    def _get_route_coords(self):
        """
        makes request to google directions api and creates a pandas dataframe to hold lat/lon pairs of route
        """

        # make request and get response
        self.nav_request = f"""origin={self.start_address}&destination={self.end_address}&key={config.gmaps_key}"""
        self.request = self.endpoint + self.nav_request
        self.response = urllib.request.urlopen(self.request).read()
        self.directions = json.loads(self.response)

        # create empty dataframe. lat = 0, lng = 1
        route_gps_coords = pd.DataFrame(columns=[0, 1])

        # determine number of steps in route
        self.steps_in_route = len(
            self.directions['routes'][0]['legs'][0]['steps'])

        # put gps coords and add to dataframe
        for i in range(self.steps_in_route):
            route_gps_coords = pd.concat([route_gps_coords,
                                          pd.DataFrame(polyline.decode((self.directions['routes'][0]['legs'][0]['steps'][i]['polyline']['points'])))])

        # reset index
        route_gps_coords = route_gps_coords.reset_index(drop=True)

        # get route coordinates as a "row list"
        self.Row_list = []

        for rows in route_gps_coords.itertuples():
            # Create list for the current row
            my_list = [rows[1], rows[2]]

            # append the list to the final list
            self.Row_list.append(my_list)

        return(route_gps_coords)

    def _check_weather(self, lat, lon):
        """
        Docstring
        """

        owm_request = f'''https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={ self.owm_key}'''

        owm_response = urllib.request.urlopen(owm_request).read()
        weather_response = json.loads(owm_response)

        for i in weather_response['list']:
            try:
                if i[self.weather_type]:
                    return (True)
            except KeyError:
                pass

        return (False)

    def _get_checkpoint_locations(self):
        """
        this function finds the locations (lat/lon) to check for weather along a route. every 10 miles.
        return: list 
        """
        checkpoint_locations = []
        route_length = int(
            self.directions['routes'][0]['legs'][0]['distance']['text'].split(' ')[0])
        self.number_of_checkpoints = math.ceil(route_length/10)

        for i in range(1, len(self.route_gps_coords),  math.floor(len(self.route_gps_coords)/self.number_of_checkpoints)):
            checkpoint_locations.append({'name': f"""{i}""",
                                         'location': (self.route_gps_coords.iloc[i].values[0], self.route_gps_coords.iloc[i].values[1])})

        return (checkpoint_locations)

    def create_map(self):
        # get the gps coordinates for the route.
        self.route_gps_coords = self._get_route_coords()

        # create and center map at center of route
        self.map = folium.Map(location=self.Row_list[round(
            len(self.route_gps_coords)/2)], zoom_start=8)

        # add route polylines to map
        folium.PolyLine(locations=self.Row_list,
                        line_opacity=0.5).add_to(self.map)

        # starting marker
        folium.Marker(self.Row_list[0], popup='Origin').add_to(self.map)

        # ending marker
        folium.Marker(self.Row_list[-1],
                      popup='Destination').add_to(self.map)

        # get checkpoint locations
        self.checkpoint_locations = self._get_checkpoint_locations()

        # add markers to map
        for i in self.checkpoint_locations:

            if self._check_weather(i['location'][0], i['location'][1]) == True:

                url = f'''https://openweathermap.org/city/{self.checkpoint_locations['name']}'''
                weblink = f'''<a href=" {url} "target="_blank"> {'Link to weather 5 day forecast'} {'</a>'}'''

                iframe = folium.IFrame(
                    html=url, width=200, height=75)
                popup = folium.Popup(iframe, max_width=2650)

                folium.Marker(weblink, popup=popup).add_to(self.map)

        return self.map


def weather_map(origin, destination, weather_type, travel_date):
    # create WeatherMapping object
    w = WeatherMapping(origin, destination, weather_type,
                       travel_date)

    map = w.create_map()

    # save map data
    map.save('map.html', close_file=False)

    # get map data
    webbrowser.open('map.html')


weather_map("Seattle, WA", "Moses Lake, WA",
            "Clouds", datetime.datetime.today().strftime('%Y-%m-%d'))
