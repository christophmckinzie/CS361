from fastapi import FastAPI
import urllib.request
import json
import config

# to run the server enter the command below in shell
# uvicorn server:app --port 8000 --reload

# example call to api: http://localhost:8000/owm_onecall/lat=47.753990&lon=-122.163008

# IMPORTANT: REQUIREMENTS.TXT MUST BE ENCODED USING UTF-8 FOR "DETA NEW" COMMAND TO WORK


app = FastAPI()
owm_key = config.owm_key


@app.get("/")
def read_root():
    return {"Hello": "Jared Chang"}


@app.get("/onecall/lat={lat}&lon={lon}")
def owm_onecall(lat: float, lon: float):

    try:
        request = f"""https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={owm_key}"""
        response = urllib.request.urlopen(request).read()
        weather = json.loads(response)
    except urllib.error.HTTPError:
        response = json.dumps({'HTTP Error 400:': 'Bad Request'})

    return {response}
