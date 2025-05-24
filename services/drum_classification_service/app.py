from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import os
import numpy as np
import json

app = Flask(__name__)
CORS(app)

# 📁 Chemin vers les fichiers audio déjà uploadés
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'uploads')

@app.route('/classify-drums', methods=['POST'])
def classify_drums():
    # ✅ Vérifie que les données attendues sont là
    data = request.get_json()
    if not data or 'filename' not in data or 'onsets' not in data:
        return jsonify({'error': 'Missing filename or onsets'}), 400

    filename = data['filename']
    onset_times = data['onsets']

    # 📄 Reconstitue le chemin du fichier déjà uploadé
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Audio file not found'}), 404

    # 🎧 Charge l'audio
    y, sr = librosa.load(filepath)

    result = []
    for t in onset_times:
        onset_sample = int(t * sr)
        start = max(0, onset_sample - int(0.05 * sr))
        end = min(len(y), onset_sample + int(0.05 * sr))
        segment = y[start:end]

        centroid = librosa.feature.spectral_centroid(y=segment, sr=sr)
        mean_centroid = np.mean(centroid)

        if mean_centroid < 1500:
            label = "kick"
        elif mean_centroid < 3000:
            label = "snare"
        else:
            label = "hat"

        velocity = np.random.randint(60, 100)

        result.append({
            "time": round(t, 3),
            "type": label,
            "velocity": velocity,
            "centroid": float(round(mean_centroid, 2))
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5004)
