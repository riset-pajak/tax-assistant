# AGENTS.md — Engineering Rules

## Architecture Rules
The system is divided into:
- application/control plane
- AI compute plane

control plane:
- Google ADK
- Python backend/API
- PostgreSQL + pgvector
- SQLite
- Web frontend

compute plane:
- Ollama
- embedding model multilingual-e5-large-instruct use jeffh/intfloat-multilingual-e5-large-instruct:q8_0
- reranker model bge-reranker-v2-m3 use hans-tech/bge-reranker-v2-m3:260522
- configured LLM prefer use qwen3:8b

## Design Principle
ADK orchestrates. Tools execute. PostgreSQL stores knowledge. pgvector performs semantic retrieval. Reranker scores relevance. Ollama provides AI inference. Web provides interaction.

## Code Organization
Prefer separation:
- app/agent
- app/tools
- app/services
- app/rag
- app/database
- app/api
- frontend
- tests
- scripts
- docker
- config

## Tool Boundary
Agents should call well-defined tools. RAG database operations must live in services/repositories, not inside prompt logic.

Primary RAG interface:
`search_knowledge(query: str, top_k: int = 5)`

## Configuration
Never hard-code:
- IP addresses
- credentials
- model names
- environment-specific paths
- secrets

Use environment variables/configuration.

Never modify, create, delete, overwrite, or commit `.env` or any environment-specific local configuration file. Treat `.env` as user-local and read-only. When configuration schema changes, update `.env.example` or documented configuration instead.
Use environment variables/configuration in .env on root project. Don't edit this file.

## Model Baseline
Embedding: multilingual-e5-large-instruct
Reranker: bge-reranker-v2-m3
LLM baseline: qwen3:8b

Verify actual Ollama compatibility before implementation. Do not silently substitute a model.

## Testing
RAG components must be independently testable:
- embedding
- vector search
- reranking
- context assembly
- ADK tool
- Ollama connectivity
- API
- frontend integration

## Grounding
LLM output must be grounded in retrieved evidence. If evidence is insufficient, do not fabricate facts.

## Change Discipline
Before large refactors:
1. inspect;
2. explain impact;
3. implement incrementally;
4. test;
5. document.
