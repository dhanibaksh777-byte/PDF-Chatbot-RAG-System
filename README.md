# PDF Chatbot — RAG System

A Retrieval-Augmented Generation (RAG) system that lets users upload PDF documents and ask natural language questions about them.

## Screenshot

![PDF Chatbot](https://github.com/dhanibaksh777-byte/PDF-Chatbot-RAG-System/blob/9de1b0fe1a8ce23128c59815aa0c3818e4bdfbe9/Screenshot%202026-09-09%20181043.png?raw=true)

## How It Works

1. User uploads a PDF
2. Document is chunked and embedded using Jina Embeddings API
3. Embeddings stored as vectors in PostgreSQL (pgvector)
4. At query time, semantic similarity search finds relevant chunks
5. LLM generates accurate, context-aware answer from retrieved chunks

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL + pgvector (Neon.tech)
- **Embeddings:** Jina Embeddings API
- **ORM:** SQLAlchemy
- **Deployment:** Render

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/store-pdf` | Upload and store a PDF |
| POST | `/ask` | Ask a question about stored documents |

## Setup

```bash
git clone https://github.com/dhanibaksh777-byte/PDF-Chatbot-RAG-System.git
cd PDF-Chatbot-RAG-System
pip install -r requirements.txt
```

Add `.env` file:
