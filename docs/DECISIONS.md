# Architecture Decision Records

## ADR-001 — PostgreSQL + pgvector
Status: Accepted

PostgreSQL + pgvector is the primary vector store.

Rejected as baseline:
- Qdrant
- Elasticsearch
- Milvus
- Pinecone
- Chroma
- FAISS as primary store

Reason: reduce operational complexity while retaining relational metadata and semantic vector search.

## ADR-002 — Ollama on compute plane
Status: Accepted

AI inference is centralized on compute plane.

## ADR-003 — Google ADK on control plane
Status: Accepted

ADK is the agent orchestration layer on control plane.

## ADR-004 — Web Only
Status: Accepted

The only interaction channel is the Web UI.

## ADR-005 — No Elasticsearch
Status: Accepted

Elasticsearch is not part of the current architecture.

## ADR-006 — No Qdrant
Status: Accepted

Qdrant is not part of the current architecture.
