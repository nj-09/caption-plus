import requests
import os
from dotenv import load_dotenv

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def transcribe_audio(file_path):
    """Transcribe audio using Deepgram API."""
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }
    with open(file_path, "rb") as audio:
        response = requests.post(url, headers=headers, data=audio)
        result = response.json()
        return result["results"]["channels"][0]["alternatives"][0]["transcript"]