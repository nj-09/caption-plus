from pydub import AudioSegment

def convert_mp3_to_wav(mp3_file, wav_file):
    """Convert an MP3 audio file to WAV format."""
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")