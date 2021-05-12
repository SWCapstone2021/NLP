from pytube import YouTube
import youtube_dl
import os
import glob
from os.path import basename
from konlpy.tag import Mecab

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

def OnlyNoun(URL):
    with open(f'{YOUTUBE_REPO_PATH}/{ChkID(URL)}.ko.vtt','r', encoding='utf-8') as f:
        script = f.read()
    tagger = Mecab()
    ex1 = tagger.nouns(script)
    ex1
    