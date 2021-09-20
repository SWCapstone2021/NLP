## FindU NLP

<p align="center">
    <img src="asset/logo-com.svg" alt="logo" width="250" height="250"/>
</p>
<h4 align="center">스크립트 기반 영상 검색 및 요약 서비스</h4>
<p align="center">
    <a href="https://github.com/SWCapstone2021/NLP/actions/workflows/deploy.yml">
        <img src="https://github.com/SWCapstone2021/NLP/actions/workflows/deploy.yml/badge.svg"/>
    </a> 
    <a href="https://github.com/SWCapstone2021/NLP/actions/workflows/pytest.yml">
        <img src="https://github.com/SWCapstone2021/NLP/actions/workflows/pytest.yml/badge.svg?branch=dev"/>
    </a>	
    <a href="https://github.com/SWCapstone2021/NLP/issues">
        <img src="https://img.shields.io/github/issues/SWCapstone2021/NLP"/>
    <a href="https://github.com/SWCapstone2021/NLP/issues">
        <img src="https://img.shields.io/github/issues-closed/SWCapstone2021/NLP?color=green"/>
    </a>
    <a href="https://github.com/SWCapstone2021/NLP/pulls">
        <img src="https://img.shields.io/github/forks/SWCapstone2021/NLP"/>
    </a>
    <a href="https://github.com/SWCapstone2021/NLP/stargazers">
        <img src="https://img.shields.io/github/stars/SWCapstone2021/NLP"/>
    </a>
    <a href="https://github.com/SWCapstone2021/NLP/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/SWCapstone2021/NLP"/>
    </a> <br/>
        <img src="https://img.shields.io/badge/python-3.8-3776AB?style=flat-square&logo=python"/>
        <img src="https://img.shields.io/badge/torch-1.8.1-EE4C2C?style=flat-square&logo=pytorch"/>

</p>

<p align="center">
  <a href="#website">Website</a></a> •   
  <a href="#Dependency">Dependency</a></a> • 
  <a href="#features">Features</a></a> • 
  <a href="#contributors">Contributors</a> • 
  <a href="#license">License</a> • 
  <a href="#reference">Reference</a>
</p>
<p align="center">
    본 프로젝트는 2021 Ajou University Spring SW Capston Design 과목의 일환으로 진행되었습니다. <br/>
    해당 repository는 찾아봐유의 <b>NLP</b> 소스코드를 저장하고 있습니다.
<br/>    
    상업적 목적을 띄고 있지 않으며, 팀 APC에 의해 개발되었습니다.
</p>
<p align="center">
    <b>2021년 한국디지털콘텐츠학회 대학생 논문경진대회 금상 수상</b>
</p>

## Website
Visit out website [FindU](https://apcfindu.web.app/) 😀

## Dependency

`FindU-NLP` is based on `torch=1.8.1(cuda 11.1)` and `python 3.8`

자세한 dependency는 [requirements](requirements.txt)를 참고하시기 바랍니다.

## Features

### STT

**찾아봐유**를 사용하기 위해서는 영상의 script가 필요하다. 하지만 유튜브에서는 script가 없는 영상이 많고 '자막 자동 생성 기능'이 있지만 한국어의 경우 제대로 자막 생성이 이루어지지 않아 ***한국어에 맞는 STT model을 제작***하여 사용하고자 한다.

|  |         |
| ------- | ------------- |
| Dataset | AIHub         |
| Model   | DeepSpeech2   |
| Period  | Iteration 1~3 |
| Model path | 'STT/models/ds2.pt' |

```python
from STT import load_stt_model, stt

stt_model, stt_vocab = load_stt_model()  # model과 vocab은 서버가 시작할 때 load
audio_path = 'your/audio_path/origin_audio.wav'

sentences = stt(stt_model, stt_vocab, audio_path)  # sentences는 list로 (시간, 자막)으로 구성
>> sentences[0] = (3.2, "번역된 자막이 출력됩니다.")
```

### Ctrl+F기능

해당 키워드가 동영상의 어떤 구간에 있는지 찾아준다. 
키워드를 입력하면 키워드가 속해있는 대사가 시작하는 시간을 리스트형식으로 return한다.

```python
from basefunction import ctrl_f

SearchingValue = input("keyword:")
timestamp = ctrl_f(SearchingValue, json_file) 
>>> ['00','00', ...]  #  SearchingValue의 영상 시작시간 return
```

### 신뢰도 기능

영상의 제목과 내용을 기반으로 얼마나 연관성이 높은지 수치로 보여준다. 제목 sentence vector와 내용 sentence vector를 cos-similarity로 계산하여 영상의 신뢰도기능을 제공한다. 신뢰도의 범위는 0~10이다.

```python
from wordembedding import cosin_similar

model = load_wm_model()  # word embedding model은 서버가 시작할 때  load
SearchingValue = input("keyword:")

score = cosin_similar(SearchingValue, json_file, model)
>>> 0.3
```

### word embedding + crtl_F 기능(association_f)

해당 키워드와 키워드의 연상단어가 동영상의 어떤 구간에 있는지 찾아준다. 

```python
from wordembedding import association_f

model = load_wm_model()  # word embedding model은 서버가 시작할 때  load
SearchingValue = input("keyword:")

association_f(SearchingValue, json_file, model)
>>> ['00','00', ...]   #  SearchingValue의 영상 타임스탬프와 SearchingValue의 연상단어가 해당하는 영상 타임스탬프 return
```

### QA System

사용자가 더 인간적인 질문을 던지고 이에 해당하는 답변을 찾을 수 있다.

|            |                      |
| ---------- | -------------------- |
| Dataset    | KoQuAD1.0, KoQuAD2.0 |
| Model      | bert-multilingual    |
| Period     | Iteration 20         |
| Model path | 'QA/models/*'        |

```python
from QA import load_qa_model, QA_system

qa_model, qa_tokenizer = load_qa_model()  # model과 tokenizer는 서버가 시작할 때 load

question = 'Your Question'
answers = QA_system(qa_model, qa_tokenizer, question, json_script)  # answers는 list로 (index, 답변)으로 구성, index는 해당 답변이 출현하는 script의 index
>> (index, "답변")
```

### Summarization

전체 스크립트의 3줄정도 분량을 요약해서 보여준다.

```python
from Summarization import load_sc_model, summary_script
from pororo import Pororo

summ_model = load_sc_model()
summarized_texts = summary_script(json_file, summ_model)
>>> "Text.Text.Text."
```


## Contributors

Maintainer : [남희수](https://github.com/HeesuNam), [오승민](https://github.com/Rhcsky)

Contributor : [강한결](https://github.com/hankyul2), [김수연](https://github.com/amelia9981), [허범수](https://github.com/xxoSoo)



## License

`FindU-NLP` project is [licensed](LICENSE) under the terms of **the Apache License 2.0**.



## Reference

[PORORO](https://github.com/kakaobrain/pororo)

[🤗transformers](https://github.com/huggingface/transformers)

