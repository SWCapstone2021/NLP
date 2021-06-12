import pytest

from Summarization import load_summ_model, summary_script
from pororo.tasks.text_summarization import PororoRobertaSummary


@pytest.fixture(scope='session')
def summ_model():
    model = load_summ_model()
    return model


def test_load_model(summ_model):
    assert isinstance(summ_model, PororoRobertaSummary)


def test_summary_script(example, summ_model):
    text = summary_script(example.script, summ_model)

    assert isinstance(text, str)
    assert len(text) > 0
