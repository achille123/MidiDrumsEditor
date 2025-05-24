import os
import librosa
import mido
from mido import MidiFile, MidiTrack, Message
from datetime import datetime

def process_audio_to_midi(filepath):
    y, sr = librosa.load(filepath)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    ticks_per_beat = mid.ticks_per_beat
    time_per_beat = 60 / tempo
    ticks_per_second = ticks_per_beat / time_per_beat

    last_tick = 0
    for onset in onsets:
        tick = int(onset * ticks_per_second)
        delta = tick - last_tick
        last_tick = tick

        track.append(Message('note_on', note=36, velocity=100, time=delta))  # Kick
        track.append(Message('note_off', note=36, velocity=0, time=50))

    # Nom de fichier basé sur l'heure
    filename = f"drums_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, '..', '..', 'static', 'midi', filename)
    output_path = os.path.abspath(output_path)
    mid.save(output_path)
    return output_path
