from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import os
from pydub import AudioSegment
import tempfile

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin (utile pour le frontend JS)

# Définition de l'endpoint POST /detect-onsets
@app.route('/detect-onsets', methods=['POST'])
def detect_onsets():
    print("📡 Requête reçue par onset_service")
    print("📡 Fichier recu:",request.files.get("audio"))

    # Vérifie si le fichier audio est bien inclus dans la requête
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio provided'}), 400

    # Récupère le fichier et son nom
    audio = request.files['audio']
    filename = audio.filename

    # Définit un chemin temporaire pour sauvegarder le fichier
    filepath = os.path.join('/tmp', filename)
    audio.save(filepath)

    # 🔄 Convertit en WAV si c'est un fichier MP3
    if filepath.endswith('.mp3'):
        try:
            audio_seg = AudioSegment.from_file(filepath, format="mp3")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                audio_seg.export(tmpfile.name, format="wav")
                filepath = tmpfile.name  # Met à jour le chemin pour librosa
        except Exception as e:
            return jsonify({'error': f'Conversion MP3 failed: {str(e)}'}), 500

    # 📥 Charge le fichier audio avec librosa
    y, sr = librosa.load(filepath)

    # 🥁 Détecte les onsets (déclenchements rythmiques)
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    print("📡 Onsets détectés onset_service")


    # ⏱️ Calcule la durée totale du fichier audio
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"✅ Duration du fichier: {duration}")
    print(f"✅ Liste des onsets: {onsets.tolist()}")
    # ✅ Retourne les onsets et la durée en JSON
    return jsonify({
        'duration': duration,
        'onsets': onsets.tolist()
    })

# 🚀 Lancement du service Flask
if __name__ == '__main__':
    app.run(debug=True, port=5003)
