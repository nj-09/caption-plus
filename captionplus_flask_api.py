from flask import Flask, request, jsonify
from audio_utils import convert_mp3_to_wav
from deepgram_api import transcribe_audio
from gemini_api import fix_grammar_with_gemini
import os
import tempfile

app = Flask(__name__)

@app.route('/caption', methods=['POST'])
def caption_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    glossary = request.form.get('glossary', '')

    with tempfile.TemporaryDirectory() as tmpdir:
        mp3_path = os.path.join(tmpdir, 'input.mp3')
        wav_path = os.path.join(tmpdir, 'input.wav')
        audio_file.save(mp3_path)

        convert_mp3_to_wav(mp3_path, wav_path)
        raw_text = transcribe_audio(wav_path)
        cleaned_text = fix_grammar_with_gemini(raw_text, glossary)

    return jsonify({
        'raw': raw_text,
        'cleaned': cleaned_text
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)