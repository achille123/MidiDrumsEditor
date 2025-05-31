import librosa

def analyze_tempo(filepath):
    y, sr = librosa.load(filepath)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return {
        "tempo": round(tempo[0], 2),
        "beats": [round(bt, 3) for bt in beat_times]
    }
