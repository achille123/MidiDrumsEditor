from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import librosa
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

BASE_UPLOAD_FOLDER = os.path.abspath('static/uploads')

@app.route('/detect-onsets', methods=['GET'])
def detect_onsets():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Missing 'filename' parameter"}), 400

    safe_filename = secure_filename(filename)
    filepath = os.path.join(BASE_UPLOAD_FOLDER, safe_filename)

    if not os.path.isfile(filepath):
        return jsonify({"error": f"File '{safe_filename}' not found"}), 404

    try:
        y, sr = librosa.load(filepath)
        onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
        duration = librosa.get_duration(y=y, sr=sr)

        return jsonify({
            'duration': duration,
            'onsets': onsets.tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
