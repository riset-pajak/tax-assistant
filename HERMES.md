# HERMES.md — Project Operating Instructions

## Mission
Develop and maintain a self-hosted Web AI Agent using Google ADK on this control plane as the control/orchestration node and Ollama on the compute plane as the AI compute node.

## Mandatory Architecture
- Web is the only interaction channel.
- Google ADK runs on this computer as control plane.
- Python is the primary backend language.
- PostgreSQL + pgvector is the primary vector store.
- Ollama runs on compute plane.
- Embedding, reranking, and LLM inference are intended to run on compute plane through Ollama, subject to model/runtime compatibility.
- SQLite is used for application logs/audit.
- Docker-first deployment.

## Explicitly Excluded
Do not introduce Qdrant, Elasticsearch, vLLM, Gemini/Vertex AI, OpenAI API, WhatsApp/Baileys, or another vector database unless explicitly requested or an ADR is approved.

## Operating Procedure
1. Inspect the repository before modifying anything.
2. Read AGENTS.md and relevant docs before implementation.
3. Identify existing working components and avoid unnecessary rewrites.
4. Make incremental changes.
5. Test each major change.
6. Update documentation when architecture/configuration changes.
7. Never silently replace a requested technology.
8. If a dependency is incompatible, document the issue and propose alternatives before changing architecture.

## Priority
Correctness > reproducibility > observability > performance > feature breadth.

## Development Order
Infrastructure → model connectivity → ingestion → retrieval → reranking → ADK tool → generation → citation → Web UI → agentic RAG → evaluation → multi-agent.

## Security
Never commit secrets, credentials, API keys, or production .env files. Use .env.example and environment variables.
