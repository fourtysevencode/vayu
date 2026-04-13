import streamlit as st

st.title("🔰Welcome to Vayu")
st.subheader("Your Climate Change Buddy")
st.set_page_config(page_title="Vayu Home", page_icon="🔰")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.write("---")
st.header("Purpose")
st.markdown("""
    <style>
    .card {
        border-radius: 12px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .card span {
        font-weight: 700;
        margin-right: 0.6rem;
    }
    </style>

    <div class="card" style="background:#0f1a24; border:1px solid #1e3a50; color:#ddeef8;">
        <span style="color:#38b4d9;">></span>India is home to 9 of the world's 10 most polluted cities. The air quality crisis isn't coming, it's already here.</div>

    <div class="card" style="background:#140f1a; border:1px solid #3a1e50; color:#ddeef8;">
        <span style="color:#a855f7;">></span>Climate change is making it worse. Rising temperatures accelerate the formation of ground-level ozone, and longer dry seasons mean more dust and wildfire smoke.</div>

    <div class="card" style="background:#1a1409; border:1px solid #503a1e; color:#ddeef8;">
        <span style="color:#f59e0b;">></span>Most people have no idea what they're breathing. AQI numbers exist but nobody explains what they actually mean for your health.</div>

    <div class="card" style="background:#1a0f0f; border:1px solid #501e1e; color:#ddeef8;">
        <span style="color:#ef4444;">></span>Transportation, construction, crop burning, and industrial emissions are the biggest culprits in Indian cities. The sources are visible, but rarely tracked in one place.</div>

    <div class="card" style="background:#0f1214; border:1px solid #1e2e3e; color:#ddeef8;">
        <span style="color:#94a3b8;">></span>Individual action matters more than people think. Your commute, your diet, your energy use all have a measurable carbon cost.</div>

    <div class="card" style="background:#0a1a12; border:1px solid #1e5032; color:#ddeef8;">
        <span style="color:#38d9c0;">></span>Vayu brings it all together. Real-time AQI for Indian cities, a personal carbon footprint calculator, and an AI pollution detector so you can see the problem and understand your part in it.</div>

""", unsafe_allow_html=True)

st.write("---")
st.header("Features")

st.subheader("🌫️ AQI Dashboard")
st.write("Live air quality data for Indian cities. Track PM2.5, PM10, NO2 and more with interactive charts.")
if st.button("Go to Dashboard"):
    st.switch_page("pages/1_Dashboard 📊.py")

st.subheader("📷 Pollution Detector")
st.write("Upload an image or use your camera to detect pollution sources using a YOLOv8 model.")
if st.button("Open Detector"):
    st.switch_page("pages/4_Pollution_Source_Detector.py")

st.subheader("🌿 Green Cover vs Air Quality")
st.write("View a real-time map showcasing AQI vs Tree Cover in Indian Cities")
if st.button("Open Map"):
    st.switch_page("pages/5_Green_Cover_vs_Air_Quality.py")

st.subheader("🤖 Vayu Chatbot")
st.write("Ask anything about air quality, AQI, or your carbon footprint. Plain answers, no jargon.")
if st.button("Chat with Vayu"):
    st.switch_page("pages/2_Chat 💬.py")

st.subheader("🌱 Carbon Footprint Calculator")
st.write("Estimate your personal carbon emissions based on your commute, diet, and energy usage.")
if st.button("Calculate Footprint"):
    st.switch_page("pages/3_Carbon Foorprint Calculator 💚.py")

 