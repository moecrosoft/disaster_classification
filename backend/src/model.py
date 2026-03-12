import torch
import torch.nn as nn

class EmergencyModel(nn.Module):
    def __init__(self,vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size,128)
        self.lstm = nn.LSTM(128,128,batch_first=True)
        self.fc = nn.Linear(128,2)
    
    def forward(self,x):
        x = self.embedding(x)
        _,(hidden,_) = self.lstm(x)
        out = self.fc(hidden[-1])
        return out