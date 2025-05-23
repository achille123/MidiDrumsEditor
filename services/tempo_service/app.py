from flask import Flask, request, jsonify
from flask_cors import CORS
from tempo_analyzer import analyze_tempo
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/analyze-tempo', methods=['POST'])
def analyze():
    if 'audio' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['audio']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    print(f"📥 Fichier reçu : {filepath}")
    result = analyze_tempo(filepath)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)

