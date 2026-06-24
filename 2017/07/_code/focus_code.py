#!/usr/bin/env python3
"""自然語言處理示範"""

def demo():
    print("=" * 50)
    print("自然語言處理示範")
    print("=" * 50)

    print("\n1. 文字預處理概念:")
    text = "Hello, World! I have 3 apples."
    words = text.lower().replace(",", "").replace("!", "").replace(".", "").split()
    print(f"   原文: {text}")
    print(f"   處理後: {words}")

    print("\n2. TF-IDF 概念:")
    documents = ["the cat sat", "the dog ran", "the cat and the dog"]
    print(f"   文件: {documents}")
    print(f"   詞彙: {set(' '.join(documents).split())}")

    print("\n3. 簡單文字分類:")
    train = [
        ("I love this", "positive"),
        ("Great product", "positive"),
        ("Terrible", "negative"),
        ("Worst ever", "negative"),
    ]
    for text, label in train:
        print(f"   '{text}' -> {label}")

    print("\n4. 情感分析概念:")
    sentiments = {"love": 0.8, "great": 0.7, "terrible": -0.8, "worst": -0.9}
    sample = "I love this great product"
    words = sample.lower().split()
    avg = sum(sentiments.get(w, 0) for w in words) / len(words)
    print(f"   文字: '{sample}'")
    print(f"   平均情感: {avg:.2f}")

    print("\n" + "=" * 50)
    print("NLP 示範完成")
    print("=" * 50)

if __name__ == "__main__":
    demo()