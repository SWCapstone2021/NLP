import os
from glob import glob

from STT import load_model, stt
from pprint import pprint as pp
from basefunction.FindUMethod import MakeTXTFile

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

if __name__ == "__main__":
    ids = [os.path.basename(x)[:-4] for x in glob('data/true/*')]

    for id in ids:
        if not os.path.exists(f'data/audio/{id}.wav') or not os.path.exists(f'data/scripts/{id}.ko.vtt'):
            print(f"Make scripts about {id}")
            MakeTXTFile(f'https://www.youtube.com/watch?v={id}')

    print("Model loading... ")
    model, vocab = load_model()
    print("Done")

    for id in ids:
        audio_path = f'data/audio/{id}'

    sentences = stt(model, vocab, audio_path)
    pp(sentences)
