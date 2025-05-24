from flask import Flask, request, jsonify       # Flask pour l’API, request pour accéder aux fichiers envoyés, jsonify pour renvoyer une réponse JSON
from flask_cors import CORS                     # CORS pour autoriser les appels entre frontend et backend
import librosa                                  # Librosa pour le traitement audio
import os

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin (utile pour le frontend JS)

# Définition de l'endpoint POST /detect-onsets
@app.route('/detect-onsets', methods=['POST'])
def detect_onsets():
    # Vérifie si le fichier audio est bien inclus dans la requête
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio provided'}), 400

    # Récupère le fichier et son nom
    audio = request.files['audio']
    filename = audio.filename

    # Définit un chemin temporaire pour sauvegarder le fichier
    filepath = os.path.join('/tmp', filename)
    audio.save(filepath)

    # Charge le fichier audio avec librosa
    y, sr = librosa.load(filepath)

    # Détecte les onsets (déclenchements rythmiques)
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')

    # Calcule la durée totale du fichier audio
    duration = librosa.get_duration(y=y, sr=sr)

    # Retourne les onsets et la durée en JSON
    return jsonify({
        'duration': duration,
        'onsets': onsets.tolist()
    })

# Lance le service Flask sur le port 5003
if __name__ == '__main__':
    app.run(debug=True, port=5003)
