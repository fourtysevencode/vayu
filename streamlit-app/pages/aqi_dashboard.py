import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # adding streamlit-app to sys.path to import utils

import streamlit as st
import pandas as pd
from utils.aqi import get_multiple_cities, aqi_color, get_aqi

st.set_page_config(page_title="AQI Dashboard", page_icon="🌫️")
st.title("AQI Dashboard")
st.caption("Real time AQI Dashboard for selected cities")

cities = st.multiselect(label = "city", options = ["Bangalore", "Mumbai", "Pune", "Jakarta", "Washington"])

if st.button("🔃 Fetch Live Data"):
    with st.spinner("Fetching.."):
        data = get_multiple_cities(cities)

for i in data:
    for j in cities:
        if i["city"] == j:
            st.header(j)
            st.write(i)

