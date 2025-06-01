from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import os
import numpy as np
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'uploads'))

ONSET_SERVICE_URL = "http://localhost:5003/detect-onsets"

@app.route('/classify-drums', methods=['POST'])
def classify_drums():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'Missing filename'}), 400

    safe_filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Audio file not found'}), 404

    # 🛰 Appel au microservice /detect-onsets
    try:
        onset_response = requests.get(ONSET_SERVICE_URL, params={"filename": filename})
        if onset_response.status_code != 200:
            return jsonify({'error': 'Failed to get onsets', 'details': onset_response.text}), 502
        onset_data = onset_response.json()
        onset_times = onset_data.get("onsets", [])
    except Exception as e:
        return jsonify({'error': f'Onset service call failed: {str(e)}'}), 500

    # 🎧 Analyse des segments
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
