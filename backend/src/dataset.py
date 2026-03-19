import pandas as pd

def load_train():
    return pd.read_csv('backend/data/train.csv')

def load_test():
    return pd.read_csv('backend/data/test.csv')

def build_vocab(texts, min_freq=2):
    from collections import Counter
    counter = Counter()
    for text in texts:
        counter.update(text.split())
    vocab = {'<pad>': 0, '<unk>': 1}
    idx = 2
    for word, freq in counter.items():
        if freq >= min_freq:
            vocab[word] = idx
            idx += 1
    return vocab

def encode_text(text, vocab, max_len=60):
    tokens = text.split()
    encoded = [vocab.get(t, vocab['<unk>']) for t in tokens]
    if len(encoded) < max_len:
        encoded += [vocab['<pad>']] * (max_len - len(encoded))
    else:
        encoded = encoded[:max_len]
    return encoded