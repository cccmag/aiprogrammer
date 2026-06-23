"""
Mini Vector Database — from scratch in Python

Demonstrates: embeddings, cosine similarity, HNSW-like index, filtered search, RAG integration
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Vector Index — brute force (baseline)
# ---------------------------------------------------------------------------

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-10)


@dataclass
class Document:
    id: str
    text: str
    vector: list[float]
    metadata: dict = field(default_factory=dict)


class FlatIndex:
    """Brute-force vector index"""

    def __init__(self):
        self.documents: list[Document] = []

    def add(self, doc: Document):
        self.documents.append(doc)

    def search(self, query_vector: list[float], k: int = 5,
               filter_fn: Optional[callable] = None) -> list[tuple[Document, float]]:
        scored = []
        for doc in self.documents:
            if filter_fn and not filter_fn(doc.metadata):
                continue
            sim = cosine_similarity(query_vector, doc.vector)
            scored.append((doc, sim))
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


# ---------------------------------------------------------------------------
# HNSW-like Index (simplified)
# ---------------------------------------------------------------------------

class HNSWNode:
    def __init__(self, doc: Document, level: int):
        self.doc = doc
        self.level = level
        self.neighbors: dict[int, list['HNSWNode']] = {}  # level -> neighbors

class HNSWIndex:
    """Simplified HNSW (Hierarchical Navigable Small World) index"""

    def __init__(self, m: int = 5, m_max: int = 10, ef_construction: int = 100):
        self.m = m
        self.m_max = m_max
        self.ef_construction = ef_construction
        self.nodes: list[HNSWNode] = []
        self.max_level = 0
        self.enter_point: Optional[HNSWNode] = None

    def _random_level(self) -> int:
        level = -int(math.log(random.random()) * self.m)
        return min(level, 10)

    def add(self, doc: Document):
        level = self._random_level()
        node = HNSWNode(doc, level)
        self.nodes.append(node)

        if self.enter_point is None:
            self.enter_point = node
            self.max_level = level
            return

        # Find entry point neighbors at each level
        curr = self.enter_point
        for lvl in range(self.max_level, level, -1):
            curr = self._select_nearest(curr, doc.vector, 1, lvl)[0] if curr.neighbors.get(lvl) else curr

        for lvl in range(min(level, self.max_level), -1, -1):
            nearest = self._select_nearest(curr, doc.vector, self.ef_construction, lvl)
            neighbors = nearest[:self.m_max]
            node.neighbors[lvl] = neighbors
            for n in neighbors:
                if lvl not in n.neighbors:
                    n.neighbors[lvl] = []
                n.neighbors[lvl].append(node)
                if len(n.neighbors[lvl]) > self.m_max:
                    n.neighbors[lvl] = self._select_nearest(n, n.doc.vector, self.m_max, lvl)

        if level > self.max_level:
            self.max_level = level
            self.enter_point = node

    def _select_nearest(self, start: HNSWNode, query_vec: list[float],
                        k: int, level: int) -> list[HNSWNode]:
        candidates = [(start, cosine_similarity(query_vec, start.doc.vector))]
        visited = {start}
        result = []

        while candidates:
            candidates.sort(key=lambda x: -x[1])
            if len(result) >= k and candidates[0][1] < result[-1][1]:
                break
            node, _ = candidates.pop(0)
            for neighbor in node.neighbors.get(level, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    sim = cosine_similarity(query_vec, neighbor.doc.vector)
                    candidates.append((neighbor, sim))
                    result.append((neighbor, sim))
                    result.sort(key=lambda x: -x[1])
                    result = result[:k]

        return [n for n, _ in result]

    def search(self, query_vector: list[float], k: int = 5,
               filter_fn: Optional[callable] = None) -> list[tuple[Document, float]]:
        if not self.enter_point:
            return []
        candidates = self._select_nearest(self.enter_point, query_vector, k * 2, self.max_level)
        scored = [(node.doc, cosine_similarity(query_vector, node.doc.vector))
                  for node in candidates]
        if filter_fn:
            scored = [(d, s) for d, s in scored if filter_fn(d.metadata)]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


# ---------------------------------------------------------------------------
# Simple Embedder (simulated)
# ---------------------------------------------------------------------------

class SimpleEmbedder:
    """Simulated embedding model — returns random vectors (for demo only)"""

    def __init__(self, dim: int = 64):
        self.dim = dim

    def embed(self, text: str) -> list[float]:
        random.seed(hash(text) % (2**31))
        return [random.gauss(0, 1) for _ in range(self.dim)]


# ---------------------------------------------------------------------------
# Metadata Filtering
# ---------------------------------------------------------------------------

def tag_filter(tags: list[str]) -> callable:
    """Create a filter function that checks if doc has all specified tags"""
    def fn(metadata: dict) -> bool:
        doc_tags = metadata.get("tags", [])
        return all(t in doc_tags for t in tags)
    return fn


def date_filter(after: Optional[str] = None, before: Optional[str] = None) -> callable:
    """Create a date range filter"""
    def fn(metadata: dict) -> bool:
        date = metadata.get("date", "")
        if after and date < after:
            return False
        if before and date > before:
            return False
        return True
    return fn


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo():
    print("=== Mini Vector Database Demo ===\n")

    embedder = SimpleEmbedder(32)

    # Create documents
    docs = [
        Document("d1", "Transformer architecture uses attention mechanisms",
                 embedder.embed("transformer attention"), {"tags": ["ai", "nlp"], "date": "2017"}),
        Document("d2", "Vector databases enable semantic search",
                 embedder.embed("vector database semantic search"), {"tags": ["database", "ai"], "date": "2023"}),
        Document("d3", "RAG combines retrieval with generation",
                 embedder.embed("RAG retrieval generation"), {"tags": ["ai", "nlp", "rag"], "date": "2024"}),
        Document("d4", "PostgreSQL supports vector search via pgvector",
                 embedder.embed("postgres pgvector"), {"tags": ["database", "sql"], "date": "2023"}),
        Document("d5", "HNSW is a popular ANN algorithm",
                 embedder.embed("HNSW ANN algorithm"), {"tags": ["algorithm", "database"], "date": "2020"}),
        Document("d6", "Attention Is All You Need paper",
                 embedder.embed("attention is all you need"), {"tags": ["ai", "nlp", "paper"], "date": "2017"}),
        Document("d7", "Python is a popular programming language",
                 embedder.embed("python programming"), {"tags": ["programming"], "date": "1991"}),
    ]

    # Build index
    index = FlatIndex()
    for doc in docs:
        index.add(doc)

    # Search
    queries = [
        ("machine learning attention", None),
        ("database technology", None),
        ("AI retrieval", ["ai"]),
        ("NLP papers", ["nlp", "paper"]),
    ]

    for query_text, tags in queries:
        q_vec = embedder.embed(query_text)
        filter_fn = tag_filter(tags) if tags else None
        results = index.search(q_vec, k=2, filter_fn=filter_fn)

        filter_info = f" [tags: {tags}]" if tags else ""
        print(f"Query: '{query_text}'{filter_info}")
        for doc, score in results:
            print(f"  [{score:.4f}] {doc.text[:60]}...")
        print()

    # HNSW demo
    print("--- HNSW Index Demo ---")
    hnsw = HNSWIndex(m=3, m_max=5)
    for doc in docs:
        hnsw.add(doc)

    q_vec = embedder.embed("neural network attention")
    results = hnsw.search(q_vec, k=3)
    for doc, score in results:
        print(f"  [{score:.4f}] {doc.text[:60]}...")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
