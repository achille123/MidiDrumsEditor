from flask import Flask, request, jsonify
from flask_cors import CORS
from tempo_analyzer import analyze_tempo
import os
import librosa  # 📦 pour calculer la durée audio

app = Flask(__name__)
CORS(app)

# 📁 Dossier temporaire pour stocker les fichiers audio uploadés
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/analyze-tempo', methods=['POST'])
def analyze():
    # 🔒 Vérifie qu'un fichier audio a bien été envoyé
    if 'audio' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # 📥 Récupère le fichier et sauvegarde temporairement
    file = request.files['audio']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    print(f"📥 Fichier reçu : {filepath}")

    # 🎼 Analyse du tempo
    result = analyze_tempo(filepath)

    # ⏱️ Calcul de la durée du fichier audio
    y, sr = librosa.load(filepath)
    duration = librosa.get_duration(y=y, sr=sr)

    # 👌 Ajoute la durée dans la réponse
    result["duration"] = duration

    return jsonify(result)

# 🚀 Lancement de l'application sur le port 5001
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)
