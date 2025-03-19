import os
import time
import argparse
import subprocess
import glob
from datetime import datetime
from flask import Flask, request, jsonify
from elevenlabs.client import ElevenLabs
from flask_cors import CORS  # Importa CORS
 
app = Flask(__name__)
CORS(app)
 
API_KEY = "sk_61cddb7392d84a46443fcb7e8aebbc1673ef73ed1d412f7a"
UPLOAD_FOLDER = "./audio_input"
OUTPUT_FOLDER = "./text_output"
MAX_FILES = 5  # Limite massimo di file per ciascuna cartella

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
 
client = ElevenLabs(api_key=API_KEY)
audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.webm'}

def manage_file_limit(directory, max_files=MAX_FILES):
    """
    Controlla se il numero di file in una directory supera il limite.
    Se sì, elimina i file più vecchi.
    """
    files = glob.glob(os.path.join(directory, '*'))
    
    if len(files) >= max_files:
        # Ordina i file per data di modifica (più vecchio prima)
        files_with_time = [(f, os.path.getmtime(f)) for f in files]
        files_with_time.sort(key=lambda x: x[1])
        
        # Calcola quanti file eliminare
        num_to_delete = len(files) - max_files + 1  # +1 per fare spazio al nuovo file
        
        # Elimina i file più vecchi
        for i in range(num_to_delete):
            if i < len(files_with_time):
                try:
                    os.remove(files_with_time[i][0])
                    print(f"File eliminato: {files_with_time[i][0]}")
                except Exception as e:
                    print(f"Errore nell'eliminazione del file {files_with_time[i][0]}: {e}")
 
def convert_webm_to_mp3(input_file):
    """ Converte file .webm in .mp3 usando ffmpeg """
    mp3_file = input_file.replace('.webm', '.mp3')
    command = ["ffmpeg", "-i", input_file, "-q:a", "2", "-y", mp3_file]
    try:
        subprocess.run(command, check=True)
        return mp3_file
    except subprocess.CalledProcessError as e:
        print(f"Errore nella conversione di {input_file}: {e}")
        return None
 
def process_audio_file(file_path):
    """ Processa il file audio e lo converte in testo """
    try:
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_FOLDER, f"{name_without_ext}.txt")
 
        if os.path.exists(output_path):  # Evita di rielaborare file già convertiti
            return {"message": f"Il file {filename} è già stato elaborato"}
 
        print(f"Convertendo {filename}...")
 
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
 
        if not audio_data:
            return {"error": f"Il file {file_path} è vuoto"}
 
        response = client.speech_to_text.convert(
            file=audio_data, model_id="scribe_v1", language_code="it"
        )
        
        # Gestisci il limite di file nella cartella di output prima di scrivere il nuovo file
        manage_file_limit(OUTPUT_FOLDER)
        
        with open(output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(response.text)
 
        print(f"Conversione completata: {output_path}")
        return {"text": response.text}
 
    except Exception as e:
        return {"error": str(e)}
 
@app.route('/caricaudio', methods=['POST'])
def upload_audio():
    """ Endpoint per caricare file audio """
    if 'file' not in request.files:
        return jsonify({"error": "Nessun file fornito"}), 400
 
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nessun file selezionato"}), 400
    
    # Gestisci il limite di file nella cartella di input prima di salvare il nuovo file
    manage_file_limit(UPLOAD_FOLDER)
    
    # Aggiungi un timestamp al nome del file per evitare collisioni
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    new_filename = f"audio_{timestamp}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, new_filename)
    
    file.save(file_path)
 
    # Se il file è webm, convertirlo in mp3 prima di elaborarlo
    _, ext = os.path.splitext(new_filename)
    if ext.lower() == ".webm":
        mp3_path = convert_webm_to_mp3(file_path)
        if mp3_path:
            os.remove(file_path)  # Rimuove il file webm originale
            file_path = mp3_path
        else:
            return jsonify({"error": "Errore nella conversione del file"}), 500
 
    result = process_audio_file(file_path)
    return jsonify(result)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)