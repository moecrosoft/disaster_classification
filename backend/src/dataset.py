import pandas as pd
import numpy as np
import torch
import os
from sklearn.model_selection import train_test_split

def load_data():
    base = os.path.dirname(__file__)
    path = os.path.join(base,'..','data','train.csv')
    df = pd.read_csv(path)
    df = df[['text','target']]
    df['text'] = df['text'].str.lower()
    
    return df

def tokenize(text):
    return text.split()

def build_vocab(texts):
    vocab = {'<PAD>':0}
    index = 1
    for sentence in texts:
        for word in tokenize(sentence):
            if word not in vocab:
                vocab[word] = index
                index += 1

    return vocab

def encode_text(text,vocab,max_len):
    tokens = tokenize(text)
    ids = [vocab.get(t,0) for t in tokens]
    if len(ids) < max_len:
        ids += [0] * (max_len-len(ids))
    else:
        ids = ids[:max_len]

    return ids