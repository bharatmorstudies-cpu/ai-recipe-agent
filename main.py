import os
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("CRITICAL: GEMINI_API_KEY is missing from environment variables.")

client = genai.Client(api_key=API_KEY)
app = FastAPI(title="ChefAI Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_INSTRUCTION = (
    "You are an elite AI Chef. You only generate recipes based on food images "
    "or voice/text input descriptions of ingredients. Keep answers structured."
)

def get_monetization_prompt(user_tier: str) -> str:
    if user_tier.lower() == "premium":
        return (
            "\n\n[PREMIUM BENEFIT]: Provide an exact breakdown of total calories, "
            "macronutrients (protein, carbs, fat), and offer 3 alternative ingredient substitutions."
        )
    return (
        "\n\n[FREE TIER]: Provide the recipe steps only. Add a polite note at the end saying "
        "'Upgrade to Premium to see calorie tracking and macro breakdowns!'"
    )

@app.post("/recipe/photo")
async def recipe_from_photo(user_tier: str = Form("free"), file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        prompt = "Identify the food items in this image and create a delicious recipe from them."
        prompt += get_monetization_prompt(user_tier)

        # Updated to Gemini 3.6 Flash
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[image, prompt],
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
        )
        return {"success": True, "tier": user_tier, "recipe": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recipe/voice-text")
async def recipe_from_voice_text(text_input: str = Form(...), user_tier: str = Form("free")):
    try:
        prompt = f"The user says: '{text_input}'. Create a recipe based on this request."
        prompt += get_monetization_prompt(user_tier)

        # Updated to Gemini 3.6 Flash
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
        )
        return {"success": True, "tier": user_tier, "recipe": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Add this at the bottom of main.py for PythonAnywhere WSGI compatibility
from asgiref.wsgi import WsgiToAsgi
wsgi_app = WsgiToAsgi(app)
