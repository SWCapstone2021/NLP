from pytube import YouTube
import youtube_dl
import os
from os.path import basename
from konlpy.tag import Mecab
from math import log
# -*- coding: utf-8 -*-
import fasttext
import fasttext.util
import re

YOUTUBE_REPO_PATH = '/home/seungmin/dmount/NLP/script'  # mount/NLP/script'

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
    for line in lines[5::3]:
        entire_text += line
    f.close()
    fw = open('%s.txt' % (SubtitleFile[:-4]), 'w')
    fw.write(entire_text)
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
    mecab = Mecab()
    NounResult = mecab.nouns(script)
    return NounResult


def Frequency(keyword, URL):
    OnlyNoun = ScriptNoun(URL)
    TF = 0
    KeywordList = KeyWordNoun(keyword)
    for noun in KeywordList:
        for word in OnlyNoun:
            if noun in word:
                TF += 1
    with open(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt', 'r', encoding='utf-8') as f:
        script = f.readlines()
    ILF = 1
    for line in script:
        if keyword in line:
            ILF += 1
    TF_IDF = TF * log(len(script) / ILF)
    return print(TF_IDF)
    # TF-IDF = TF * (log(N/df)) TF:단어 빈도수, N: 문장개수, IDF: 단어가 포함된 문장개수

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
    mecab = Mecab()
    KeywordResult = mecab.nouns(keyword)
    return KeywordResult