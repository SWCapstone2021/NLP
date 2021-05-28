from pytube import YouTube
import youtube_dl
import os
from os.path import basename
from konlpy.tag import Okt
# -*- coding: utf-8 -*-
import fasttext
import fasttext.util
import re
import numpy as np
import kss
import operator
from Summarization.textrankr2 import TextRank

YOUTUBE_REPO_PATH = '/home/heesu/mount/NLP/script'  # mount/NLP/script'

VttOption = {
    'skip_download': True,
    'writesubtitles': True,
    'subtitleslangs': ['ko'],
    'subtitlesformat': 'vtt',
    'nooverwrites': True,
    'outtmpl': 'script/%(id)s'
}

WavOption = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
    'nooverwrites': True,
    'outtmpl': 'script/%(id)s.wav'
}


def MakeFile(URL, option=VttOption):
    with youtube_dl.YoutubeDL(option) as ydl:
        ydl.download([URL])
        ChkFile(URL)

def ChkVttForm(SubtitleFile):
    f = open(SubtitleFile, 'r')
    lines = f.readlines()
    f.close()


def MakeVttForm(SubtitleFile):
    f = open(SubtitleFile, 'r')
    lines = f.readlines()
    f.close()
    fw = open(SubtitleFile,'w')
    for line in lines[:4]:
        fw.write(line)
    for idx, line in enumerate(lines[6::8]):
        skip = False
        time_stamp = True
        clean = ''
        time = ''
        for c in line:
            if c == '>':
                skip = False
                time_stamp = False
                continue

            if c == '<' or skip:
                if time_stamp and skip:
                    time += c
                skip = True
                continue

            clean += c
        if time_stamp:
            try:
                time = lines[(idx + 1) * 8].split(' ')[0]
            except:
                pass
        fw.write(f'{time}\n{clean}\n')
    fw.close()


def ChkFile(URL):
    if not os.path.exists(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'):
        VttOption['writeautomaticsub'] = True
        MakeFile(URL, option=VttOption)
        SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
        MakeVttForm(SubtitleFile)
        VttOption['writeautomaticsub'] = False
        MakeFile(URL, option=WavOption)


def MakeTXTFile(URL):
    SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
    f = open(SubtitleFile, 'r')
    lines = f.readlines()
    entire_text = ''
    for line in lines[5:]:
        if len(line)==0 or re.search('-->',line):
            continue
        line=line.rsplit('\n')[0]
        line = line + ' '
        entire_text += line
    f.close()
    fw = open('%s.txt' % (SubtitleFile[:-4]), 'w')
    fw.write(entire_text)
    fw.close()
    senteceTXT(URL)


def SplitBySentence(txtfile):
    sentence_text= ''
    lines = txtfile.readlines()
    for line in lines:
        for sent in kss.split_sentences(line):
            sent = sent + '\n'
            sentence_text += sent
    return sentence_text


def senteceTXT(URL):
    entire_text=''
    SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt'
    f = open(SubtitleFile, 'r')
    entire_text = SplitBySentence(f)
    fw = open(SubtitleFile,'w')
    fw.write(entire_text)
    f.close()
    fw.close()


def SplitBySentence(txtfile):
    sentence_text= ''
    lines = txtfile.readlines()
    for line in lines:
        for sent in kss.split_sentences(line):
            sent = sent + '\n'
            sentence_text += sent
    return sentence_text


def senteceTXT(URL):
    entire_text=''
    SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt'
    f = open(SubtitleFile, 'r')
    entire_text = SplitBySentence(f)
    fw = open(SubtitleFile,'w')
    fw.write(entire_text)
    f.close()
    fw.close()


def ChkID(URL):
    id = URL.rsplit('=', 1)[-1]
    return id


def Ctrl_F(keyword, URL):
    if not os.path.exists(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'):
        MakeFile(URL)
    SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
    TimeStamp = []
    with open(SubtitleFile) as f:
        lines = f.readlines()
        StartPoint = 3
        for line in lines[4:]:
            StartPoint += 1
            if keyword in line:
                PlaySection = lines[StartPoint - 1]
                # print(line + PlaySection) #확인용
                PlaySection = PlaySection.split(' ')[0]
                TimeStamp.append(PlaySection.split('\n')[0])
    # print(TimeStamp) #확인용
    return TimeStamp


def ChkTxtFile(URL):
    if not os.path.exists(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt'):
        MakeTXTFile(URL)


def ScriptNoun(URL):
    ChkTxtFile(URL)
    with open(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt', 'r', encoding='utf-8') as f:
        script = f.read()
    okt = Okt()
    NounResult = okt.nouns(script)
    return NounResult


def WordEm_crtlF(SearchingValue,URL):
    TimeStamp=[]
    TimeStamp=Ctrl_F(SearchingValue,URL)
    WordEmTimeStamp=[]
    wordset = WordEmbedding(SearchingValue)
    for word in wordset:
        WordEmTimeStamp=Ctrl_F(word,URL)
        if len(WordEmTimeStamp):
            for time in WordEmTimeStamp:
                TimeStamp.append(time)
    return TimeStamp

    
def WordEmbedding(SearchingValue):
    ModelPath = 'wordembedding/dataset/cc.ko.300.bin'
    Model = fasttext.load_model(ModelPath)
    wordset=[]
    for similiarity, word in Model.get_nearest_neighbors(SearchingValue,20):
        #print(f'{word}:{similiarity}')
        if SearchingValue not in word:
            if KorChk(word) :
                wordset=WordEmChk(word,wordset)
                if len(wordset)==5:
                    return wordset


def WordEmChk(word,wordset):
    if len(wordset) == 0:
        wordset.append(word)
        return wordset
    for index in wordset:
        if index not in word:
            wordset.append(word)
            return wordset       
        return wordset


def KorChk(word):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+').sub('',word)
    return len(hangul)


def KeyWordNoun(keyword):
    okt = Okt()
    KeywordResult = okt.nouns(keyword)
    return KeywordResult


def cos_sim(word1, word2):
    return dot(word1,word2)/(norm(word1)*norm(word2))


def CosinSimilar(keyword,URL):
    OnlyNoun = ScriptNoun(URL)
    WordCnt={}
    cnt=0
    for word in OnlyNoun:
        if word in WordCnt:
            cnt = WordCnt[word]
            WordCnt[word]= cnt+1
        else:
            WordCnt[word]=1
    mostwords = Sortcnt(WordCnt)
    result = 0
    KeywordList = KeyWordNoun(keyword)
    ModelPath = 'wordembedding/dataset/cc.ko.300.bin'
    Model = fasttext.load_model(ModelPath)
    for keyword in KeywordList:
        print(keyword)
        for word in mostwords:
            print(word)
            result += cos_sim(Model.get_word_vector(keyword),Model.get_word_vector(word[0]))
            print(result)
    return result / (len(KeywordList) * 5)


def Sortcnt(WordCnt):
    return sorted(WordCnt.items(), key=operator.itemgetter(1))[-5:]


class OktTokenizer:
    okt = Okt()

    def __call__(self, text):
        tokens = self.okt.pos(text)
        return tokens


def Summary(URL):
    ChkTxtFile(URL)
    SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt'
    texts = open(SubtitleFile, 'r').read()
    mytokenizer = OktTokenizer()

    tokens = mytokenizer(texts)
    textRank = TextRank(mytokenizer)

    summerized = textRank.summarize(texts, 0.1)

    return summerized

