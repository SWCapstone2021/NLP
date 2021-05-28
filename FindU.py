from STT import load_model, stt

from basefunction.FindUMethod import *

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

# with open("test_scripts.json", "r") as st_json:
#     json_file = json.load(st_json)

if __name__ == "__main__":
    i = input("function num:  2(ctrl+F), 3(reliability), 4(STT), 5(association), 6(summarization), 7(QA)")

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

    if i == '4':
        print("Model loading... ")
        model, vocab = load_model()
        print("Done")

        audio_path = 'data/origin_audio/2YD2p24EKb4.wav'

        sentences = stt(model, vocab, audio_path)
        # from pprint import pprint as pp
        # pp(sentences)

    if i == '5':
        SearchingValue = input("keyword:")
        URL = input("URL:")
        WordEm_crtlF(SearchingValue, URL)

    if i == '6':
        URL = input("URL:")
        Summary(URL)
