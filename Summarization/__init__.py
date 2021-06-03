from pororo import Pororo
from wordembedding.utils import split_sentence

def load_summ_model():
<<<<<<< HEAD
    summ_model = Pororo(task="text_summarization", lang="ko", model="extractive")
    return summ_model

def summary_script(json_file, summ_model):
    texts = split_sentence(json_file)
    result = summ_model(texts)

    return result
=======
    model = Pororo(task="text_summarization", lang="ko", model="extractive")
    return model
>>>>>>> 0c84ae153fcab4c308b200fbc9d7d36855098308
