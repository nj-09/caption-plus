import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

# Load the correct Gemini model (1.5 recommended)
model = genai.GenerativeModel("gemini-1.5-pro")  # ✅ No "models/" prefix

def fix_grammar_with_gemini(text, glossary=None):
    """Fix grammar using Gemini with optional glossary."""
    prompt = "Correct ONLY grammar, spelling, and punctuation. Do NOT add extra info. Return corrected text:\n"
    if glossary:
        prompt = glossary + "\n\n" + prompt

    try:
        response = model.generate_content(prompt + text)
        return response.text
    except Exception as e:
        print("❌ Gemini SDK Error:", e)
        return f"[Error: Gemini API failed: {str(e)}]"