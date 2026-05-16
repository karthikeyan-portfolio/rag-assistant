# Enterprise RAG Assistant using LangChain, Gemini & Pinecone

An enterprise-style Retrieval-Augmented Generation (RAG) assistant built using LangChain, Google Gemini Embeddings, Gemini 2.5 Flash, and Pinecone Vector Database.

This project demonstrates a modern semantic retrieval pipeline for enterprise document question-answering systems.

---

# Features

- DOCX document ingestion
- Recursive semantic chunking
- Google Gemini Embeddings
- Pinecone vector database integration
- SHA-256 hash-based deduplication
- Batch vector upserts
- Semantic similarity retrieval
- Grounded response generation using Gemini 2.5 Flash
- Modular ingestion and querying pipelines

---

# Tech Stack

- Python
- LangChain
- Google Gemini API
- Pinecone Vector DB
- dotenv

---

# Project Structure

```text
.
├── ingest.py
├── query.py
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

# Engineering Highlights

## Modular RAG Architecture

Separated:
- ingestion pipeline
- retrieval pipeline
- generation pipeline

This follows modern production-style RAG system design.

---

## Hash-Based Deduplication

Uses SHA-256 hashing to avoid duplicate vector storage.

---

## Batch Vector Upserts

Optimized Pinecone insertion for scalable ingestion workflows.

---

## Semantic Retrieval

Uses Google Gemini Embeddings for contextual similarity search.

---

# Future Improvements

- Hybrid Retrieval (BM25 + Dense Search)
- Reranking Models
- Metadata Filtering
- LangSmith Observability
- RAG Evaluation Pipeline
- Streaming Responses
- FastAPI Deployment
- Multi-Document Retrieval
- Agentic RAG Workflow
- Citation Support

---

# Use Cases

- Enterprise Knowledge Assistants
- Healthcare Document Retrieval
- AI-Powered Search Systems
- Internal Documentation Assistants
- Policy and Compliance Search

---

# Resume Positioning

This project demonstrates:

- Retrieval-Augmented Generation (RAG)
- Vector Database Engineering
- Semantic Search Systems
- LLM Orchestration
- Enterprise AI Architecture
- Document Intelligence Pipelines

---