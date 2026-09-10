# RAG Design

## Ingestion
Document → Parser → Structural Chunking → Metadata → Embedding @ compute plane → PostgreSQL/pgvector

## Query
Question → Query Embedding @ compute plane → pgvector Search → Candidate Chunks → Reranker @ compute plane → Top-N Context → LLM @ compute plane

## Principles
- Prefer structural chunking for structured/regulatory documents.
- Preserve document hierarchy in metadata.
- Store source metadata with every chunk.
- Use pgvector as the primary semantic retrieval mechanism.
- Rerank candidates before generation.
- Keep retrieval independently testable.

## Evidence
The LLM is not the source of truth. Retrieved evidence is the source of truth.

If evidence is insufficient, the agent must not fabricate an answer.
