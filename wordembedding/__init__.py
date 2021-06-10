from basefunction import ctrl_f
from pororo import Pororo
from wordembedding.utils import *
from operator import itemgetter


def association_f(keyword, json_file, model):
    TimeStamp = ctrl_f(keyword, json_file)
    time = list()
    for start in TimeStamp:
        time.append(start['start'])

    wordset = word_embedding(keyword, model)
    for word in wordset:
        for line in json_file:
            if word in line['text']:
               if line['start'] not in time:
                    TimeStamp.append(line)
                    time.append(line['start'])

    TimeStamp = sorted(TimeStamp, key=itemgetter('start'))
    return TimeStamp

def load_wm_model():
    model = Pororo("word2vec", lang="ko")
    return model


def load_sc_model():
    model = Pororo(task="sentence_embedding", lang="ko")
    return model


def cosin_similar(title, json_file, model):
    word1 = model(title)
    script = script_list2str(json_file)
    word2 = model(script)

    result = cos_sim(word1, word2)
    result = int(result * 10)
    return result
