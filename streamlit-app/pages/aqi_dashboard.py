import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # adding streamlit-app to sys.path to import utils

import streamlit as st
import pandas as pd
from utils.aqi import get_multiple_cities, aqi_color, get_aqi

st.set_page_config(page_title="Vayu AQI Dashboard", page_icon="🔰")
st.title("Vayu AQI Dashboard")
st.caption("Real time AQI Dashboard for selected cities")

cities = st.multiselect(label = "Select one or more cities", options = ["Bangalore", "Mumbai", "Pune", "Jakarta", "Washington"])

if st.button("🔃 Fetch Live Data"):
    if cities:
        with st.spinner("Fetching.."):
            data = get_multiple_cities(cities)

            if not data: st.error("Check your API token")

            df = pd.DataFrame(data)
            df = df.replace("N/A", None)
            
            for i in data:
                st.header(i["city"])
                st.write(i)

            st.header("Dataframe with AQI Metrics of theSelected Cities")
            st.write(df.head())
        
    else:
        st.toast("Select one or more city!")


