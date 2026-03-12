from fastapi import FastAPI
from pydantic import BaseModel
from src.inference import predict
from fastapi.middleware.cors import CORSMiddleware
from src.dataset import load_data, build_vocab

df = load_data()
texts = df['text'].tolist()
vocab = build_vocab(texts)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class Request(BaseModel):
    text:str

@app.post('/predict')

def classify(req:Request):
    result = predict(req.text,vocab)
    return{'prediction':result}