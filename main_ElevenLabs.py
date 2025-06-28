import os
import time
import difflib
import requests
from pydub import AudioSegment
from gemini_api import fix_grammar_with_gemini  # Make sure this file is available

def convert_mp3_to_wav(input_file, output_file):
    try:
        sound = AudioSegment.from_mp3(input_file)
        sound.export(output_file, format="wav")
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")

def typewriter_print(text, delay=0.07):
    for word in text.split():
        print(word, end=' ', flush=True)
        time.sleep(delay)
    print("\n")

def highlight_diff_words(original, cleaned):
    original_words = original.split()
    cleaned_words = cleaned.split()
    diff = difflib.ndiff(original_words, cleaned_words)
    for word in diff:
        if word.startswith("  "):
            print(word[2:], end=' ', flush=True)
        elif word.startswith("- "):
            print(f"\033[91m{word[2:]}\033[0m", end=' ', flush=True)
        elif word.startswith("+ "):
            print(f"\033[92m{word[2:]}\033[0m", end=' ', flush=True)
        time.sleep(0.07)
    print("\n")

def print_banner(text):
    print(f"\n\033[96m=== {text} ===\033[0m\n")
    time.sleep(0.5)

def transcribe_audio(filepath):
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("Missing ElevenLabs API key. Set ELEVEN_API_KEY as an environment variable.")

    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {
        "xi-api-key": api_key
    }
    files = {
        "audio": open(filepath, "rb")
    }

    print("[📤] Uploading to ElevenLabs Scribe...")
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(f"Transcription failed: {response.text}")

    return response.json().get("text", "").strip()

if __name__ == "__main__":
    mp3_file = "cs_sample.mp3"
    wav_file = "converted_audio.wav"

    if not os.path.exists(mp3_file):
        print(f"\033[91m[!] File not found: {mp3_file}\033[0m")
    else:
        print_banner("Caption+ Terminal Demo")

        print("[🎧] File found, continuing...")
        print("[🔁] Converting audio...")
        convert_mp3_to_wav(mp3_file, wav_file)

        print("[🧠] Transcribing audio with ElevenLabs...")
        raw_text = transcribe_audio(wav_file)

        print_banner("Raw Transcript")
        typewriter_print(raw_text)

        glossary = "Glossary: kernel = computer core, not colonel. cache = memory, not cash. parsing = analyzing, not passing."
        print("[✨] Sending to Gemini for grammar fix...")
        cleaned_text = fix_grammar_with_gemini(raw_text, glossary)

        print_banner("Cleaned Transcript (Highlighted)")
        highlight_diff_words(raw_text, cleaned_text)

        print_banner("Process Complete ✔")

