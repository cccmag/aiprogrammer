#!/usr/bin/env python3
"""NLP Demo: Word Embeddings and Simple Attention"""

import math
import random

class WordEmbedding:
    def __init__(self, vocab_size, embedding_dim):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.embeddings = [[random.uniform(-0.5, 0.5) for _ in range(embedding_dim)]
                           for _ in range(vocab_size)]

    def get_embedding(self, word_idx):
        return self.embeddings[word_idx]

    def cosine_similarity(self, vec1, vec2):
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(a * a for a in vec2))
        return dot / (norm1 * norm2 + 1e-8)

class SimpleAttention:
    def softmax(self, x):
        exp_x = [math.exp(val - max(x)) for val in x]
        sum_exp = sum(exp_x)
        return [val / sum_exp for val in exp_x]

    def forward(self, query, keys, values):
        scores = []
        for key in keys:
            score = sum(q * k for q, k in zip(query, key))
            scores.append(score)

        attn_weights = self.softmax(scores)

        output = [0.0] * len(values[0])
        for weight, value in zip(attn_weights, values):
            for i, v in enumerate(value):
                output[i] += weight * v

        return output, attn_weights

def demo():
    print("=" * 50)
    print("NLP Demo: Word Embeddings and Attention")
    print("=" * 50)

    vocab = ["king", "queen", "man", "woman", "prince", "princess"]
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    embedding_dim = 6

    model = WordEmbedding(len(vocab), embedding_dim)

    print("\n1. Word Embeddings:")
    print("-" * 30)
    for word, idx in word_to_idx.items():
        vec = model.get_embedding(idx)
        print(f"  {word}: [{vec[0]:+.3f}, {vec[1]:+.3f}, ...]")

    print("\n2. Similarity Analysis:")
    print("-" * 30)
    king_vec = model.get_embedding(word_to_idx["king"])
    queen_vec = model.get_embedding(word_to_idx["queen"])
    man_vec = model.get_embedding(word_to_idx["man"])
    woman_vec = model.get_embedding(word_to_idx["woman"])

    sim_king_queen = model.cosine_similarity(king_vec, queen_vec)
    sim_king_man = model.cosine_similarity(king_vec, man_vec)
    sim_queen_woman = model.cosine_similarity(queen_vec, woman_vec)

    print(f"  king vs queen:  {sim_king_queen:.4f}")
    print(f"  king vs man:    {sim_king_man:.4f}")
    print(f"  queen vs woman: {sim_queen_woman:.4f}")

    print("\n3. Simple Attention Demo:")
    print("-" * 30)
    attention = SimpleAttention()

    query = model.get_embedding(word_to_idx["king"])
    keys = [model.get_embedding(word_to_idx["queen"]),
            model.get_embedding(word_to_idx["man"]),
            model.get_embedding(word_to_idx["woman"])]
    values = keys[:]

    output, weights = attention.forward(query, keys, values)

    print(f"  Query: king")
    print(f"  Keys: queen, man, woman")
    print(f"  Attention weights: {weights}")

    print("\n4. Vector Arithmetic (Conceptual):")
    print("-" * 30)
    print("  king - man + woman ≈ queen")
    print("  (demonstrates word2vec-style relationships)")

    print("\n5. Attention Visualization:")
    print("-" * 30)
    print("  Attention scores for 'king' querying others:")
    for word, w in zip(["queen", "man", "woman"], weights):
        bar = "#" * int(w * 30)
        print(f"    {word:8s}: {bar} ({w:.3f})")

    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)

if __name__ == "__main__":
    demo()