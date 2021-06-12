import json
import os
import time
import urllib
from urllib.parse import urlparse

from youtube_transcript_api import YouTubeTranscriptApi

from QA import load_qa_model
from Summarization import load_summ_model
from wordembedding import *

os.environ["CUDA_VISIBLE_DEVICES"] = "2"


class Example:
    def __init__(self, id, questions):
        self.id = id
        self.questions = questions
        self.answers = list()
        self.score = 0
        self.summary = ''
        self.script = self.load_script()
        self.title, self.author = self.load_title()

    def load_script(self):
        file_path = f"survey_script/{id}.json"
        if not os.path.exists(file_path):
            script = self.download_script()
            return script

        with open(file_path, 'r') as f:
            script = json.load(f)

        return script

    def download_script(self):
        transcript = YouTubeTranscriptApi.get_transcripts([self.id], languages=['ko'])

        transcript = transcript[0]
        sub = transcript[self.id]
        for x in sub:
            x.pop('duration', None)

        return sub

    def load_title(self):
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % self.id}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())

        return [data['title'], data['author_name']]

    def __str__(self):
        return f"author: {self.author}\ntitle: {self.title}\nsub: {self.script}\nquestion: {self.questions}"


def load_models():
    wm_model = load_wm_model()
    qa_model, qa_tokenizer = load_qa_model()
    summ_model = load_summ_model()
    sc_model = load_sc_model()

    return [wm_model, qa_model, qa_tokenizer, summ_model, sc_model]


if __name__ == "__main__":
    wm_model, qa_model, qa_tokenizer, summ_model, sc_model = load_models()

    ids = ['0iOspqjA83g', 'vrAH1jfj3bU', 'FisxKZHJU18', '4puc2Ox9_vc', 'oPJ7d3Yvh88']

    examples = list(map(lambda x: Example(x, []), ids))

    start = time.time()
    for e in examples:
        e.score = cosin_similar(e.title, e.script, sc_model)
        e.summary = summary_script(e.script, summ_model)

    print(f"running time: {time.time() - start}")

    for e in examples:
        print('=' * 10)
        print(f'https://www.youtube.com/watch?v={e.id}')
        print(e.title)
        print(e.score)
        print('summary: ', e.summary)
