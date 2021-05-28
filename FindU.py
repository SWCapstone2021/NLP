#from STT import load_model, stt
from pprint import pprint as pp
from basefunction import ctrl_f
from wordembedding import association_f, load_model, cosin_similar, summary_script
import os
import json

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

with open("test_scripts.json", "r") as st_json:
    json_file = json.load(st_json)
# script = json2list(json_file)

if __name__ == "__main__":
    i = input("fucntion num:  2(ctrl+F), 3(reliability), 4(STT), 5(association), 6(summarization), 7(QA)")

    if i == '2':
        SearchingValue = input("keyword:")
        ctrl_f(SearchingValue, json_file)
    if i == '3':
        model = load_model()
        SearchingValue = input("keyword:")
        cosin_similar(SearchingValue, json_file, model)
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
        model = load_model()
        SearchingValue = input("keyword:")
        association_f(SearchingValue, json_file, model)

    if i == '6':
        summary_script(json_file)