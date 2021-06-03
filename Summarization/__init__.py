from pororo import Pororo


def load_summ_model():
    summ_model = Pororo(task="text_summarization", lang="ko", model="extractive")
    return summ_model
