import os
import json
from pprint import pprint as pp

from basefunction import ctrl_f
from wordembedding import association_f, load_wm_model, cosin_similar, summary_script
from QA import load_qa_model, QA_system
from STT import load_stt_model, stt

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

with open("test_scripts.json", "r") as st_json:
    json_file = json.load(st_json)
# script = json2list(json_file)

if __name__ == "__main__":
    i = input("fucntion num:  1(ctrl+F), 2(reliability), 3(STT), 4(association), 5(summarization), 6(QA)")

    if i == '1':
        SearchingValue = input("keyword:")
        timestamp = ctrl_f(SearchingValue, json_file)

    if i == '2':
        model = load_wm_model()
        SearchingValue = input("keyword:")
        score = cosin_similar(SearchingValue, json_file, model)

    if i == '3':
        print("Load model...", end='')
        stt_model, stt_vocab = load_stt_model()
        print("done")

        audio_path = 'data/origin_audio/2YD2p24EKb4.wav'

        sentences = stt(stt_model, stt_vocab, audio_path)
        # pp(sentences)

    if i == '4':
        model = load_wm_model()
        SearchingValue = input("keyword:")
        timestamp = association_f(SearchingValue, json_file, model)

    if i == '5':
        summarized_text = summary_script(json_file)
        pp(summarized_text)


    if i == '6':
        print("Load model...", end='')
        qa_model, qa_tokenizer = load_qa_model()
        print("done")

        question = '개방적인 곳은?'
        answers = QA_system(qa_model, qa_tokenizer, question, json_file)
        # pp(answers)


