import torch
import os
import pandas
from src.model import EmergencyModel
from src.dataset import encode_text
from src.dataset import load_data, build_vocab

labels = ['not emergency','emergency']

df = load_data()
texts = df['text'].tolist()
vocab = build_vocab(texts)
vocab_size = len(vocab)

model = EmergencyModel(vocab_size)

script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir, 'models')
model_path = os.path.join(models_dir, 'emergency_model.pt')
model.load_state_dict(torch.load(model_path))

model.eval()

def predict(text,vocab):
    x = encode_text(text,vocab,40)
    x = torch.tensor([x])
    outputs = model(x)
    pred = torch.argmax(outputs,dim=1).item()
    return labels[pred]