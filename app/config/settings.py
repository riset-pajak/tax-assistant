"""
Application settings loaded from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self):
        # Database
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASS = os.getenv("DB_PASS", "postgres")
        self.DB_NAME = os.getenv("DB_NAME", "taxassistant")
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:5432/{self.DB_NAME}"
        )
        # Ollama
        self.OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        # Model names (baseline from AGENTS.md)
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "multilingual-e5-large-instruct")
        self.RERANKER_MODEL = os.getenv("RERANKER_MODEL", "bge-reranker-v2-m3")
        self.LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:8b")
        # App
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

settings = Settings()