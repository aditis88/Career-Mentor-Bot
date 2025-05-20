# model_switcher.py

import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-1.5-flash"

# Setup Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Only import OpenAI if key is present
try:
    if OPENAI_API_KEY:
        import openai
        openai.api_key = OPENAI_API_KEY
        OPENAI_MODEL = "gpt-3.5-turbo"
    else:
        openai = None
except Exception:
    openai = None

def get_response_from_openai(prompt: str) -> str:
    if not openai:
        return "[OpenAI] API key not found or not set."
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAI Error] {str(e)}"

def get_response_from_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] {str(e)}"

def get_response(prompt: str, model: str = "Gemini") -> str:
    if model.lower() == "openai" and openai:
        return get_response_from_openai(prompt)
    return get_response_from_gemini(prompt)
