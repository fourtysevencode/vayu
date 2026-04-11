from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi .responses import HTMLResponse
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
from ultralytics import YOLO
from PIL import Image
import io
import base64


app = FastAPI()
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
templates = Jinja2Templates(directory="templates")
client = OpenAI(
    api_key = OPENAI_API_KEY
)


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

model_path = os.environ["CV_MODEL_PATH"]
model = YOLO(model_path)

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
        response = client.responses.create(
            model = "gpt-5-nano",
            input = [
                {"role":"system", "content":prompt},
                {"role": "user", "content":message.message}
            ]
        )
        return {"response":response.output_text}
    
    except Exception as e:
        return {"response":f"Error: {e}"}

@app.post("/dashboard_overview")
def overview(data: aqi_data):
    try:
        response = client.responses.create(
            model = "gpt-5-nano",
            input = [
                {"role":"system", "content":prompt},
                {"role": "system", "content":f"In 1-2 sentences max, describe the AQI of {data.aqi} in {data.cities} using a simple real-life comparison anyone would get (e.g. 'like standing behind a bus'). No jargon."},
            ]
        )
        return {"response":response.output_text}
    
    except Exception as e:
        return {"response":f"Error: {e}"}


@app.post("/co2_overview")
def co2_overview(total: co2):
    try:
        response = client.responses.create(
            model = "gpt-5-nano",
            input = [
                {"role":"system", "content":prompt},
                {"role":"system", "content":f"""
In 2-3 sentences, describe a monthly carbon footprint of {total.total_co2} kg CO₂e in simple, 
relatable terms. Compare it to a celebrity or world leader's lifestyle (e.g. Taylor Swift's 
private jet, Elon Musk's rockets, Jeff Bezos's yacht and other famous celebrities or world leaders like Donald Trump, Narendra Modi and others.). Be witty but keep it grounded. 
No jargon, no bullet points, just a punchy paragraph. Avoid using more than 2 em dashes.
"""} # sorry for the ugly looking code reader!
            ]
        )
        return {"response":response.output_text}
    
    except Exception as e:
        return {"response":f"Error: {e}"}
    
@app.post("/cv_predict")
def predict(image: ImagePayload):
    img_bytes = base64.b64decode(image.image)
    img = Image.open(io.BytesIO(img_bytes))
    img_array = np.array(img)

    result = model.predict(img_array)
    annotated = result[0].plot()
    
    annotated_pil = Image.fromarray(annotated)
    buffered = io.BytesIO()
    annotated_pil.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"annotated_image": img_b64}

@app.get("/health")
def health():
    return {"status":"alive"}