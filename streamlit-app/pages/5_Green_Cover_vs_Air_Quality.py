import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from streamlit_folium import st_folium
from utils.ndvi_map import map_with_aqi
from utils.aqi import get_aqi
import json

st.title("🔰 Vayu NDVI-AQI Map")
st.subheader("Green Cover vs Air Quality")
st.caption("Exploring how vegetation density correlates with real-time AQI across major Indian cities.")

if "map" not in st.session_state:
    st.session_state.map = None

CITY_COORDS = {
    "Delhi": [28.6139, 77.2090],
    "Mumbai": [19.0760, 72.8777],
    "Bangalore": [12.9716, 77.5946],
    "Chennai": [13.0827, 80.2707],
    "Kolkata": [22.5726, 88.3639],
    "Hyderabad": [17.3850, 78.4867],
    "Ahmedabad": [23.0225, 72.5714],
    "Pune": [18.5204, 73.8567],
    "Jaipur": [26.9124, 75.7873],
    "Lucknow": [26.8467, 80.9462],
    "Surat": [21.1702, 72.8311],
    "Kanpur": [26.4499, 80.3319],
    "Nagpur": [21.1458, 79.0882],
    "Bhopal": [23.2599, 77.4126],
    "Patna": [25.5941, 85.1376],
}

selected_city = st.selectbox(options=list(CITY_COORDS.keys()), label="Choose city")
if st.button("Fetch", use_container_width=True):
    st.divider()
    lat, lon = CITY_COORDS[selected_city]
    with st.spinner("Vayu is thinking..."):
        m = map_with_aqi(selected_city, lat, lon)
        st.session_state.map = m

if st.session_state.map is not None:
    st_folium(st.session_state.map, width=800, height=500)

st.divider()

