import os
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("CRITICAL: GEMINI_API_KEY is missing from environment variables.")

# Initialize standard Google GenAI Client
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="ChefAI Agent Backend")

# Allow mobile apps to connect
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
    """Modifies the AI output based on whether the user has paid or not."""
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
async def recipe_from_photo(
    user_tier: str = Form("free"), 
    file: UploadFile = File(...)
):
    """Accepts an image file from a mobile phone and generates a recipe."""
    try:
        # Read uploaded image bytes
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Build monetization logic into prompt
        prompt = "Identify the food items in this image and create a delicious recipe from them."
        prompt += get_monetization_prompt(user_tier)

        # Call Gemini 2.5 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image, prompt],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        return {"success": True, "tier": user_tier, "recipe": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recipe/voice-text")
async def recipe_from_voice_text(
    text_input: str = Form(...), 
    user_tier: str = Form("free")
):
    """Accepts a text string (transcribed from mobile voice) and generates a recipe."""
    try:
        prompt = f"The user says: '{text_input}'. Create a recipe based on this request."
        prompt += get_monetization_prompt(user_tier)

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        return {"success": True, "tier": user_tier, "recipe": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
