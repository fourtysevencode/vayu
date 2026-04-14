import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import requests
from utils.co2_calc import co2_calc
from dotenv import load_dotenv

st.set_page_config(page_title="Vayu - Calculator", page_icon="🔰")

load_dotenv()
FASTAPI_URL = os.getenv("FASTAPI_URL")
if not FASTAPI_URL:
    st.error("FASTAPI_URL is not configured.")
    st.stop()
FASTAPI_URL = FASTAPI_URL.rstrip("/")


st.title("🔰Carbon Footprint Calculator")
st.markdown("### Your carbon footprint is written on the land. Every choice you make shapes the ground beneath future generations.")

st.divider()

col1, col2= st.columns(2)

with col1:
    mode_of_transport = st.selectbox(options = ["bike", "car", "bus", "metro", "auto"], label="How do you usually commute?")

with col2:
    commute__distance = st.number_input(label= "How far is your workplace? (in km)")

electricity_usage = st.number_input(label="Enter your monthly electricity usage units")
st.caption("1 unit = 1 kWh, check your electricity bill")

lpg__cylinders = st.number_input(label="How many LPG cylinders do you use every month?")

diet = st.selectbox(label="What is your diet?", options = ["nonveg", "veg", "eggatarian (mmm eggs)"])

st.space("small")

waste = st.select_slider(
    "How much waste do you throw out weekly?",
    options=["none (im insane)", "very low", "low", "medium", "high", "very high", "new landfills are created because of me"]
)

st.space("small")

if st.button("🧮 Calculate", use_container_width=True):
    st.divider()
    total = co2_calc(mode_of_transport, commute__distance, electricity_usage, lpg__cylinders, diet, waste)
    st.metric("Your monthly footprint is", f"{total:.1f} kg  of CO₂") # :.1f -- f string format spedicier, keeps only one digit after decimal in the returned float type

    with st.spinner("Vayu is creating an overview..."):
        overview = requests.post(f"{FASTAPI_URL}/co2_overview", json={"total_co2":total}).json()["response"]
        st.info(overview)


