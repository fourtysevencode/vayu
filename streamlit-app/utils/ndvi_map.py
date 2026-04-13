import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import folium
from utils.aqi import aqi_color, get_from_waqi, getall_stations
import json

with open("streamlit-app/utils/data/city_ndvi.json") as f:
    NDVI_DATA = json.load(f)


def map_with_aqi(city, lat, lon):

    NDVI = NDVI_DATA.get(city,0)
    m = folium.Map(
        location=[lat,lon], zoom_start=11
    )

    # NDVI
    folium.Circle(
        location=[lat,lon],
        radius = NDVI * 40000,
        color="#006400", # border color
        fill=True,
        fill_opacity=0.2,
        tooltip = f"NDVI in {city}: {NDVI}"
    ).add_to(m)

    stations = getall_stations(city)
    for station in stations:
        aqi = int(station["aqi"])
        aqi_colorname, remark = aqi_color(aqi)
        aqi_colorname = aqi_colorname[0]
        lat_aqi_station,lon_aqi_station = station["geo"]
        if [lat_aqi_station,lon_aqi_station] == [None, None]:
            lat_aqi_station,lon_aqi_station  = lat,lon

        folium.Circle(
            color=aqi_colorname,
            location=[lat_aqi_station,lon_aqi_station],
            fill=True,
            fill_opacity=0.4,
            radius=1000,
            tooltip=f"{station["name"]}: AQI = {aqi} ({remark})"
        ).add_to(m)

    return m