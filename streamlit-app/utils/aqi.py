import requests
import os
from dotenv import load_dotenv

load_dotenv() # creates environment from the .env file (finds automatically) and creates an environment
TOKEN = os.getenv("WAQI_TOKEN") # retieves WAQI token

def aqi_color(value): # AQI color values | source: https://vajiramandravi.com/current-affairs/national-air-quality-index/#:~:text=Good%20(0%20to%2050):,existing%20diseases%20face%20serious%20complications.
    if value <= 50:   return ["#00e400", "green"], "Good"
    if value <= 100:  return ["#ffff00", "yellow"], "Moderate"
    if value <= 150:  return ["#ff7e00", "orange"], "Unhealthy for Sensitive Groups"
    if value <= 200:  return ["#ff0000", "red"], "Unhealthy"
    if value <= 300:  return ["#8f3f97", "violet"], "Very Unhealthy"
    return ["#1e1e1e", "grey"], "Hazardous"

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
        "pm25": d["iaqi"].get("pm25", {}).get("v", "N/A"), # returns N/A if sensor doesn't exist for a specific pollutant
        "pm10": d["iaqi"].get("pm10", {}).get("v", "N/A"),
        "so2":  d["iaqi"].get("so2",  {}).get("v", "N/A"),
        "o3":   d["iaqi"].get("o3",   {}).get("v", "N/A"),
        "no2":  d["iaqi"].get("no2",  {}).get("v", "N/A"),
        "co":   d["iaqi"].get("co",   {}).get("v", "N/A"),
        "dew":  d["iaqi"].get("dew",  {}).get("v", "N/A"),
    }

def get_multiple_cities(cities):
    results = []
    for city in cities:
        data = get_aqi(city)
        if data: # if response is not None, else ignore
            results.append(data) 
    return results # list of dictionaries of results from inputted cities in an iterable

