from audio_utils import convert_mp3_to_wav
from deepgram_api import transcribe_audio
from gemini_api import fix_grammar_with_gemini
import os
import time
import difflib

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
            # Deleted/incorrect word = red
            print(f"\033[91m{word[2:]}\033[0m", end=' ', flush=True)
        elif word.startswith("+ "):
            # New or corrected word = green
            print(f"\033[92m{word[2:]}\033[0m", end=' ', flush=True)
        time.sleep(0.07)
    print("\n")

def print_banner(text):
    print(f"\n\033[96m=== {text} ===\033[0m\n")
    time.sleep(0.5)

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

        print("[🧠] Transcribing audio with Deepgram...")
        raw_text = transcribe_audio(wav_file)

        print_banner("Raw Transcript")
        typewriter_print(raw_text)

        glossary = "Glossary: kernel = computer core, not colonel. cache = memory, not cash. parsing = analyzing, not passing."
        print("[✨] Sending to Gemini for grammar fix...")
        cleaned_text = fix_grammar_with_gemini(raw_text, glossary)

        print_banner("Cleaned Transcript (Highlighted)")
        highlight_diff_words(raw_text, cleaned_text)

        print_banner("Process Complete ✔")
