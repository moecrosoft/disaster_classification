# 🚨 Text Based Emergency Detection AI

An end-to-end AI application that detects whether a text message indicates an emergency.

This project combines Natural Language Processing (NLP), a deep learning model, and a full-stack system with database and deployment.

---

## 📌 Overview

Users can:
- Enter a message
- Get an AI prediction (Emergency / Not Emergency)
- View message history stored in a database

The entire system is fully containerized and can be run locally with a single command.

---

## 🧠 How It Works (Step-by-Step)

1. User enters a message in the frontend (Next.js UI)

2. Frontend sends request to backend:
POST /predict

3. Backend processes text:
- Cleans text (lowercase, remove symbols, URLs, etc.)
- Tokenizes into words
- Converts words to numerical indices using a vocabulary
- Pads or truncates to fixed length

4. Model prediction:
- Bidirectional LSTM processes the sequence
- Outputs logits → converted into prediction (emergency / not emergency)

5. Database storage:
- Message and prediction are saved into PostgreSQL

6. Response:
- Result is returned and displayed to user

7. History retrieval:
GET /history
- Fetches latest messages from database

---

## 🏗️ Tech Stack

Backend:
- FastAPI
- PyTorch (BiLSTM model)
- psycopg2

Frontend:
- Next.js (React)
- TailwindCSS

Database:
- PostgreSQL

DevOps / Deployment:
- Docker
- Docker Compose
- AWS EC2
- GitHub Actions (CI/CD)

---

## 📂 Project Structure

disaster_classification/
│
├── backend/
│   ├── src/
│   │   ├── api.py
│   │   ├── model.py
│   │   ├── inference.py
│   │   └── dataset.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
└── README.md

---

## 🚀 Getting Started (Local Setup)

### Prerequisites
- Docker
- Docker Compose

---

### 1. Clone the Repository

git clone https://github.com/moecrosoft/disaster_classification.git
cd disaster_classification

---

### 2. Run the Entire System

docker-compose up -d --build

This will start:
- Frontend → http://localhost:3000
- Backend → http://localhost:8000
- PostgreSQL database

---

### 3. Open the Application

http://localhost:3000

---

### 4. Stop the Application

docker-compose down

---

## 📊 Model Details

- Architecture: Bidirectional LSTM
- Embedding size: 128
- Hidden size: 128
- Sequence length: 60
- Output: 2 classes (Emergency / Not Emergency)

Training Features:
- Text cleaning and normalization
- Vocabulary with <pad> and <unk>
- Rare word filtering (min_freq)
- Class imbalance handling:
  - Weighted loss
  - WeightedRandomSampler

Evaluation Metrics:
- Accuracy
- F1 Score (~0.72 on validation set)

---

## 🎯 Features

- Real-time AI prediction
- Message history tracking
- Color-coded results:
  - 🔴 Emergency
  - 🟢 Not Emergency
- Fully containerized system
- One-command local deployment

---

## 🌐 Deployment

This project is deployed on AWS EC2 using:
- Docker Compose for container orchestration
- GitHub Actions for automatic deployment on push to main

Deployment workflow:
1. Push to GitHub
2. GitHub Actions SSH into EC2
3. Pull latest code
4. Build Docker containers
5. Restart services

---

## 🔗 API Endpoints

POST /predict

Request:
{
  "text": "Someone collapsed and needs help"
}

Response:
{
  "prediction": "emergency (confidence: 0.91)"
}

---

GET /history

Response:
[
  {
    "user_message": "...",
    "ai_result": "..."
  }
]
