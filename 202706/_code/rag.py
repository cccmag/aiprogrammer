"""
Mini RAG (Retrieval-Augmented Generation) — from scratch in Python
Demonstrates: embedding, vector search, context augmentation
"""

import numpy as np

# ---------------------------------------------------------------------------
# Simple embedding model (random projections as a stand-in)
# ---------------------------------------------------------------------------

class SimpleEmbedder:
    """A simple embedder using random projections (for demo only)"""
    def __init__(self, vocab_size, d_embed=16):
        # In practice, use sentence-transformers or OpenAI embeddings
        self.embeddings = np.random.randn(vocab_size, d_embed) * 0.01
        self.d_embed = d_embed

    def embed(self, text, char_to_idx):
        """Average character embeddings as a simple document embedding"""
        indices = [char_to_idx.get(c, 0) for c in text]
        if not indices:
            return np.zeros(self.d_embed)
        return np.mean(self.embeddings[indices], axis=0)

# ---------------------------------------------------------------------------
# Simple Vector Store
# ---------------------------------------------------------------------------

class VectorStore:
    """Simple in-memory vector store with cosine similarity search"""
    def __init__(self):
        self.documents = []
        self.vectors = []

    def add(self, document, vector):
        self.documents.append(document)
        self.vectors.append(vector)

    def search(self, query_vector, k=3):
        """Search top-k most similar documents"""
        if not self.vectors:
            return []
        vectors = np.array(self.vectors)
        query_norm = query_vector / (np.linalg.norm(query_vector) + 1e-8)
        vec_norms = vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-8)
        scores = vec_norms @ query_norm
        top_indices = np.argsort(scores)[-k:][::-1]
        return [(self.documents[i], scores[i]) for i in top_indices]

# ---------------------------------------------------------------------------
# Mini RAG System
# ---------------------------------------------------------------------------

class MiniRAG:
    """Retrieval-Augmented Generation demo system"""
    def __init__(self, vocab_size, char_to_idx):
        self.embedder = SimpleEmbedder(vocab_size)
        self.store = VectorStore()
        self.char_to_idx = char_to_idx

    def index_documents(self, documents):
        """Index a list of documents"""
        for doc in documents:
            vec = self.embedder.embed(doc, self.char_to_idx)
            self.store.add(doc, vec)
        print(f"Indexed {len(documents)} documents")

    def query(self, question, k=2):
        """Retrieve relevant documents for a question"""
        q_vec = self.embedder.embed(question, self.char_to_idx)
        results = self.store.search(q_vec, k=k)
        return results

# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo():
    chars = " abcdefghijklmnopqrstuvwxyz.,!?\n0123456789"
    char_to_idx = {c: i for i, c in enumerate(chars)}

    print("=== Mini RAG Demo ===\n")

    # Create knowledge base
    documents = [
        "the transformer model uses attention mechanisms.",
        "attention allows the model to focus on relevant parts of the input.",
        "multi head attention runs multiple attention operations in parallel.",
        "the feed forward network applies to each position separately.",
        "layer normalization stabilizes training in deep networks.",
        "positional encoding gives the model information about token order.",
        "the encoder processes the input sequence in transformer models.",
        "the decoder generates output tokens one at a time.",
        "self attention relates different positions of the same sequence.",
        "cross attention relates encoder and decoder representations.",
        "residual connections help gradients flow through deep networks.",
        "dropout prevents overfitting during neural network training.",
        "the adam optimizer adapts learning rates for each parameter.",
        "beam search finds the most likely sequence in generation.",
        "temperature controls randomness in text generation output.",
    ]

    rag = MiniRAG(len(chars), char_to_idx)
    rag.index_documents(documents)

    questions = [
        "what is attention",
        "how does multi head attention work",
        "what is positional encoding",
        "tell me about the decoder",
        "what helps with deep network training",
    ]

    for q in questions:
        print(f"\nQuestion: {q}")
        results = rag.query(q, k=2)
        for doc, score in results:
            print(f"  [{score:.3f}] {doc}")

    # Simulate RAG-augmented response
    print("\n--- RAG-Augmented Response ---")
    q = "how does attention work"
    results = rag.query(q, k=2)
    context = "\n".join(doc for doc, _ in results)
    print(f"Question: {q}")
    print(f"Retrieved context:\n  {context}")
    print(f"Response (simulated): Based on the retrieved information, "
          f"attention mechanisms allow the model to focus on relevant parts of the input. "
          f"Multi-head attention runs multiple attention operations in parallel.")

if __name__ == "__main__":
    demo()
