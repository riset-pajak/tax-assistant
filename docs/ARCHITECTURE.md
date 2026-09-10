# Architecture

```text
Browser
  |
  v
Web/API
  |
  v
Google ADK
  |
  +--> Tools
  |
  +--> RAG Tool
          |
          +--> PostgreSQL + pgvector
          |
          +--> Reranker @ compute plane
          |
          +--> Context
                    |
                    v
                 Ollama @ compute plane
                    |
                    v
                   LLM
                    |
                    v
                 Answer
                    |
                    v
                 Browser
```

This computer is the control/application plane. Ollama server is the AI compute plane.

Do not expose Ollama directly to the browser.
