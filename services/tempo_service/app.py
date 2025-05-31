from flask import Flask, request, jsonify
from flask_cors import CORS
from tempo_analyzer import analyze_tempo
import os
import librosa
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

BASE_UPLOAD_FOLDER = os.path.abspath('static/uploads')

@app.route('/analyze-tempo', methods=['GET'])
def analyze_single_file():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Missing 'filename' parameter"}), 400

    safe_filename = secure_filename(filename)
    filepath = os.path.join(BASE_UPLOAD_FOLDER, safe_filename)

    if not os.path.isfile(filepath):
        return jsonify({"error": f"File '{safe_filename}' not found"}), 404

    try:
        print(f"🔍 Analyse du fichier : {filepath}")
        analysis = analyze_tempo(filepath)

        y, sr = librosa.load(filepath)
        duration = librosa.get_duration(y=y, sr=sr)

        analysis["duration"] = duration
        analysis["filename"] = safe_filename

        return jsonify(analysis)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
