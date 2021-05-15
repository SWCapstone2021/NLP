# Copyright (c) 2020, Soohwan Kim. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from glob import glob

import torch
import torch.nn as nn
import numpy as np
import torchaudio
from torch import Tensor

from kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech.audio.core import load_audio
from kospeech.models import (
    DeepSpeech2,
    ListenAttendSpell,
)


def parse_audio(audio_path: str, del_silence: bool = False, audio_extension: str = 'pcm') -> Tensor:

    paths = sorted(glob(os.path.join(audio_path,'*.wav')), key=lambda i: int(os.path.basename(i)[:-4]))
    features = list()
    input_lengths = list()

    for path in paths:
        signal = load_audio(path, del_silence, extension=audio_extension)
        feature = torchaudio.compliance.kaldi.fbank(
            waveform=Tensor(signal).unsqueeze(0),
            num_mel_bins=80,
            frame_length=20,
            frame_shift=10,
            window_type='hamming'
        ).transpose(0, 1).numpy()

        feature -= feature.mean()
        feature /= np.std(feature)
        feature = torch.FloatTensor(feature).transpose(0, 1)

        features.append(feature)
        input_lengths.append(torch.LongTensor([len(feature)]))

    return features, input_lengths

def stt(model, vocab, audio_path):
    
    features, input_lengths = parse_audio(audio_path, del_silence=True)
    sentences = list()

    for feature, input_length in zip(features, input_lengths):
        y_hats = model.recognize(feature.unsqueeze(0).to('cuda'), input_length)
        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())
        
        sentences.append(sentence)
    
    return sentences

def load_model(model_path='models/ds2.pth'):
    device = 'cuda'

    model = torch.load(model_path, map_location=lambda storage, loc: storage).to(device)
    if isinstance(model, nn.DataParallel):
        model = model.module
    model.eval()

    if isinstance(model, ListenAttendSpell):
        model.encoder.device = device
        model.decoder.device = device
    
    vocab = KsponSpeechVocabulary('kospeech/aihub_character_vocabs.csv')

    return model, vocab




