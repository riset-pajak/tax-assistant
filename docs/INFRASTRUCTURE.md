# Infrastructure

## This Computer/Application
Application/control plane:
- ADK
- Python API
- PostgreSQL + pgvector
- SQLite
- Web frontend

## Compute/LLM Server
AI compute plane:
- Ollama
- embedding
- reranker
- LLM

## Network
control plane calls Ollama on compute plane over the private network.

Use:
`OLLAMA_BASE_URL=http://OLLAMA_HOST:11434`

Do not hard-code deployment IPs.

## Docker
Use Docker-first deployment. Avoid unnecessary microservice fragmentation during MVP.
