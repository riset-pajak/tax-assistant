#!/usr/bin/env python3
"""
Validate that the baseline Ollama models are available.
Run after Ollama service is up.
"""
import sys
import os

# Load environment variables from .env file (root project)
from dotenv import load_dotenv
load_dotenv()

# Add the project root (parent of this script's directory) to sys.path
# so that we can import from the 'app' package if needed.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Determine Ollama URL: OLLAMA_URL primary, OLLAMA_HOST as fallback
ollama_url_env = os.getenv("OLLAMA_URL") or os.getenv("OLLAMA_HOST", "http://localhost:11434")

from urllib.parse import urlparse
parsed = urlparse(ollama_url_env)
ollama_host = parsed.hostname or "localhost"
ollama_port = parsed.port or 11434
ollama_base_url = f"{parsed.scheme}://{ollama_host}:{ollama_port}"

# Import Ollama client using the resolved URL
import httpx

ollama_client = httpx.Client(timeout=30.0)


def health_check():
    """Check if Ollama service is reachable."""
    try:
        resp = ollama_client.get(f"{ollama_base_url}/api/version", timeout=5.0)
        resp.raise_for_status()
        return True
    except Exception:
        return False


def list_models():
    """List available Ollama models with full metadata."""
    try:
        resp = ollama_client.get(f"{ollama_base_url}/api/tags", timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        models = []
        for m in data.get("models", []):
            name = m.get("name", "")
            capabilities = m.get("capabilities", [])
            details = m.get("details", {})
            models.append({
                "name": name,
                "capabilities": capabilities,
                "details": details,
                "modified_at": m.get("modified_at", ""),
            })
        return models
    except Exception as e:
        print(f"❌ Failed to list models: {e}")
        return []


def main():
    print("Checking Ollama service...")
    if not health_check():
        print(f"❌ Ollama service is not reachable at {ollama_base_url}")
        sys.exit(1)
    print("✅ Ollama service is reachable")

    print("\nFetching available models...")
    try:
        available = list_models()
    except Exception as e:
        print("❌ Failed to list models:", e)
        sys.exit(1)

    print(f"Available models ({len(available)}):")
    for m in available:
        print(f"  - {m['name']} (capabilities: {m['capabilities']})")

    # Baseline models from AGENTS.md
    required = {
        "embedding": "jeffh/intfloat-multilingual-e5-large-instruct:q8_0",
        "reranker": "hans-tech/bge-reranker-v2-m3:260522",
        "llm": "qwen3:8b",
    }

    missing = []
    for kind, model in required.items():
        # Check if model exists in available list (exact match or prefix?)
        found = any(model == m["name"] or m["name"].startswith(model + ":") for m in available)
        if not found:
            missing.append((kind, model))
        else:
            # Display model metadata
            md = next(m for m in available if m["name"] == model)
            print(f"✅ {kind} model '{model}' found")
            print(f"   - Uploader: {md['name'].split('/')[0] if '/' in md['name'] else 'local'}")
            print(f"   - Capabilities: {', '.join(md['capabilities'])}")
            if md['details']:
                print(f"   - Parameter size: {md['details'].get('parameter_size', 'N/A')}")
                print(f"   - Quantization: {md['details'].get('quantization_level', 'N/A')}")
                print(f"   - Modified: {md['modified_at'][:10] if md['modified_at'] else 'N/A'}")

    if missing:
        print("\n❌ Missing models:")
        for kind, model in missing:
            print(f"   - {kind}: {model}")
        print("\nPlease pull the missing models, e.g.:")
        for _, model in missing:
            print(f"   docker exec -it <ollama-container> ollama pull {model}")
        sys.exit(1)
    else:
        print("\n🎉 All baseline models are available!")
        sys.exit(0)


if __name__ == "__main__":
    main()
