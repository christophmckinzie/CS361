from fastapi import FastAPI
import config
import requests

# to run the server enter the command below in shell
# uvicorn server:app --port 8000 --reload

# example call to api: https://cs361-1-l3925805.deta.app/onecall/lat=47.753990&lon=-122.163008

# IMPORTANT: REQUIREMENTS.TXT MUST BE ENCODED USING UTF-8 FOR "space new" COMMAND TO WORK


app = FastAPI()
owm_key = config.owm_key


@app.get("/")
def read_root():
    return "Hello, Jared Chang. Welcome to my weather API."


@app.get("/onecall")
async def onecall(request: dict):
    lat = request.get("lat")
    lon = request.get("lon")
    weather_response = requests.get(
        f'''https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={owm_key}&units=imperial''')
    return weather_response.json()


@app.get("/forecast")
async def forecast(request: dict):
    lat = request.get("lat")
    lon = request.get("lon")
    response = requests.get(
        f'''https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={owm_key}&units=imperial''')
    return response.json()
