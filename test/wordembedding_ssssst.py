import pytest

from pororo.tasks.sentence_embedding import PororoSBertSentence
from pororo.tasks.word_embedding import PororoWikipedia2Vec
from wordembedding import load_sc_model, load_wm_model, association_f, cosin_similar


@pytest.fixture(scope='session')
def sc_model():
    model = load_sc_model()
    return model


@pytest.fixture(scope='session')
def wm_model():
    model = load_wm_model()
    return model


def test_load_model(sc_model, wm_model):
    assert isinstance(sc_model, PororoSBertSentence)
    assert isinstance(wm_model, PororoWikipedia2Vec)


def test_association_f(example, wm_model):
    keyword = '백신'
    time_stamp = association_f(keyword, example.script, wm_model)

    assert len(time_stamp) > 0
    assert isinstance(time_stamp[0]['text'], str)
    assert isinstance(time_stamp[0]['start'], float)


def test_cosin_similar(example, sc_model):
    score = cosin_similar(example.title, example.script, sc_model)
    assert score >= 0
