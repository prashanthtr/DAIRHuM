import tensorflow as tf
import os
import librosa
import numpy as np
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

def load_audio(track):
    audio, sr = librosa.load(track, sr=16000)
    return audio

#wavenet encode
def get_embeddings(audio):
    encoding = fastgen.encode(audio, 'src/wavenet-ckpt/model.ckpt-200000', audio.shape[0])
    return encoding
# should be as long as number of tracks

# Store embedings with from and to path 
def store_embeddings(read_path,out_path):

    arr = os.listdir(read_path)

    if not os.path.exists(out_path): 
        os.makedirs(out_path) 

    for track in arr:
        encoding = get_embeddings(load_audio(os.path.join(read_path,track)))
        print("Embedding for ",track)
        np.save(os.path.join(out_path, track.split(".wav")[0] +'.npy'), encoding)
