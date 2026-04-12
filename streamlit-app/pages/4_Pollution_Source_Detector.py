import streamlit as st
import requests
from PIL import Image
import numpy as np
import os
from dotenv import load_dotenv
import base64
import io

load_dotenv()
FASTAPI_URL = os.environ["FASTAPI_URL"]
st.title("🔰Pollution Source Detector")
st.subheader("Detects pollution sources on land (Smoke, Vehicles, Fire or Garbage) from any given image.")

st.divider()

image = st.file_uploader("Upload an image!", type=["jpg", "jpeg", "png"])

st.write("or try with these:")
col1,col2,col3 = st.columns(3)

with col1:
    path = os.path.join("streamlit-app", "pages", "example_images", "example1.jpg")
    st.image(path, caption = "Hosur Road (Near Singasandra Metro Station), Electronic City, Bengaluru")
    if st.button("Detect", key=1, use_container_width=True):
        image = path
with col2:
    path = os.path.join("streamlit-app", "pages", "example_images", "example2.jpg")
    st.image(path, caption = "Neeladri Road (Near Neo Hospital), Electronic City, Bengaluru")
    if st.button("Detect", key=2, use_container_width=True):
        image = path
with col3:
    path = os.path.join("streamlit-app", "pages", "example_images", "example3.jpg")
    st.image(path, caption = "Thogur Cross, Electronic City, Bengaluru")
    if st.button("Detect", key=3, use_container_width=True):
        image = path

if image is not None: # if an image is uploaded
    image = Image.open(image) # bytes to image
    buffered = io.BytesIO() # in memory
    image.save(buffered, format="JPEG") # writing image bytes to memory
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8") # convets to jpeg then base64 string

    with st.spinner("Vayu is thinking..."):
        res = requests.post(f"{FASTAPI_URL}/cv_predict", json={"image":img_b64}).json()
        
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="uploaded image")

    with col2:
        annotated_image = res.get("annotated_image", 0)
        annotated_image = base64.b64decode(annotated_image)
        annotated_image = Image.open(io.BytesIO(annotated_image))
        st.image(annotated_image, caption="annotated image")

st.subheader("How it works")
st.write("""This tool uses YOLO-based object detection for urban pollution sources, trained on a real-world dataset of Indian street imagery spanning multiple locations across Bengaluru. Images were preprocessed and augmented to improve robustness across varying lighting conditions, camera angles, and urban environments.

The detection threshold is tuned for high recall, prioritizing catching every potential pollution source over avoiding false positives, which is critical for real-world environmental monitoring.

Detected classes: Vehicles, Garbage, Smoke, Fire""")

st.subheader("Use cases")
st.write("Built for applications like traffic emission monitoring, municipal solid waste identification, and early fire or smoke detection. Data collected from this tool can help civic bodies prioritize cleanup efforts and identify high-pollution zones in real time.")