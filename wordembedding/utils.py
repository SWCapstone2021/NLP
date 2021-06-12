import re

import kss
from konlpy.tag import Okt
from numpy import dot
from numpy.linalg import norm

from basefunction import json2list


def word_embedding(keyword, model):
    keyword_list = keyword.split(' ')
    wordset = []
    for searching_word in keyword_list:
        association_word = model.find_similar_words(searching_word)
        for words in association_word.values():
            for word in words:
                word = word.split(' (')[0]
                wordset = wordem_chk(searching_word, word, wordset)
    return set(wordset)


def kor_chk(word):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+').sub('', word)
    return len(hangul)


def wordem_chk(keyword, chkword, wordset):
    if keyword == chkword:
        return wordset

    if '분류:' in chkword:
        return wordset

    if kor_chk(chkword):
        wordset.append(chkword)
        return wordset

    return wordset


def cos_sim(word1, word2):
    return dot(word1, word2) / (norm(word1) * norm(word2))


def title_noun(title):
    okt = Okt()
    title_set = okt.nouns(title)

    return title_set


def script_noun(json_file):
    script = script_list2str(json_file)
    okt = Okt()
    NounResult = okt.nouns(script)

    return NounResult


def script_list2str(json_file):
    scriptfile = json2list(json_file)
    script_text = ''.join(scriptfile)
    return script_text


def word_set(noun_set):
    word_list = list()
    for word in noun_set:
        if word not in word_list:
            word_list.append(word)
    return word_list


def split_sentence(json_file):
    script = json2list(json_file)
    sentence_text = ''
    for line in script:
        for sent in kss.split_sentences(line):
            sent = sent + ' '
            sentence_text += sent
    return sentence_text
