from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)
CORS(app)

# ✅ Autoriser uniquement certains formats
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}

# 📁 Dossier racine vers static/uploads
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'filename' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['filename']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print(f"✅ Fichier sauvegardé dans : {filepath}")

    # ✅ Just return the filename, no orchestration
    return jsonify({
        'message': 'File uploaded successfully',
        'filename': filename
    })


if __name__ == '__main__':
    app.run(debug=True, port=5002)
