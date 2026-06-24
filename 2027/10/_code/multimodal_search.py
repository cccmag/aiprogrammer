"""
Mini Multi-Modal Search Engine — from scratch in Python

Demonstrates: multi-modal embedding (simulated), cross-modal search,
image-text similarity, and multimodal RAG.
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Simulated Embeddings (in production, use CLIP / ImageBind / etc.)
# ---------------------------------------------------------------------------

class MultiModalEmbedder:
    """Simulated multi-modal embedder — same dim for all modalities"""

    def __init__(self, dim: int = 64):
        self.dim = dim

    def embed_text(self, text: str) -> list[float]:
        random.seed(hash(text) % (2**31))
        return [random.gauss(0, 1) for _ in range(self.dim)]

    def embed_image(self, caption: str) -> list[float]:
        random.seed(hash(f"img_{caption}") % (2**31))
        return [random.gauss(0, 1) for _ in range(self.dim)]

    def embed_audio(self, caption: str) -> list[float]:
        random.seed(hash(f"audio_{caption}") % (2**31))
        return [random.gauss(0, 1) for _ in range(self.dim)]


# ---------------------------------------------------------------------------
# Cosine similarity (reused)
# ---------------------------------------------------------------------------

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-10)


@dataclass
class MultiModalItem:
    id: str
    text: str
    modality: str  # text / image / audio
    vector: list[float]
    metadata: dict = field(default_factory=dict)


class MultiModalIndex:
    """Cross-modal search index — embed everything to shared space"""

    def __init__(self):
        self.items: list[MultiModalItem] = []

    def add(self, item: MultiModalItem):
        self.items.append(item)

    def search(self, query_vector: list[float], k: int = 5,
               modality: Optional[str] = None) -> list[tuple[MultiModalItem, float]]:
        scored = []
        for item in self.items:
            if modality and item.modality != modality:
                continue
            sim = cosine_similarity(query_vector, item.vector)
            scored.append((item, sim))
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


# ---------------------------------------------------------------------------
# Simple CLIP-like training simulation
# ---------------------------------------------------------------------------

def contrastive_loss(text_embs: list[list[float]], image_embs: list[list[float]],
                     temperature: float = 0.07) -> float:
    """Simulated InfoNCE loss — higher = better alignment"""
    scores = []
    n = min(len(text_embs), len(image_embs))
    for i in range(n):
        sim_pos = cosine_similarity(text_embs[i], image_embs[i])
        sim_neg = max(
            cosine_similarity(text_embs[i], image_embs[(i + 1) % n]),
            cosine_similarity(text_embs[(i + 1) % n], image_embs[i])
        )
        scores.append(sim_pos - sim_neg)
    return sum(scores) / len(scores)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo():
    print("=== Multi-Modal Search Engine Demo ===\n")

    embedder = MultiModalEmbedder(32)

    items = [
        MultiModalItem("t1", "A cat sitting on a windowsill", "text",
                       embedder.embed_text("cat windowsill"),
                       {"lang": "en"}),
        MultiModalItem("t2", "A dog running in the park", "text",
                       embedder.embed_text("dog park"),
                       {"lang": "en"}),
        MultiModalItem("i1", "cat on windowsill (image)", "image",
                       embedder.embed_image("cat windowsill"),
                       {"format": "jpg"}),
        MultiModalItem("i2", "dog in park (image)", "image",
                       embedder.embed_image("dog park"),
                       {"format": "jpg"}),
        MultiModalItem("i3", "sunset over mountains (image)", "image",
                       embedder.embed_image("sunset mountains"),
                       {"format": "png"}),
        MultiModalItem("a1", "cat meowing (audio)", "audio",
                       embedder.embed_audio("cat meowing"),
                       {"duration": 3.2}),
        MultiModalItem("a2", "dog barking (audio)", "audio",
                       embedder.embed_audio("dog barking"),
                       {"duration": 2.1}),
    ]

    index = MultiModalIndex()
    for item in items:
        index.add(item)

    # Cross-modal search: text query -> images
    print("1. Text query → Images:")
    q_vec = embedder.embed_text("a pet animal")
    results = index.search(q_vec, k=3, modality="image")
    for item, score in results:
        print(f"  [{score:.4f}] {item.text} ({item.modality})")

    # Cross-modal search: text query -> audio
    print("\n2. Text query → Audio:")
    q_vec = embedder.embed_text("animal sounds")
    results = index.search(q_vec, k=2, modality="audio")
    for item, score in results:
        print(f"  [{score:.4f}] {item.text} ({item.modality})")

    # All-modality search
    print("\n3. Text query → All modalities:")
    q_vec = embedder.embed_text("nature outdoor scenery")
    results = index.search(q_vec, k=4)
    for item, score in results:
        print(f"  [{score:.4f}] {item.text} ({item.modality})")

    # Image query -> text (reverse cross-modal)
    print("\n4. Image query → Text:")
    q_vec = embedder.embed_image("cat looking outside")
    results = index.search(q_vec, k=2, modality="text")
    for item, score in results:
        print(f"  [{score:.4f}] {item.text} ({item.modality})")

    # Contrastive loss demo
    print("\n5. Contrastive Loss (CLIP-style):")
    text_embs = [embedder.embed_text("cat"), embedder.embed_text("dog"),
                 embedder.embed_text("sunset")]
    image_embs = [embedder.embed_image("cat"), embedder.embed_image("dog"),
                  embedder.embed_image("sunset")]
    loss = contrastive_loss(text_embs, image_embs)
    print(f"  Alignment score: {loss:.4f} (higher = better pairs)")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
