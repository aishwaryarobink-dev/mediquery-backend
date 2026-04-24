# ⚙️ MediQuery Backend – Flask API for AI Medical Assistant

> 🔗 Frontend Repository: https://github.com/aishwaryarobink-dev/mediquery-frontend

---

## 🚀 Overview

This repository contains the backend service for MediQuery, an AI-powered medical assistant.

Built using Flask, the backend handles request processing, lightweight context retrieval, and real-time streaming of LLM responses using Server-Sent Events (SSE).

---

## 🏗️ Architecture

The backend acts as an intermediary between the frontend and the LLM:

* Receives user queries and conversation history
* Retrieves relevant context from a local knowledge base
* Sends structured prompts to the Groq LLM
* Streams responses back to the frontend in real-time

---

## ⚡ Key Features

* 🔄 Real-time streaming responses using Server-Sent Events (SSE)
* 🧠 Integration with Groq API for fast LLM inference
* 📚 Lightweight context retrieval from JSON-based knowledge base
* 🌐 CORS-enabled API for cross-origin frontend communication
* 🛠️ Robust error handling and streaming-safe responses

---

## 📡 API Endpoints

### `GET /`

Health check endpoint

**Response:**

```json
{ "status": "ok" }
```

---

### `POST /api/chat`

Handles chat requests and streams AI responses.

#### Request Body

```json
{
  "messages": [
    { "role": "user", "content": "What is a headache?" }
  ]
}
```

#### Response

* Content-Type: `text/event-stream`
* Streamed in chunks using SSE format:

```text
data: {"text": "A headache is...", "source": "model"}

data: {"text": "It can be caused by...", "source": "kb"}

data: [DONE]
```

---

## 🔄 Streaming Flow (SSE)

1. Client sends POST request with message history
2. Backend calls Groq API with streaming enabled
3. Response chunks are received incrementally
4. Each chunk is sent to client using SSE (`data: ...\n\n`)
5. Client reconstructs response in real-time

---

## 🧠 Context Retrieval

A simple keyword-based retrieval system is used:

* Loads documents from `medical_knowledge.json`
* Matches query terms against document content
* Selects the most relevant document (if score ≥ threshold)
* Injects context into system prompt

---

## 🛠️ Tech Stack

* Python
* Flask
* Groq API (LLM inference)
* Flask-CORS
* JSON-based knowledge base

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
PORT=5000
```

---

## ▶️ Running Locally

```bash
git clone https://github.com/aishwaryarobink-dev/mediquery-backend.git
cd mediquery-backend

pip install -r requirements.txt
python app.py
```

Server runs on:

```
http://localhost:5000
```

---

## 🌐 Deployment

* Hosted on Render
* Configured with environment variables
* CORS enabled for frontend integration

---

## ⚠️ Known Limitations

* Keyword-based retrieval (not embedding-based RAG)
* No persistent storage or database
* No authentication or rate limiting
* Limited domain knowledge (static JSON file)

---

## 📈 Future Improvements

* Semantic search using embeddings (true RAG)
* Database integration (MongoDB / PostgreSQL)
* Authentication & rate limiting
* Scalable deployment (Docker, Kubernetes)
* Structured logging and monitoring

---

## 👩‍💻 Author

**Aishwarya Robin Kandikatla**

* GitHub: https://github.com/aishwaryarobink-dev
* LinkedIn: linkedin.com/in/aishwarya-robin-kandikatla

---

## ⭐ Support

If you find this useful, consider giving it a ⭐ on GitHub!
