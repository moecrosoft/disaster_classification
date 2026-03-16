from fastapi import FastAPI
from pydantic import BaseModel
from src.inference import predict
from fastapi.middleware.cors import CORSMiddleware
from src.dataset import load_data, build_vocab
import os
import psycopg2

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

conn = psycopg2.connect(
    host = os.environ['POSTGRES_HOST'],
    database = os.environ['POSTGRES_DB'],
    user = os.environ['POSTGRES_USER'],
    password = os.environ['POSTGRES_PASSWORD']
)

class Request(BaseModel):
    text:str

def save_message(user_message, ai_result):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (user_message, ai_result) VALUES (%s, %s)",
        (user_message, ai_result)
    )
    conn.commit()
    cur.close()

@app.post('/predict')

def classify(req:Request):
    user_text = req.text
    result = predict(user_text, vocab)
    save_message(user_text, result)
    return {'prediction': result}

@app.get('/history')

def history():
    cur = conn.cursor()

    cur.execute(
        'SELECT user_message, ai_result FROM messages ORDER BY id DESC LIMIT 50'
    )

    rows = cur.fetchall()

    messages = []

    for r in rows:
        messages.append({
            'user_message': r[0],
            'ai_result': r[1]
        })

    return messages