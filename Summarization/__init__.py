from pororo import Pororo


def load_summ_model():
    model = Pororo(task="text_summarization", lang="ko", model="extractive")
    return model
