# API

Minimum API:

`POST /api/chat`
`GET /health`
`GET /health/ollama`
`GET /health/database`

Example chat response:

```json
{
  "answer": "...",
  "sources": [],
  "request_id": "..."
}
```

The browser communicates with this computer as control plane. The browser must not call Ollama directly.
