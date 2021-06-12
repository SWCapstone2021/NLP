import json
import urllib
from urllib.parse import urlparse

import pytest
from youtube_transcript_api import YouTubeTranscriptApi


class Example:
    def __init__(self):
        self.id = '4puc2Ox9_vc'
        self.questions = ['얀센 백신의 장점은?', '얀센 백신은 몇 명분?']
        self.answers = list()
        self.score = 0
        self.summary = ''
        self.script = self.download_script()
        self.title, self.author = self.load_title()

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


@pytest.fixture(scope='session')
def example():
    example = Example()
    return example
