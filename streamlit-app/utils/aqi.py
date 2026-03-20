import requests
import os
from dotenv import load_dotenv

load_dotenv() # creates environment from the .env file (finds automatically) and creates an environment
TOKEN = os.getenv("WAQI_TOKEN") # retieves WAQI token

def aqi_color(value): # AQI color values | source: https://vajiramandravi.com/current-affairs/national-air-quality-index/#:~:text=Good%20(0%20to%2050):,existing%20diseases%20face%20serious%20complications.
    if value <= 50:   return "#00e400", "Good"
    if value <= 100:  return "#ffff00", "Moderate"
    if value <= 150:  return "#ff7e00", "Unhealthy for Sensitive Groups"
    if value <= 200:  return "#ff0000", "Unhealthy"
    if value <= 300:  return "#8f3f97", "Very Unhealthy"
    return "#7e0023", "Hazardous"

def get_aqi(city):
    url = f"https://api.waqi.info/feed/{city}?token={TOKEN}"
    r = requests.get(url)
    data = r.json() # parses json api response to dictionary
    if data["status"] != "ok": # if response is corrupt, return None
        return None
    d = data["data"]
    # return a dictionary of real-time aqi data from api response
    return {
        "name":d["attributions"][0]["name"],
        "city":city,
        "time":d["time"]["s"],
        "aqi":d["aqi"],
        "pm25":d["iaqi"]["pm25"]["v"],
        "pm10":d["iaqi"]["pm10"]["v"],
        "so2":d["iaqi"]["so2"]["v"],
        "o3":d["iaqi"]["o3"]["v"],
        "no2":d["iaqi"]["no2"]["v"],
        "co":d["iaqi"]["co"]["v"],
        "dew":d["iaqi"]["dew"]["v"]
    }

def get_multiple_cities(cities):
    results = []
    for city in cities:
        data = get_aqi(city)
        if data: # if response is not None, else ignore
            results.append(data) 
    return results # list of dictionaries of results from inputted cities in an iterable

