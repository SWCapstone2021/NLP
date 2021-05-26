from textrankr2 import TextRank
from pprint import pprint as pp

from konlpy.tag import Okt, Mecab

class OktTokenizer:
    okt = Mecab()

    def __call__(self, text):
        tokens = self.okt.pos(text)
        return tokens

text = open('../script/GZJornwzM_k.ko.txt','r').read()


# 1. init
mytokenizer = OktTokenizer()

tokens = mytokenizer(text)

textrank: TextRank = TextRank(mytokenizer)

# 2. summarize (like, pre-computation)
summerized = textrank.summarize(text, 0.1)

pp(summerized)