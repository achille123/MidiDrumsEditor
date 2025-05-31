FROM python:3.10

WORKDIR /app
COPY . /app

# 💡 Évite la barre riche de pip (qui cause les threads)
ENV PIP_NO_PROGRESS_BAR=off
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production


# ✅ Ajout de ce fallback : évite les threads (remplace 'rich' par 'legacy')
RUN pip config set global.progress_bar off

# 📦 Installation groupée sans mise à jour de pip
RUN pip install flask flask-cors librosa soundfile --no-cache-dir

EXPOSE 5001

CMD ["python", "app.py"]
