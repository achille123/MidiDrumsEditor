from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.errorhandler(500)
def handle_500(e):
    return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/process-audio", methods=["POST", "OPTIONS"])
def process_audio():
    if request.method == "OPTIONS":
        return '', 200

    try:
        data = request.get_json()
        filename = data.get("filename")
        print("📥 Received filename:", filename)

        if not filename:
            print("❌ No filename in request")
            return jsonify({"error": "Missing filename"}), 400

        filepath = os.path.join("static/uploads", filename)
        print("📂 Filepath resolved:", filepath)

        # 🥁 Onset Detection
        try:
            with open(filepath, "rb") as f:
                print("📨 Sending to onset service...")
                onset_res = requests.post("http://127.0.0.1:5003/detect-onsets", files={"audio": f})
        except Exception as e:
            print("❌ File open or request failed:", e)
            return jsonify({"error": "File open or onset call failed", "details": str(e)}), 500

        if onset_res.status_code != 200:
            print("❌ Onset service returned error:", onset_res.status_code)
            return jsonify({"error": "Onset detection failed"}), 500

        onset_data = onset_res.json()
        print("✅ Onset data received")

        # 🧠 Classification
        classify_res = requests.post("http://127.0.0.1:5004/classify-drums", json={
            "filename": filename,
            "onsets": onset_data["onsets"]
        })
        if classify_res.status_code != 200:
            print("❌ Drum classification failed")
            return jsonify({"error": "Drum classification failed"}), 500
        pattern = classify_res.json()
        print("✅ Classification result received")

        # 🎼 MIDI
        midi_res = requests.post("http://127.0.0.1:5000/generate-midi", json={
            "filename": filename,
            "pattern": pattern
        })
        if midi_res.status_code != 200:
            print("❌ MIDI generation failed")
            return jsonify({"error": "MIDI generation failed"}), 500

        print("✅ MIDI generation successful")
        return jsonify({"message": "MIDI generated", "filename": filename, "classification": pattern})

    except Exception as e:
        print("❌ General error in /process-audio:", e)
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5010)
