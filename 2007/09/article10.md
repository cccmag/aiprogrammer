# 資訊檢索：向量空間模型

## 概述

向量空間模型（Vector Space Model）是資訊檢索的經典方法，將文件和查詢表示為向量，透過計算向量之間的相似度來進行檢索。2007 年，這個模型仍是搜尋引擎和文件檢索系統的重要基礎。

## 向量空間模型原理

```python
"""
資訊檢索概念展示
展示向量空間模型的原理
"""

def demo():
    print("=" * 50)
    print("資訊檢索概念展示")
    print("=" * 50)

    print("\n--- 文件表示 ---")
    print("""
文件轉換為向量的過程：

文件內容：
  "Python 是一種程式語言"

TF-IDF 向量：
  [0.0, 0.5, 0.3, 0.2, 0.4, 0.0, ...]
   python 程式 語言 資料 庫 ...

每個維度代表一個詞項，
值代表該詞項在文件中的權重。
""")

    print("\n--- TF-IDF 權重計算 ---")
    tfidf_code = """
# TF-IDF 計算
def tf(term, document):
    return document.count(term) / len(document.split())

def idf(term, corpus):
    N = len(corpus)
    df = sum(1 for doc in corpus if term in doc)
    return log(N / df)

def tfidf(term, document, corpus):
    return tf(term, document) * idf(term, corpus)

# 範例
corpus = [
    "Python 程式 語言",
    "Java 程式 語言",
    "資料庫 系統 設計"
]

doc = corpus[0]
tfidf("Python", doc, corpus)
"""
    print(tfidf_code)

    print("\n--- 向量相似度 ---")
    similarity = """
# 餘弦相似度
def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm1 = sqrt(sum(a * a for a in v1))
    norm2 = sqrt(sum(b * b for b in v2))
    return dot_product / (norm1 * norm2)

# 範例
doc1 = [0.5, 0.3, 0.2]
doc2 = [0.4, 0.4, 0.1]

similarity = cosine_similarity(doc1, doc2)
print(f"相似度: {similarity:.4f}")  # 輸出: 相似度: 0.9545
"""
    print(similarity)

    print("\n--- 文件檢索流程 ---")
    retrieval_steps = [
        "文件解析與預處理",
        "詞項抽取與正規化",
        "計算 TF-IDF 向量",
        "建立倒排索引",
        "查詢向量化",
        "計算相似度排名",
        "返回相關文件",
    ]
    for i, step in enumerate(retrieval_steps, 1):
        print(f"  {i}. {step}")

    print("\n--- 優點與限制 ---")
    pros_cons = {
        "優點": ["簡單直觀", "支持部分匹配", "高效檢索"],
        "限制": ["維度災難", "語義鴻溝", "假設詞項獨立"],
    }
    for category, items in pros_cons.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  - {item}")

    print("\n" + "=" * 50)
    print("資訊檢索概念展示完成")

if __name__ == "__main__":
    demo()