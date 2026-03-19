import torch
import torch.nn.functional as F
import os
from src.dataset import encode_text
from src.model import EmergencyModel

script_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(script_dir,'models')

model_path = os.path.join(models_dir,'emergency_model.pt')
vocab_path = os.path.join(models_dir,'vocab.pt')

vocab = torch.load(vocab_path)

model = EmergencyModel(len(vocab))
model.load_state_dict(torch.load(model_path))
model.eval()

labels = ['not emergency', 'emergency']
max_len = 40

def predict(text):
    x = encode_text(text, vocab, max_len)
    x = torch.tensor([x])

    with torch.no_grad():
        outputs = model(x)
        probs = F.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs,1)

    return {
        'label': labels[predicted.item()],
        'confidence': float(confidence.item())
    }