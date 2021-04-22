import time
import random

import sklearn
from pylab import *
from transformers import AutoTokenizer
from torch.nn import functional

import spacy
from spacy.lang.en import English

def init():
    pass
def run(input_data):
    # time.sleep(10)
    def _subfunction(a):
        return a + 1
    value = random.random()
    input_data['new'] = value
    input_data['new count'] = input_data['new'].apply(lambda x: _subfunction(x))
    return input_data
