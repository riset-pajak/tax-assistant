# Database

PostgreSQL + pgvector is the primary knowledge store.

Recommended entities:

## documents
- id
- document_id
- document_type
- document_number
- title
- year
- version
- status
- source
- created_at
- updated_at

## document_chunks
- id
- document_id
- chunk_index
- content
- metadata
- embedding
- created_at

Embedding dimension must be verified from the actual embedding model output before schema finalization.
