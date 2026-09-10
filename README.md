# Web AI Agent Project Context

This repository defines a self-hosted Web AI Agent architecture.

## Nodes

### Control Plane
Google ADK, Python backend/API, PostgreSQL + pgvector, SQLite, Web frontend.

### AI Compute Plane
Ollama serving embedding, reranker, and LLM models.

## Core Flow

Browser → Web/API → Google ADK → RAG Tool → PostgreSQL/pgvector → Reranker → Ollama LLM → Web/API → Browser

See `docs/` for the authoritative architecture and implementation context.
