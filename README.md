# FindU NLP
이 프로젝트는 2021 Ajou University Spring SW capstone design 과목의 일환으로 진행되었습니다.

해당 repository는 찾아봐유의 **NLP** 소스코드를 저장하고 있습니다. 



## Features

### STT

**찾아봐유**를 사용하기 위해서는 영상의 script가 필요하다. 하지만 유튜브에서는 script가 없는 영상이 많고 '자막 자동 생성 기능'이 있지만 한국어의 경우 제대로 자막 생성이 이루어지지 않아 ***한국어에 맞는 STT model을 제작***하여 사용하고자 한다.

Dataset : ClovaCall, AIHub

Model : [ClovaCall](https://github.com/clovaai/ClovaCall)

Period : Iteration 1~3

### script 추출하기
from basefunction.FindUMethod import MakeVttFile를 선언하고  MakeVttFile 메소드를 사용하여 script를 추출할 수 있다. 파라미터로는 원하는 동영상의 URL를 넣어주면 된다. script의 첫 3줄은
"WEBVTT
Kind: captions
Language: ko"이다.
5번째 줄부터 해당 동영상의 내용과 시간이 적혀져 있다. 
1. 동영상 업로더가 직접 script를 제공한 경우
"시작 구간 --> 종료 구간\n대사\n\n"형식으로 구성되어 있다.
2. 유튜브에서 자동생성한  script인 경우
"시작 구간\n대사\n\n"형식으로 구성되어 있다.

### Ctrl+F 기능
from basefunction.FindUMethod import Ctrl_F를 선언하고 Ctrl_F 메소드를 사용하여 검색한 키워드가 포함된 동영상 구간을 찾아준다. 파라미터로는 키워드, 동영상의 URL순이다.  찾고자하는 키워드가 포함된 시작 구간들을 리스트로 return하며 각 시간은 00:00:00.00형식으로 되어있다.

### Word Embedding

### QA System

### Summarization



## Contributor

Maintainer : 남희수, 오승민

Contributor : 강한결, 김수연, 허범수



## License

MIT License