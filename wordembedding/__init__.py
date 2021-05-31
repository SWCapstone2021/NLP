from basefunction import ctrl_f, json2list
from wordembedding.utils import *
import fasttext
import fasttext.util

def association_f(keyword, json_file, model):
    TimeStamp=[]
    TimeStamp = ctrl_f(keyword,json_file)
    wordset = word_embedding(keyword, model)
    for word in wordset:
        for line in json_file:
            if word in line['text']:
                TimeStamp.append(line['time'])
    
    TimeStamp = sorted(TimeStamp)
    return TimeStamp


def load_wm_model():
    modelPath = 'wordembedding/dataset/cc.ko.300.bin'
    model = fasttext.load_model(modelPath)

    return model


def cosin_similar(title, json_file, model):
    only_script_noun = script_noun(json_file)
    only_title_noun = title_noun(title)
    script_mostwords=word_count(only_script_noun)

    result = 0
    for keyword in only_title_noun:
        for word in script_mostwords:
            result += cos_sim(model.get_word_vector(keyword),model.get_word_vector(word[0]))

    return result / (len(only_title_noun) * len(script_mostwords)) 



def summary_script(json_file):
    texts = split_sentence(json_file) 
    
    my_tokenizer = okt_tokenizer()
    tokens = my_tokenizer(texts)
    textRank = TextRank(my_tokenizer)
    
    summerized = textRank.summarize(texts, 0.1)

    return summerized
