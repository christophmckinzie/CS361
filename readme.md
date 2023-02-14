Microservice Description:
There is a single GET request available from my microservice's API. "lat" and "lon" are the latitude and longitude of the location you wish to receive weather data about. This API call in turns sends a request to Openweathermaps API "onecall" GET request.

lat---> float
lon---> float

Microservice Usage:
GET /owm_onecall/lat={lat}&lon={lon}
