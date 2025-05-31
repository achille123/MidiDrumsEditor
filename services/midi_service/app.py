from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from midi_generator import process_audio_to_midi
import os

app = Flask(__name__)
CORS(app)

# 📁 Dossier contenant les fichiers audio déjà uploadés
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'uploads')

@app.route('/generate-midi', methods=['POST'])
def generate_midi():
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'error': 'Missing filename'}), 400

    filename = data['filename']
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({'error': f'File not found: {filename}'}), 404

    print(f"🎧 Génération MIDI depuis : {filepath}")
    midi_path = process_audio_to_midi(filepath)
    print(f"🎼 MIDI généré : {midi_path}")

    return send_file(midi_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
