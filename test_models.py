import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

try:
    model = genai.GenerativeModel('gemma-4-26b-a4b-it')
    response = model.generate_content("Based on 195 mins active, VS Code most used, 23% distraction. Give 2 sentence advice. CRITICAL: Output ONLY the advice. No reasoning or drafts.")
    print("SUCCESS! Gemma Response:", response.text)
except Exception as e:
    print("Error:", e)
