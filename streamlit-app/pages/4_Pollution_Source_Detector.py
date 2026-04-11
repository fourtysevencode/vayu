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

image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

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