# 實作：簡單的 NLP 模型

## 程式概述

本程式中，我們將用 Python 實作一個簡單的詞嵌入模型，展示自然語言處理的基本概念。

## 實作內容

1. **詞嵌入（Word Embedding）**：將單詞映射為向量
2. **Softmax 分類**：簡單的多類別分類
3. **Skip-gram 模型**：Word2Vec 的簡化版本

## 程式碼

```python
#!/usr/bin/env python3
"""簡單的 NLP 模型實作"""

import math
import random

class SimpleEmbeddings:
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

class SoftmaxClassifier:
    def __init__(self, input_dim, num_classes):
        self.weights = [[random.uniform(-0.1, 0.1) for _ in range(num_classes)]
                        for _ in range(input_dim)]
        self.biases = [0.0] * num_classes

    def softmax(self, scores):
        max_score = max(scores)
        exp_scores = [math.exp(s - max_score) for s in scores]
        sum_exp = sum(exp_scores)
        return [e / sum_exp for e in exp_scores]

    def predict(self, features):
        scores = [sum(f * w for f, w in zip(features, self.weights[i])) + self.biases[i]
                  for i in range(len(self.weights))]
        return self.softmax(scores)

class SkipGramModel:
    def __init__(self, vocab_size, embedding_dim, window_size):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window_size = window_size
        self.embeddings = SimpleEmbeddings(vocab_size, embedding_dim)
        self.context_embeddings = SimpleEmbeddings(vocab_size, embedding_dim)

    def get_context_words(self, words, center_idx):
        context = []
        for i in range(center_idx - self.window_size, center_idx + self.window_size + 1):
            if i != center_idx and 0 <= i < len(words):
                context.append(words[i])
        return context

    def forward(self, center_word_idx):
        center_vec = self.embeddings.get_embedding(center_word_idx)
        return center_vec

    def negative_sampling_loss(self, center_vec, context_word_idx, negative_samples):
        pos_score = self.context_embeddings.get_embedding(context_word_idx)
        pos_sim = sum(c * p for c, p in zip(center_vec, pos_sim))

        neg_loss = 0.0
        for neg_idx in negative_samples:
            neg_vec = self.context_embeddings.get_embedding(neg_idx)
            neg_sim = sum(c * n for c, n in zip(center_vec, neg_vec))
            neg_loss += math.log(1 + math.exp(-neg_sim))
        return -pos_sim + neg_loss

def demo():
    print("=" * 50)
    print("簡單 NLP 模型演示")
    print("=" * 50)

    vocab = ["the", "cat", "sat", "on", "mat", "dog", "ran", "hill"]
    word_to_idx = {w: i for i, w in enumerate(vocab)}

    print("\n1. 詞嵌入演示")
    print("-" * 30)
    embedding_dim = 8
    model = SimpleEmbeddings(len(vocab), embedding_dim)
    for word, idx in word_to_idx.items():
        vec = model.get_embedding(idx)
        print(f"{word}: {vec[:3]}...")

    print("\n2. 詞彙相似度演示")
    print("-" * 30)
    cat_idx = word_to_idx["cat"]
    dog_idx = word_to_idx["dog"]
    cat_vec = model.get_embedding(cat_idx)
    dog_vec = model.get_embedding(dog_idx)
    sim = model.cosine_similarity(cat_vec, dog_vec)
    print(f"cat 與 dog 的相似度: {sim:.4f}")

    print("\n3. Skip-gram 模型演示")
    print("-" * 30)
    sentence = ["the", "cat", "sat", "on", "the", "mat"]
    window_size = 2
    sg = SkipGramModel(len(vocab), embedding_dim, window_size)
    print(f"句子: {sentence}")
    print(f"視窗大小: {window_size}")

    center_idx = 2  # "sat"
    center_word = sentence[center_idx]
    context_words = sg.get_context_words(sentence, center_idx)
    print(f"中心詞: '{center_word}' (idx={word_to_idx[center_word]})")
    print(f"上下文詞: {context_words}")

    print("\n4. Softmax 分類演示")
    print("-" * 30)
    classifier = SoftmaxClassifier(embedding_dim, num_classes=5)
    test_features = model.get_embedding(cat_idx)
    probs = classifier.predict(test_features)
    print(f"輸入特徵維度: {len(test_features)}")
    print(f"輸出類別數: {len(probs)}")
    print(f"類別機率分佈: {[f'{p:.4f}' for p in probs]}")

    print("\n5. 詞嵌入可視化（降維投影）")
    print("-" * 30)
    print("三維投影（取前三維）：")
    for word, idx in word_to_idx.items():
        vec = model.get_embedding(idx)
        proj = vec[:3]
        print(f"  {word}: [{proj[0]:+.3f}, {proj[1]:+.3f}, {proj[2]:+.3f}]")

    print("\n" + "=" * 50)
    print("演示完成")
    print("=" * 50)

if __name__ == "__main__":
    demo()