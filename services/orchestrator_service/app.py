from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/process-audio", methods=["POST"])
def process_audio():
    data = request.json
    filename = data.get("filename")
    if not filename:
        return jsonify({"error": "Missing filename"}), 400

    filepath = os.path.join("static/uploads", filename)

    # 🥁 1. Appel onset_service
    with open(filepath, "rb") as f:
        onset_res = requests.post("http://localhost:5003/detect-onsets", files={"audio": f})
    if onset_res.status_code != 200:
        return jsonify({"error": "Onset detection failed"}), 500
    onset_data = onset_res.json()

    # 🧠 2. Appel classification
    classify_res = requests.post("http://localhost:5004/classify-drums", json={
        "filename": filename,
        "onsets": onset_data["onsets"]
    })
    if classify_res.status_code != 200:
        return jsonify({"error": "Drum classification failed"}), 500
    pattern = classify_res.json()

    # 🎼 3. Appel MIDI
    midi_res = requests.post("http://localhost:5000/generate-midi", json={
        "filename": filename,
        "pattern": pattern
    })
    if midi_res.status_code != 200:
        return jsonify({"error": "MIDI generation failed"}), 500

    return jsonify({"message": "MIDI generated", "filename": filename})

if __name__ == "__main__":
    app.run(port=5010)
