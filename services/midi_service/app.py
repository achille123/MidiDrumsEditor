from flask import Flask, request, send_file
from flask_cors import CORS
from services.midi_service.midi_generator import process_audio_to_midi
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    print("🎵 Requête reçue !")

    if 'audio' not in request.files:
        print("❌ Aucun fichier 'audio' reçu")
        return "No file part", 400

    file = request.files['audio']
    if file.filename == '':
        print("❌ Fichier sans nom")
        return "No selected file", 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    print(f"💾 Sauvegarde dans : {filepath}")

    midi_path = process_audio_to_midi(filepath)
    return send_file(midi_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


