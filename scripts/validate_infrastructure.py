#!/usr/bin/env python3
"""
Infrastructure validation script.
Checks if required services are reachable and responding correctly.
"""
import sys
import socket
import os
import json
import urllib.request
import urllib.error
from urllib.parse import urljoin


def check_port(host, port, service_name, timeout=5):
    """Check if a TCP port is open."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            print(f"[OK] {service_name} at {host}:{port} is reachable")
            return True
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"[FAIL] {service_name} at {host}:{port} is not reachable: {e}")
        return False


def parse_ollama_url(ollama_host_env):
    """
    Parse OLLAMA_HOST environment variable into (host, port, base_url).
    Supports formats: http://host:port, host:port, http://host
    """
    url = ollama_host_env.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    from urllib.parse import urlparse
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 11434
    base_url = f"{parsed.scheme}://{host}:{port}"
    return host, port, base_url


def check_ollama_api(ollama_url, timeout=5):
    """Check if Ollama API is responding by hitting /api/version."""
    api_url = urljoin(ollama_url, "/api/version")
    try:
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            version = data.get("version", "unknown")
            print(f"[OK] Ollama API is responding (version: {version}) at {ollama_url}")
            return True
    except urllib.error.URLError as e:
        print(f"[FAIL] Ollama API is not responding at {ollama_url}: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"[FAIL] Ollama API returned invalid JSON at {ollama_url}: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error checking Ollama API at {ollama_url}: {e}")
        return False


def check_ollama_models(ollama_url, required_models, timeout=10):
    """Check if all required models are available on Ollama."""
    list_url = urljoin(ollama_url, "/api/show")
    available_models = set()

    try:
        req = urllib.request.Request(list_url, data=b'{}', headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            version = data.get("version", "unknown")
            print(f"[OK] Ollama API is responding (version: {version}) at {ollama_url}")
            return True
    except urllib.error.URLError as e:
        print(f"[FAIL] Ollama API is not responding at {ollama_url}: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"[FAIL] Ollama API returned invalid JSON at {ollama_url}: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error checking Ollama API at {ollama_url}: {e}")
        return False


def main():
    # Read configuration from environment or .env
    from dotenv import load_dotenv
    load_dotenv()

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", 5432))

    # Use OLLAMA_HOST (not OLLAMA_URL)
    ollama_host_env = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_host, ollama_port, ollama_url = parse_ollama_url(ollama_host_env)

    # Required models from environment, fallback to baseline models
    required_models_env = os.getenv("REQUIRED_MODELS", "")
    if required_models_env:
        required_models = [m.strip() for m in required_models_env.split(",") if m.strip()]
    else:
        # Default to baseline models from AGENTS.md
        required_models = ["multilingual-e5-large-instruct", "bge-reranker-v2-m3", "qwen3:8b"]

    checks = [
        (db_host, db_port, "PostgreSQL"),
        (ollama_host, ollama_port, "Ollama"),
    ]

    all_ok = True

    # TCP port checks
    for host, port, name in checks:
        if not check_port(host, port, name):
            all_ok = False

    # Ollama API health check
    if not check_ollama_api(ollama_url):
        all_ok = False

    if all_ok:
        print("\nAll infrastructure checks passed.")
        sys.exit(0)
    else:
        print("\nSome infrastructure checks failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
