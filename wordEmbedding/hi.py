import torch

from kor2vec.kor2vec import Kor2Vec

print(torch.cuda.is_available(), torch.cuda.device_count())

kor2vec = Kor2Vec(embed_size=128)

kor2vec.train(corpus_path='dataset/corpus_mecab_jamo.txt', model_path='runs/',
              sample_path='dataset/corpus_mecab_jamo.txt.sampled', batch_size=128)  # takes some time
