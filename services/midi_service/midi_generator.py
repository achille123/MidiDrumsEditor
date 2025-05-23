import librosa
import mido
from mido import MidiFile, MidiTrack, Message
import os

def process_audio_to_midi(filepath):
    y, sr = librosa.load(filepath)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    for time in onset_times:
        tick = int(time * 480)
        track.append(Message('note_on', note=36, velocity=100, time=tick))
        track.append(Message('note_off', note=36, velocity=0, time=50))

    midi_path = filepath.replace('.wav', '.mid')
    midi.save(midi_path)
    return midi_path
