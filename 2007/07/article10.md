# 自然語言處理：NLTK 庫的興起

## 概述

2007 年，Python 的 Natural Language Toolkit (NLTK) 已經成為自然語言處理領域的重要工具。NLTK 提供了豐富的文字處理功能、語料庫和教育資源，使 NLP 的學習和應用變得更加容易。

## NLTK 的設計理念

NLTK 的核心目標是「讓電腦處理人類語言變得簡單」：

```python
"""
NLTK 基礎展示
自然語言處理的入門介紹
"""

def demo():
    print("=" * 50)
    print("NLTK 自然語言處理展示")
    print("=" * 50)

    print("\n--- 文字標記化 (Tokenization) ---")
    print("""
# 句子標記化
text = "Natural language processing is fascinating. NLTK makes it easy!"
sentences = nltk.sent_tokenize(text)
# ['Natural language processing is fascinating.', 'NLTK makes it easy!']

# 單字標記化
words = nltk.word_tokenize(text)
# ['Natural', 'language', 'processing', 'is', 'fascinating', '.', 'NLTK', ...]
""")

    print("\n--- 詞性標記 (POS Tagging) ---")
    print("""
# 詞性標記
text = "The quick brown fox jumps over the lazy dog"
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
# [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'),
#  ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]
""")

    print("\n--- 名實體辨識 (Named Entity Recognition) ---")
    print("""
# 辨識人名、地名、組織
text = "Apple Inc. was founded by Steve Jobs in California."
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
entities = nltk.ne_chunk(tagged)
# 輸出：(ORGANIZATION Apple/NNP Inc./NNP)
#       (PERSON Steve/NNP Jobs/NNP)
#       (GPE California/NNP)
""")

    print("\n--- 文字頻率分析 ---")
    print("""
# 計算單字頻率
from collections import Counter

text = "the quick brown fox jumps over the lazy dog the quick brown fox"
words = nltk.word_tokenize(text.lower())
word_freq = Counter(words)
# Counter({'the': 3, 'quick': 2, 'brown': 2, 'fox': 2, ...})

# 最常見的單字
print(word_freq.most_common(5))
""")

    print("\n--- 語料庫範例 ---")
    print("""
# 使用內建語料庫
from nltk.corpus import brown

# 查看語料庫資訊
print("Brown 語料庫:")
print(f"  類別: {brown.categories()}")
print(f"  字數: {len(brown.words())}")
print(f"  句數: {len(brown.sents())}")

# 條件頻率分佈
cfd = nltk.ConditionalFreqDist(
    (genre, word)
    for genre in brown.categories()
    for word in brown.words(genre)
)
print(f"  文法類別新聞中的 'can': {cfd['news']['can']}")
""")

    print("\n--- 簡單的文字分類 ---")
    print("""
# 使用 Naive Bayes 分類器
from nltk.classify import NaiveBayesClassifier

# 訓練資料
training_data = [
    ('I love this movie', 'positive'),
    ('This movie is great', 'positive'),
    ('I hate this film', 'negative'),
    ('Terrible movie', 'negative'),
]

# 文字轉特徵（簡單的單字包模型）
def extract_features(text):
    words = set(nltk.word_tokenize(text.lower()))
    return {word: True for word in words}

# 訓練分類器
featuresets = [(extract_features(text), label) for (text, label) in training_data]
classifier = nltk.NaiveBayesClassifier.train(featuresets)

# 測試
test_text = "I really like this movie"
print(f"'{test_text}' 分類為: {classifier.classify(extract_features(test_text))}")
""")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    demo()