from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from google import genai

from src.config import settings


class KnowledgeBase:
    """Small local vector-search knowledge base for the project demo."""

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.kb_dir = Path("knowledge_base")
        self.index_path = Path(settings.index_path)
        self.records: list[dict[str, Any]] = []

        if self.index_path.exists():
            self._load_index()

    def _load_index(self) -> None:
        with self.index_path.open("r", encoding="utf-8") as f:
            self.records = json.load(f)

    def build_index(self) -> int:
        docs = sorted(self.kb_dir.glob("*.md"))
        if not docs:
            raise RuntimeError("No knowledge-base documents found.")

        records = []
        for path in docs:
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue

            response = self.client.models.embed_content(
                model=settings.embedding_model,
                contents=text,
            )
            vector = response.embeddings[0].values

            records.append(
                {
                    "source": path.name,
                    "text": text,
                    "embedding": vector,
                }
            )

        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with self.index_path.open("w", encoding="utf-8") as f:
            json.dump(records, f)

        self.records = records
        return len(records)

    def _embed_query(self, query: str) -> np.ndarray:
        response = self.client.models.embed_content(
            model=settings.embedding_model,
            contents=query,
        )
        return np.asarray(response.embeddings[0].values, dtype=np.float32)

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        denom = float(np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom)

    def search(self, query: str, top_k: int | None = None) -> list[dict[str, Any]]:
        if not self.records:
            self.build_index()

        query_vector = self._embed_query(query)
        scored = []

        for record in self.records:
            doc_vector = np.asarray(record["embedding"], dtype=np.float32)
            score = self._cosine_similarity(query_vector, doc_vector)
            scored.append(
                {
                    "source": record["source"],
                    "text": record["text"],
                    "score": score,
                }
            )

        scored.sort(key=lambda item: item["score"], reverse=True)
        limit = top_k or settings.top_k
        return [
            item
            for item in scored[:limit]
            if item["score"] >= settings.min_similarity
        ]

    def search_as_text(self, query: str, top_k: int | None = None) -> str:
        results = self.search(query, top_k=top_k)
        if not results:
            return "No relevant knowledge-base article was found."

        chunks = []
        for item in results:
            chunks.append(
                f"SOURCE: {item['source']}\n"
                f"SIMILARITY: {item['score']:.3f}\n"
                f"{item['text']}"
            )

        return "\n\n---\n\n".join(chunks)
