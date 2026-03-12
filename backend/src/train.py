import torch
import torch.nn as nn
import torch.optim as optim
import os
import pandas as pd
from dataset import load_data, build_vocab, encode_text
from model import EmergencyModel

df = load_data()
texts = df['text'].tolist()
labels = df['target'].values
vocab = build_vocab(texts)

max_len = 40
x = [encode_text(t,vocab,max_len) for t in texts]
x = torch.tensor(x)
y = torch.tensor(labels)

model = EmergencyModel(len(vocab))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(x)
    loss = criterion(outputs,y)
    loss.backward()
    optimizer.step()
    print('Epoch:',epoch,'Loss:',loss.item())

script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir,'models')
os.makedirs(models_dir, exist_ok=True)

torch.save(model.state_dict(), os.path.join(models_dir, 'emergency_model.pt'))