from operator import itemgetter

import fasttext
import fasttext.util

from basefunction import ctrl_f
from wordembedding.utils import *


def association_f(keyword, json_file, model):
    TimeStamp = ctrl_f(keyword, json_file)
    wordset = word_embedding(keyword, model)
    for word in wordset:
        for line in json_file:
            if word in line['text']:
                TimeStamp.append(line)

    TimeStamp = sorted(TimeStamp, key=itemgetter('time'))
    return TimeStamp


def load_wm_model():
    modelPath = 'wordembedding/dataset/cc.ko.300.bin'
    model = fasttext.load_model(modelPath)

    return model


def cosin_similar(keyword, json_file, model):
    onlyNoun = script_noun(json_file)
    mostwords = word_count(onlyNoun)

    result = 0
    for word in mostwords:
        result += cos_sim(model.get_word_vector(keyword), model.get_word_vector(word[0]))

    return result / (len(keyword) * len(mostwords))  # need to modify the keyword part


def summary_script(json_file):
    texts = split_sentence(json_file)

    my_tokenizer = okt_tokenizer()
    textRank = TextRank(my_tokenizer)

    summerized = textRank.summarize(texts, 0.1)

    result = list()
    for summerize_line in summerized:
        for line in json_file:
            if summerize_line == line["text"]:
                result.append(line)
                break

    return result
