"""
Health check endpoints.
"""
from fastapi import APIRouter

from app.services.ollama_client import ollama_client

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """
    Overall health check: checks app and dependencies.
    Returns 200 if all critical services are healthy.
    """
    # Check Ollama
    ollama_ok = ollama_client.health_check()
    # TODO: Check database connection
    db_ok = True  # placeholder
    if ollama_ok and db_ok:
        return {"status": "ok", "ollama": ollama_ok, "database": db_ok}
    else:
        return {"status": "degraded", "ollama": ollama_ok, "database": db_ok}


@router.get("/health/ollama")
def ollama_health():
    """
    Check Ollama service specifically.
    """
    ok = ollama_client.health_check()
    return {"status": "ok" if ok else "error", "service": "ollama"}


@router.get("/health/models")
def list_models():
    """
    List available Ollama models.
    """
    try:
        models = ollama_client.list_models()
        return {"models": models}
    except Exception as e:
        return {"error": str(e), "models": []}