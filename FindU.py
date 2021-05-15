from basefunction.FindUMethod import *
from pprint import pprint as pp
from STT import load_model, stt

if __name__ == "__main__":
    i = input("기능번호: 1(extract subtitle), 2(ctrl+F), 3(Frequency), 4(STT)")

    if i == '1':
        URL = input("URL:")
        MakeVttFile(URL)
    if i == '2':
        SearchingValue = input("키워드입력:")
        URL = input("URL:")
        Ctrl_F(SearchingValue, URL)
    if i == '3':
        SearchingValue = input("키워드입력:")
        URL = input("URL:")
        Frequency(SearchingValue, URL)

    if i == '4':
        print("Model loading... ", end='')
        model, vocab = load_model()
        print("Done")
        audio_path = 'STT/audio/full.wav'

        sentences = stt(model, vocab, audio_path)
        pp(sentences)
