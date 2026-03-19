import torch
import torch.nn as nn

class EmergencyModel(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, 128)

        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=128,
            batch_first=True,
            bidirectional=True
        )

        self.dropout = nn.Dropout(0.4)

        self.fc = nn.Sequential(
            nn.Linear(128 * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64,2)
        )

    def forward(self,x):
        x = self.embedding(x)

        outputs, _ = self.lstm(x)

        x = outputs.mean(dim=1)

        x = self.dropout(x)

        return self.fc(x)