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

## Quick Start

1. Copy `.env.example` to `.env` and fill in the values.
2. Start the services:
   ```bash
   docker-compose up -d
   ```
3. Run database migrations:
   ```bash
   alembic upgrade head
   ```
4. The application will be available at http://localhost:8000 (if you have a web server configured).

## Development

- Ensure you have Docker and Docker Compose installed.
- Run `./scripts/validate_infrastructure.py` to check if services are reachable.
- Run tests with `pytest`.

