from pytube import YouTube
import youtube_dl
import os
import glob
from os.path import basename

YOUTUBE_REPO_PATH = '/home/heesu/mount/NLP/script'

def MakeVttFile(URL):
  downOption = {
    'skip_download': True,
    'writesubtitles' : True,
    'writeautomaticsub' : True ,
    'subtitleslangs':['ko'],
    'subtitlesformat': 'vtt',
    'nooverwrites':True,
    'outtmpl' : 'script/%(id)s'
  }
  with youtube_dl.YoutubeDL(downOption) as ydl:
      ydl.download([URL])

def ChkID(URL):
    id = URL.rsplit('/',1)[-1]
    return id

def SelectFile(URL):
    ID=ChkID(URL)
    sub_file_list = glob.glob(os.path.join(YOUTUBE_REPO_PATH,'*.vtt'))
    sub_file_list = map(lambda x:os.path.join(YOUTUBE_REPO_PATH,x),sub_file_list)

    for sub_file in sub_file_list:
        FileName = basename(sub_file)
        SubtitleFile = FileName.split('.')[0]
        if(ID==SubtitleFile):
            return sub_file
    MakeVttFile(URL)
    return YOUTUBE_REPO_PATH + '/' + ID + '.ko.vtt'

def Ctrl_F(keyword,URL):
    SubtitleFile1 = SelectFile(URL)
    TimeStamp=[]
    with open(SubtitleFile1) as f:
        lines = f.readlines()
        StartPoint = 0
        for line in lines:
            StartPoint += 1
            if keyword in line:
                PlaySection = lines[StartPoint-2]
                #print(line + PlaySection) 확인용
                TimeStamp.append(PlaySection.split(' ')[0])
    return TimeStamp 
                