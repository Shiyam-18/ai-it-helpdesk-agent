from dotenv import load_dotenv

load_dotenv()

from src.config import settings
from src.rag import KnowledgeBase


def main() -> None:
    kb = KnowledgeBase()
    count = kb.build_index()
    print(f"Built RAG index for {count} documents.")
    print(f"Saved to: {settings.index_path}")


if __name__ == "__main__":
    main()
