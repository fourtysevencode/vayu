import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from streamlit_folium import st_folium
from utils.ndvi_map import create_map

m = create_map()
st.title("NDVI-AQI corelation map")

st.divider()

st_folium(m, width=700, height=500)

