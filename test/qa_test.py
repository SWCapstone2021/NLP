import pytest

from QA.evaluate_v1_0 import exact_match_score, f1_score
from QA.infer import interest_of_test
from QA.my_squad_metrics import normalize_answer, get_tokens, _compute_softmax
from QA.utils import _is_whitespace


class Predict:
    def __init__(self, x):
        self.text = f"텍스트{x}"
        self.prob = x * 0.1

    def values(self):
        return self.text, self.prob, 0, 0


@pytest.fixture(scope='session')
def predictions():
    predict_list = [Predict(x) for x in range(1, 10)]
    return predict_list


@pytest.fixture(scope='session')
def predict_text():
    return '안녕하세요,,,! 저는 rhcsky 입니다. 잘 부탁드려요 ^^*'


@pytest.fixture(scope='session')
def true_text():
    return '안녕하세요 저는 rhcsky 입니다 잘 부탁드려요'


def test_exact_match_score():
    assert exact_match_score("동일값", "동일값")
    assert not exact_match_score("예측갑", "실제값")


def test_f1_score():
    assert f1_score("예측값", "동일값") > f1_score("연샌벡센", "얀셴백신")


def test_interest_of_test(predictions):
    res = interest_of_test(predictions)
    assert len(res) > 2


def test_normalize_answer(predict_text, true_text):
    ans = normalize_answer(predict_text)

    assert ans == true_text


def test_get_tokens(predict_text, true_text):
    ans = get_tokens(predict_text)

    assert len(ans) == 6
    assert ans == true_text.split()


def test_compute_softmax():
    scores = [1, 2, 3, 4]
    scores = _compute_softmax(scores)

    assert scores[0] < 0.033


def test_white_space():
    assert _is_whitespace(' ')
    assert _is_whitespace('\t')
    assert not _is_whitespace('a')
