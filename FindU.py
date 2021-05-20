#from STT import load_model, stt
from pprint import pprint as pp
from basefunction.FindUMethod import *

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

if __name__ == "__main__":
    i = input("fucntion num: 1(extract subtitle), 2(ctrl+F), 3(Frequency), 4(Check stt performance)")

    if i == '1':
        URL = input("URL:")
        MakeFile(URL)
    if i == '2':
        SearchingValue = input("keyword:")
        URL = input("URL:")
        Ctrl_F(SearchingValue, URL)
    if i == '3':
        SearchingValue = input("keyword:")
        URL = input("URL:")
        Frequency(SearchingValue, URL)
    """
    if i == '4':
        # no db ins
        print("Model loading... ")
        model, vocab = load_model()
        print("Done")

        audio_path = 'STT/data/origin_audio/full.wav'

        sentences = stt(model, vocab, audio_path)
        pp(sentences)
        """
