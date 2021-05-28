#from STT import load_model, stt
from pprint import pprint as pp
from basefunction.FindUMethod import *
from basefunction.initial import json2list

import os
import json

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

with open("test_scripts.json", "r") as st_json:
    json_file = json.load(st_json)
script = json2list(json_file)

if __name__ == "__main__":
    print(script)

    i = input("fucntion num:  2(ctrl+F), 3(reliability), 4(STT), 5(association), 6(summarization), 7(QA)")

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
        CosinSimilar(SearchingValue, URL)
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
    if i == '5':
        SearchingValue = input("keyword:")
        URL = input("URL:")
        WordEm_crtlF(SearchingValue,URL)

    if i == '6':
        URL = input("URL:")
        Summary(URL)