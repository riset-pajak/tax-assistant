"""
Ollama client service for embedding, reranking, and LLM generation.
Handles timeout, retry, and error mapping.
"""
from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional, Union

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class OllamaError(Exception):
    """Base exception for Ollama-related errors."""


class OllamaConnectionError(OllamaError):
    """Raised when Ollama service is unreachable."""


class OllamaModelError(OllamaError):
    """Raised when a requested model is not available or fails."""


class OllamaAPIError(OllamaError):
    """Raised when Ollama API returns an error status."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"Ollama API error {status_code}: {message}")


class OllamaClient:
    def __init__(
        self,
        host: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.host = host or settings.OLLAMA_HOST.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = httpx.Client(timeout=self.timeout)

    # ------------------------------------------------------------------
    # Internal request handling with retry logic
    # ------------------------------------------------------------------
    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.host}{endpoint}"
        try:
            response = self._client.request(
                method,
                url,
                json=json_data,
                params=params,
            )
            # Raise for HTTP errors (4xx/5xx) but catch them as OllamaAPIError
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    message = error_data.get("error", response.text)
                except Exception:
                    message = response.text
                raise OllamaAPIError(response.status_code, message)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Ollama HTTP error: %s - %s",
                exc.response.status_code,
                exc.response.text,
            )
            if exc.response.status_code == 404:
                raise OllamaModelError(
                    f"Model or endpoint not found: {exc.response.text}"
                ) from exc
            elif exc.response.status_code >= 500:
                raise OllamaError(
                    f"Ollama server error: {exc.response.status_code}"
                ) from exc
            else:
                raise OllamaError(
                    f"Ollama request failed: {exc.response.status_code}"
                ) from exc
        except (httpx.ConnectError, httpx.ReadTimeout) as exc:
            logger.error("Ollama connection error: %s", exc)
            raise OllamaConnectionError(
                f"Cannot connect to Ollama at {self.host}"
            ) from exc
        except Exception as exc:  # pragma: no cover - safety net
            logger.error("Unexpected Ollama error: %s", exc)
            raise OllamaError(f"Unexpected error: {exc}") from exc

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------
    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((OllamaConnectionError,)),
    )
    def embed(
        self,
        model: str,
        input: Union[str, List[str]],
    ) -> List[List[float]]:
        """
        Get embeddings for input text(s).
        Returns list of vectors (list of floats).
        """
        payload = {"model": model, "input": input}
        data = self._request("POST", "/api/embeddings", json_data=payload)
        # Ollama returns {"embedding": [...]} for single input,
        # or {"embeddings": [[...], ...]}? Actually the API returns
        # {"embedding": [...]} for a single string, and for a list it returns
        # {"embeddings": [[...], ...]}? We'll handle both.
        if "embedding" in data:
            # Single input
            return [data["embedding"]] if isinstance(input, str) else data["embedding"]
        if "embeddings" in data:
            return data["embeddings"]
        # Fallback: assume the root is the list
        if isinstance(data, list):
            return data
        raise OllamaError(f"Unexpected embedding response: {data}")

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((OllamaConnectionError,)),
    )
    def rerank(
        self,
        model: str,
        query: str,
        documents: List[str],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents w.r.t. query using Ollama reranker model.
        Returns list of dicts with keys: 'index', 'score', 'text' (original doc).
        """
        payload = {
            "model": model,
            "query": query,
            "documents": documents,
        }
        if top_k is not None:
            payload["top_k"] = top_k
        data = self._request("POST", "/api/rerank", json_data=payload)
        # Normalize output: expected format is list of {index, score, text}
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # Some Ollama versions return {result: [...]} 
            if "result" in data and isinstance(data["result"], list):
                return data["result"]
            # Fallback: wrap single result
            return [data]
        raise OllamaError(f"Unexpected rerank response: {data}")

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((OllamaConnectionError,)),
    )
    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        template: Optional[str] = None,
        context: Optional[List[int]] = None,
        stream: bool = False,
        options: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], str]:
        """
        Generate text from Ollama model.
        If stream=False, returns full response dict.
        If stream=True, returns generator yielding chunks.
        """
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
        }
        if system:
            payload["system"] = system
        if template:
            payload["template"] = template
        if context is not None:
            payload["context"] = context
        if options:
            payload["options"] = options

        if stream:
            # For streaming, we return an iterator; caller must handle.
            def stream_gen():
                with httpx.Client(timeout=None) as client:
                    with client.stream(
                        "POST",
                        f"{self.host}/api/generate",
                        json=payload,
                    ) as resp:
                        resp.raise_for_status()
                        for line in resp.iter_lines():
                            if line:
                                yield json.loads(line.decode("utf-8"))
            return stream_gen()
        else:
            data = self._request("POST", "/api/generate", json_data=payload)
            return data

    def health_check(self) -> bool:
        """
        Simple health check: try to get model list.
        Returns True if Ollama is reachable and responsive.
        """
        try:
            self._request("GET", "/api/tags")
            return True
        except OllamaError:
            return False

    def list_models(self) -> List[str]:
        """Return list of available model names."""
        data = self._request("GET", "/api/tags")
        models = data.get("models", [])
        return [m.get("name", "") for m in models if m.get("name")]

    def close(self):
        self._client.close()


# Singleton instance for convenience
ollama_client = OllamaClient()