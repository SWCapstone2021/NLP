import json
import os

from QA import load_qa_model, QA_system
from STT import load_stt_model, stt
from basefunction import ctrl_f
from wordembedding import association_f, load_wm_model, summary_script, cosin_similar

# from pprint import pprint as pp

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

with open("test_scripts.json", "r") as st_json:
    json_file = json.load(st_json)
# script = json2list(json_file)

if __name__ == "__main__":
    i = input("fucntion num:  1(ctrl+F), 2(reliability), 3(STT), 4(association), 5(summarization), 6(QA)")

    if i == '1':
        SearchingValue = input("keyword:")
        result_script = ctrl_f(SearchingValue, json_file)
        # pp(result_script[:5])

    if i == '2':
        wm_model = load_wm_model()
        SearchingValue = input("keyword:")
        score = cosin_similar(SearchingValue, json_file, wm_model)
 
    if i == '3':
        print("Load model...", end='')
        stt_model, stt_vocab = load_stt_model()
        print("done")

        audio_path = 'data/origin_audio/2YD2p24EKb4.wav'

        sentences = stt(stt_model, stt_vocab, audio_path)
        # pp(sentences[:5])

    if i == '4':
        wm_model = load_wm_model()
        SearchingValue = input("keyword:")
        result_script = association_f(SearchingValue, json_file, wm_model)
        # pp(result_script[:5])

    if i == '5':
        result_script = summary_script(json_file)
        # pp(result_script[:5])


    if i == '6':
        print("Load model...", end='')
        qa_model, qa_tokenizer = load_qa_model()
        print("done")

        question = '이혼한 날'
        answers = QA_system(qa_model, qa_tokenizer, question, json_file)
        # pp(answers[:5)

