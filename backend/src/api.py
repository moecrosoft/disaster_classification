from fastapi import FastAPI
from pydantic import BaseModel
from src.inference import predict
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2 

app = FastAPI()

FRONTEND_URL = os.environ.get('NEXT_PUBLIC_FRONTEND_URL', 'http://localhost:3000')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
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
    text: str

def save_message(user_message, ai_result):
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO messages (user_message, ai_result) VALUES (%s, %s)',
        (user_message, ai_result)
    )
    conn.commit()
    cur.close()

@app.post('/predict')
def classify(req:Request):
    user_text = req.text
    result_dict = predict(user_text)
    result_str = f'{result_dict["label"]} (confidence: {result_dict["confidence"]:.2f})'
    save_message(user_text, result_str)
    return {'prediction': result_str}

@app.get('/history')
def history():
    cur = conn.cursor()
    cur.execute(
        'SELECT user_message, ai_result FROM messages ORDER BY id DESC LIMIT 50'
    )
    rows = cur.fetchall()
    messages = [{'user_message': r[0], 'ai_result': r[1]} for r in rows]
    return messages