import streamlit as st

st.title("🔰 Vayu", text_alignment="center")
st.caption("decoding the planet, one insight at a time", text_alignment="center")
st.set_page_config(page_title="Vayu - Home", page_icon="🔰")



st.write("---")
st.header("The Problem")
st.markdown("""#### India has some of the worst air quality globally most people don't understand AQI beyond a number. Pollution sources are visible but not climate change because of it. Personal impact is ignored or misunderstood. *Data exists, but insight doesn't*""")
st.space("small")
st.info("Vayu connects air quality, personal impact, and real-world visibility into one system to aid awareness.")

st.write("---")
st.header("Features")

st.subheader("🌫️ AQI Dashboard")
st.write("Live air quality data for Indian cities. Track PM2.5, PM10, NO2 and more with interactive charts.")
if st.button("Go to Dashboard", use_container_width=True):
    st.switch_page("pages/1_Dashboard 📊.py")

st.subheader("📷 Pollution Detector")
st.write("Upload an image or use your camera to detect pollution sources using a YOLOv8 model.")
if st.button("Open Detector", use_container_width=True):
    st.switch_page("pages/2_Pollution_Source_Detector.py")

st.subheader("🌿 Green Cover vs Air Quality")
st.write("View a real-time map showcasing AQI vs Tree Cover in Indian Cities")
if st.button("Open Map", use_container_width=True):
    st.switch_page("pages/3_Green_Cover_vs_Air_Quality.py")

st.subheader("🤖 Vayu Chatbot")
st.write("Ask anything about air quality, AQI, or your carbon footprint. Plain answers, no jargon.")
if st.button("Chat with Vayu", use_container_width=True):
    st.switch_page("pages/4_Chat 💬.py")

st.subheader("🌱 Carbon Footprint Calculator")
st.write("Estimate your personal carbon emissions based on your commute, diet, and energy usage.")
if st.button("Calculate Footprint", use_container_width=True):
    st.switch_page("pages/5_Carbon Foorprint Calculator 💚.py")

st.divider()

st.subheader("💻 Source Code")
st.link_button("View the source code here", "https://github.com/fourtysevencode/vayu", use_container_width=True)

st.space("small")
st.caption("with 💗 from fourtysevencode")

 