import os
import time
import argparse
from elevenlabs.client import ElevenLabs

def convert_audio_to_text(api_key, input_folder, output_folder):
    client = ElevenLabs(api_key=api_key)
    os.makedirs(output_folder, exist_ok=True)
    
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg'}
    
    while True:
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file_path)
                if ext.lower() in audio_extensions:
                    process_audio_file(client, file_path, output_folder)
        time.sleep(5)  # Controlla nuovi file ogni 5 secondi

def process_audio_file(client, file_path, output_folder):
    try:
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{name_without_ext}.txt")

        if os.path.exists(output_path):  # Evita di rielaborare file già convertiti
            return

        print(f"Convertendo {filename}...")

        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()

        if not audio_data:
            print(f"Errore: Il file {file_path} è vuoto")
            return

        response = client.speech_to_text.convert(file=audio_data, model_id="scribe_v1",language_code="it")
        
        with open(output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(response.text)

        print(f"Conversione completata: {output_path}")

    except Exception as e:
        print(f"Errore con il file {file_path}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conversione audio in testo con ElevenLabs")
    parser.add_argument("--api-key", required=True, help="API key di ElevenLabs")
    parser.add_argument("--input-folder", default="./audio_input", help="Cartella con i file audio")
    parser.add_argument("--output-folder", default="./text_output", help="Cartella dove salvare il testo")
    args = parser.parse_args()

    os.makedirs(args.input_folder, exist_ok=True)
    convert_audio_to_text(args.api_key, args.input_folder, args.output_folder)
