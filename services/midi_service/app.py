from flask import Flask, request, send_file
from services.midi_service.midi_generator import process_audio_to_midi
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    file = request.files['audio']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    midi_path = process_audio_to_midi(filepath)
    return send_file(midi_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
