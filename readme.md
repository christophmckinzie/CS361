Microservice Description/Communication Contract:
There is a single GET request available from my microservice's API which is set up using Deta Space server.

Microservice Usage:
{GET} https://cs361-2-l3925805.deta.app/onecall/lat={lat}&lon={lon}

"lat" and "lon" are the latitude and longitude of the location you wish to receive weather data about. This API call in turns sends a request to Openweathermaps API "onecall" GET request. The response from the microservice is in JSON.

lat---> float

lon---> float

UML Microservice (API) Sequence Diagram:
![image](https://user-images.githubusercontent.com/57605404/218647364-20b4d51b-500d-457e-b42f-330d8322b0bd.png)
