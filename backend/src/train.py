import torch
import torch.nn as nn
import torch.optim as optim
import os
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler
from sklearn.utils.class_weight import compute_class_weight

from dataset import load_train, build_vocab, encode_text
from model import EmergencyModel

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+','',text)
    text = re.sub(r'@\w+','',text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'[^a-z\s]','',text)
    text = re.sub(r'\s+',' ',text).strip()
    return text

df = load_train()
df['text'] = df['text'].apply(clean_text)

texts = df['text'].tolist()
labels = df['target'].values

vocab = build_vocab(texts)

max_len = 60
x = [encode_text(t, vocab, max_len) for t in texts]
x = torch.tensor(x)
y = torch.tensor(labels, dtype=torch.long)

x_train, x_val, y_train, y_val = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

class_weights_np = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train.numpy()),
    y = y_train.numpy()
)

class_weights = torch.tensor(class_weights_np, dtype=torch.float)

sample_weights = [class_weights[int(label)] for label in y_train]
sampler = WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)

train_loader = DataLoader(
    TensorDataset(x_train,y_train),
    batch_size=32,
    sampler=sampler
)

val_loader = DataLoader(
    TensorDataset(x_val,y_val),
    batch_size=32
)

model = EmergencyModel(len(vocab))

criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = optim.Adam(model.parameters(),lr=0.0005)

def evaluate(loader):
    model.eval()
    preds = []
    true = []

    with torch.no_grad():
        for x, y in loader:
            outputs = model(x)
            _, predicted = torch.max(outputs,1)
            preds.extend(predicted.tolist())
            true.extend(y.tolist())
    
    acc = accuracy_score(true,preds)
    f1 = f1_score(true,preds,zero_division=0)

    return acc, f1

num_epochs = 6

for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for x, y in train_loader:
        optimizer.zero_grad()

        outputs = model(x)
        loss = criterion(outputs,y)

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
        optimizer.step()

        total_loss += loss.item() * x.size(0)

    avg_loss = total_loss / len(train_loader.dataset)

    val_acc, val_f1 = evaluate(val_loader)

    print(f"Epoch {epoch+1}/{num_epochs}")
    print(f"Loss: {avg_loss:.4f} | Val Acc: {val_acc:.4f} | Val F1: {val_f1:.4f}")
    print("-" * 30)

script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir, 'models')
os.makedirs(models_dir, exist_ok=True)

torch.save(model.state_dict(), os.path.join(models_dir, 'emergency_model.pt'))
torch.save(vocab, os.path.join(models_dir, 'vocab.pt'))

print("Model and vocab saved successfully!")