import pytest

from basefunction import ctrl_f


@pytest.fixture
def input_keyword():
    return "얀센"


def is_empty(*items):
    for item in items:
        if len(item) == 0:
            return False

    return True


def test_get_script(example):
    assert is_empty([example.script, example.title, example.author, example.questions])


def test_ctrl_f(example, input_keyword):
    SearchingValue = input_keyword
    result_script = ctrl_f(SearchingValue, example.script)

    assert len(result_script) == 13
