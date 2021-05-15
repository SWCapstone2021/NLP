from pytube import YouTube
import youtube_dl
import os
import glob
from os.path import basename
from konlpy.tag import Mecab
from math import log

YOUTUBE_REPO_PATH = '/home/heesu/mount/NLP/script'

def MakeVttFile(URL,auto_sub=False):
  DownOption = {
    'skip_download': True,
    'writesubtitles' : True,
    'writeautomaticsub' : auto_sub,
    'subtitleslangs':['ko'],
    'subtitlesformat': 'vtt',
    'nooverwrites':True,
    'outtmpl' : 'script/%(id)s'
  }
  with youtube_dl.YoutubeDL(DownOption) as ydl:
    ydl.download([URL])
    ChkFile(URL)

def ChkFile(URL):
    if not os.path.exists(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'):
        MakeVttFile(URL, auto_sub=True)
        SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
        f = open(SubtitleFile, 'r')
        lines = f.readlines()
        f.close()
        fw = open(SubtitleFile, 'w')
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
                    time=lines[(idx+1)*8].split(' ')[0]
                except:
                    pass
            fw.write(f'{time}\n{clean}\n')
        fw.close()

def MakeTXTFile(URL):
    SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
    f = open(SubtitleFile, 'r')
    lines = f.readlines()
    entire_text=''
    for line in lines[5::3]:
        entire_text += line
    f.close()
    fw = open('%s.txt'%(SubtitleFile[:-4]), 'w')
    fw.write(entire_text)
    fw.close()

def ChkID(URL):
    id = URL.rsplit('/',1)[-1]
    return id

def Ctrl_F(keyword,URL):
    SubtitleFile = f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt'
    TimeStamp=[]
    with open(SubtitleFile) as f:
        lines = f.readlines()
        StartPoint = 3
        for line in lines[4:]:
            StartPoint += 1
            if keyword in line:
                PlaySection = lines[StartPoint-1]
                #print(line + PlaySection) #확인용
                PlaySection = PlaySection.split(' ')[0]
                TimeStamp.append(PlaySection.split('\n')[0])
    #print(TimeStamp) #확인용
    return TimeStamp  

def ChkTxtFile(URL):
    if not os.path.exists(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt'):
        MakeTXTFile(URL)

def Noun(URL):
    ChkTxtFile(URL)
    with open(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt','r', encoding='utf-8') as f:
        script = f.read()
    mecab = Mecab()
    NounResult = mecab.nouns(script)
    return NounResult

def Frequency(keyword,URL):
    OnlyNoun=Noun(URL)
    TF=0
    for word in OnlyNoun:
        if keyword in word:
            TF+=1
    with open(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.txt','r', encoding='utf-8') as f:
        script = f.readlines()
    ILF = 0
    for line in script:
        if keyword in line:
            ILF += 1
    TF_IDF = TF * log(len(script) / ILF)
    return print(TF_IDF)
    #TF-IDF = TF * (log(N/df)) TF:단어 빈도수, N: 문장개수, IDF: 단어가 포함된 문장개수

