from pathlib import Path


def test_knowledge_base_has_articles():
    files = list(Path("knowledge_base").glob("*.md"))
    assert len(files) >= 8
