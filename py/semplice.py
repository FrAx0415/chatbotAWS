from flask import Flask, request, jsonify
import os
from elevenlabs.client import ElevenLabs
from flask_cors import CORS
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

API_KEY = "sk_61cddb7392d84a46443fcb7e8aebbc1673ef73ed1d412f7a"
UPLOAD_FOLDER = "./audio_input"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client = ElevenLabs(api_key=API_KEY)

def convert_to_mp3(file_path):
    """Converte un file audio in MP3 se necessario."""
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == ".webm":  # Se il file è in WebM, lo convertiamo
        mp3_path = file_path.replace(".webm", ".mp3")
        audio = AudioSegment.from_file(file_path, format="webm")
        audio.export(mp3_path, format="mp3")
        os.remove(file_path)  # Rimuove il file originale
        return mp3_path
    return file_path  # Se è già MP3, lo lascia invariato

def process_audio_file(file_path):
    """Elabora il file audio con ElevenLabs."""
    try:
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()

        if not audio_data:
            return {"error": "Il file è vuoto"}

        response = client.speech_to_text.convert(
            file=audio_data, model_id="scribe_v1", language_code="it"
        )
        return {"text": response.text}

    except Exception as e:
        return {"error": str(e)}

@app.route('/caricaudio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "Nessun file fornito"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nessun file selezionato"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Converti in MP3 se necessario
    file_path = convert_to_mp3(file_path)

    # Elabora il file convertito
    result = process_audio_file(file_path)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)