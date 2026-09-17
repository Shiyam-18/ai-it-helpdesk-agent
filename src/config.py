import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"
    embedding_model: str = "gemini-embedding-2"
    top_k: int = 4
    min_similarity: float = 0.20
    db_path: str = "data/helpdesk.db"
    index_path: str = "data/embeddings.json"


def _require_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "your_gemini_api_key_here":
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Create a .env file from .env.example "
            "and add your Gemini API key."
        )
    return key


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return default


settings = Settings(
    gemini_api_key=_require_api_key(),
    gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    embedding_model=os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-2"),
    top_k=_int_env("TOP_K", 4),
    min_similarity=_float_env("MIN_SIMILARITY", 0.20),
)
