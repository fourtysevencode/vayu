from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi .responses import HTMLResponse
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv
from ultralytics import YOLO
from PIL import Image
import io
import base64


app = FastAPI()
load_dotenv()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
templates = Jinja2Templates(directory="templates")


prompt = """
You are Vayu, an AI assistant built into an environmental monitoring platform for Indian cities. You help users understand air quality, pollution, and their environmental impact.

You have access to the following features on the platform:
- Real-time AQI data for Indian cities (via WAQI API)
- A carbon footprint calculator
- A YOLOv8-powered pollution source detector

Your job:
- Answer questions about air quality, AQI levels, pollutants (PM2.5, PM10, NO2, CO, O3, SO2), and what they mean for health
- Help users interpret their carbon footprint results and suggest practical ways to reduce emissions
- Explain what the pollution detector identified and why it matters
- Give city-specific context when relevant (e.g. Delhi winters, Bangalore traffic, industrial zones)
- Suggest actionable steps people can actually take, not just generic advice

Tone: clear, direct, and informative. You're talking to everyday Indians, not climate scientists. Avoid jargon unless you explain it. Be honest about uncertainty when data is limited.

Boundaries: only discuss topics related to environment, air quality, climate, and pollution. If someone asks something off-topic, politely redirect them to what Vayu is built for.

Never make up AQI values or pollution statistics. If you don't have real data, say so.

Your max tokens per reply is 1024. Do not ever exceed.
"""

genai.configure(api_key=GEMINI_API_KEY)
client = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=prompt
)

model = YOLO("best.onnx")

class user_message(BaseModel):
    message: str

class aqi_data(BaseModel):
    cities: list[str]
    aqi: list[float]
class co2(BaseModel):
    total_co2: float
class ImagePayload(BaseModel):
    image: str

@app.get("/")
async def home():
    return {"status":"seems to be working fine.."}

@app.post("/chat")
def send_response(message: user_message):
    try:
        response = client.generate_content(
            message.message,
            generation_config={"max_output_tokens": 1024}
        )
        return {"response":response.text}
    
    except Exception as e:
        return {"response":f"Error: {e}"}

@app.post("/dashboard_overview")
def overview(data: aqi_data):
    try:
        response = client.generate_content(
            f"In 1-2 sentences max, describe the AQI of {data.aqi} in {data.cities} using a simple real-life comparison anyone would get (e.g. 'like standing behind a bus'). No jargon.",
            generation_config={"max_output_tokens": 1024}
        )
        return {"response":response.text}
    
    except Exception as e:
        return {"response":f"Error: {e}"}


@app.post("/co2_overview")
def co2_overview(total: co2):
    try:
        response = client.generate_content(
            f"""In 2–3 sentences, explain a monthly carbon footprint of {total.total_co2} kg CO₂e in simple, relatable terms. Compare it to the average footprint of a person in India and briefly indicate whether it is lower, typical, or higher (you may estimate if needed). Add one concrete equivalence (e.g., number of trees needed to offset it or everyday activity comparisons) and include one practical suggestion to reduce it. Keep it clear, grounded, and conversational with no jargon or bullet points.""",
            generation_config={"max_output_tokens": 1024}
        ) # sorry for the ugly looking code reader!
        return {"response":response.text}
    
    except Exception as e:
        return {"response":f"Error: {e}"}
    
@app.post("/cv_predict")
def predict(image: ImagePayload):
    img_bytes = base64.b64decode(image.image)
    img = Image.open(io.BytesIO(img_bytes))
    img_array = np.array(img)

    result = model.predict(img_array, conf=0.1, iou=0.45, show_conf=False) # iou = intersection over union, if boxes overlap by over 45% -> kills weaker one
    print(f"boxes: {result[0].boxes}")
    print(f"conf scores: {result[0].boxes.conf}")
    annotated = result[0].plot(conf=False)
    
    annotated_pil = Image.fromarray(annotated)
    buffered = io.BytesIO()
    annotated_pil.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"annotated_image": img_b64}

@app.get("/health")
def health():
    return {"status":"alive"}
