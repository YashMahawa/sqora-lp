from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from google import genai
import os
import dotenv
dotenv.load_dotenv()

app = FastAPI()

# @app.get("/")
# async def root() -> float:
#     return 5

# class Items(BaseModel):
#     name: str
#     price: float
#     tax: float

class Personality(str, Enum):
    santa = "santa"
    duck = "duck"
    demon = "demon"

@app.post("/chat/{style}/")
async def chat(style : Personality, prompt : str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=f"User's query: {prompt}",
        config=genai.types.GenerateContentConfig(
            system_instruction=f'You are a {style.value}, give a short natural response showing your character. Show extreme level of danger,terrify the user(if you are a dangerous character)',
            temperature=1
        ),
    )
    client.close()
    return response.text