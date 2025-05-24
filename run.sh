#!/bin/bash

kill -9 $(lsof -ti :5000 -sTCP:LISTEN)
kill -9 $(lsof -ti :5001 -sTCP:LISTEN)
kill -9 $(lsof -ti :5002 -sTCP:LISTEN)
kill -9 $(lsof -ti :5003 -sTCP:LISTEN)
kill -9 $(lsof -ti :5004 -sTCP:LISTEN)

export PYTHONPATH=$(pwd)

echo "🚀 Lancement de tempo_service (port 5001)"
python services/tempo_service/app.py &

echo "🚀 Lancement de midi_service (port 5000)"
python services/midi_service/app.py &

echo "🚀 Lancement de upload_service (port 5002)"
python services/upload_service/app.py &

echo "🚀 Lancement de onset_service (port 5003)"
python services/onset_service/app.py &

echo "🚀 Lancement de drum_classification_service (port 5004)"
python services/drum_classification_service/app.py

echo "✅ Tous les services sont lancés"
