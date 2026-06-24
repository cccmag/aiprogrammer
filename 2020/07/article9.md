# 小樣本學習的原理與應用

## 前言

Few-shot Learning（少樣本學習）是 2020 年 NLP 領域最重要的研究方向之一。本文深入探討其原理、方法和應用。

---

## 一、什麼是少樣本學習

### 1.1 傳統 ML vs Few-shot Learning

```
傳統 ML：
  需要：數千至數百萬範例
  訓練：從頭訓練或微調
  時間：數小時至數天

Few-shot Learning：
  需要：1 到 10 個範例
  訓練：無需梯度更新
  時間：秒級推理
```

### 1.2 少樣本學習的類型

| 類型 | 範例數量 | 說明 |
|------|---------|------|
| One-shot | 1 | 只看一次就學會 |
| Few-shot | 2-10 | 看少量範例 |
| Zero-shot | 0 | 只靠任務描述 |

---

## 二、核心原理

### 2.1 任務描述

Few-shot Learning 的核心是「任務」的概念：

```
任務 T：由支援集 S 和查詢集 Q 組成
  S = {(x_1, y_1), ..., (x_k, y_k)}  # k 個範例
  Q = {x_test}                        # 查詢範例
```

### 2.2 情境學習（In-context Learning）

GPT-3 採用的方法：

1. 將 k 個範例作為輸入的一部分
2. 模型從這些範例中推斷任務
3. 無需更新模型參數

```
輸入：
  "apple -> fruit
   banana -> fruit
   carrot -> vegetable
   dog -> ?"
  
輸出："animal"
```

### 2.3 度量學習（Metric Learning）

學習一個度量函數，比較新範例與已知範例：

```python
def similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)

def predict(query_embedding, support_set, k):
    similarities = [similarity(query_embedding, s.embedding) for s in support_set]
    top_k_indices = np.argsort(similarities)[-k:]
    return majority_vote([support_set[i].label for i in top_k_indices])
```

---

## 三、經典方法

### 3.1 Siamese Network

學習兩個輸入是否屬於同一類別：

```python
class SiameseNetwork:
    def __init__(self, encoder):
        self.encoder = encoder
        self.similarity_layer = Dense(1, activation='sigmoid')
    
    def forward(self, x1, x2):
        e1 = self.encoder(x1)
        e2 = self.encoder(x2)
        combined = tf.abs(e1 - e2)  # 或 tf.concat([e1, e2])
        return self.similarity_layer(combined)
```

### 3.2 Prototypical Networks

為每個類別計算原型：

```python
class PrototypicalNetwork:
    def forward(self, support, query):
        # 計算每個類別的原型
        prototypes = {}
        for label in support.labels:
            class_samples = support[label]
            prototypes[label] = mean(class_samples.embeddings)
        
        # 比較 query 與每個原型
        distances = {label: euclidean(query.embedding, proto) 
                     for label, proto in prototypes.items()}
        
        return min(distances, key=distances.get)
```

### 3.3 Matching Networks

使用注意力機制對支援集加權：

```python
def matching_network(query, support):
    attention_weights = softmax([
        attention(query, s.embedding) 
        for s in support
    ])
    
    weighted_sum = sum(w * s.embedding for w, s in zip(attention_weights, support))
    return classify(weighted_sum)
```

---

## 四、GPT-3 的 Few-shot 能力

### 4.1 為何 GPT-3 擅長 Few-shot

1. **大規模預訓練**：學習了豐富的語言表示
2. **Transformer 架構**：强大的上下文建模能力
3. **大量多樣化資料**：涵蓋了各種任務模式

### 4.2 GPT-3 的 Few-shot 評估

在多個 benchmark 上，GPT-3 的 Few-shot 結果與微調 SOTA 相當：

| 任務 | 微調 SOTA | GPT-3 Few-shot |
|------|----------|---------------|
| LAMBADA | 86.4% | 86.4% |
| TriviaQA | 68.9% | 71.2% |
| OpenBookQA | 74.0% | 73.2% |

---

## 五、應用場景

### 5.1 文字分類

```python
few_shot_classifier = pipeline(
    "text-classification",
    model="gpt2",
    task_template="Classify: {text} -> {labels}"
)

# 只要 2-3 個範例就能分類新類別
result = few_shot_classifier(
    "This is amazing!",
    examples=[
        ("I love it", "positive"),
        ("Terrible", "negative")
    ]
)
```

### 5.2 命名實體識別

```python
ner_task = "Extract entities from text: {text}\nEntities:"

examples = [
    ("John works at Google", "Person: John, Organization: Google"),
    ("Apple released new iPhone", "Organization: Apple, Product: iPhone")
]

result = gpt3.generate(few_shot_prompt.format(text="Microsoft acquired GitHub.", examples=...))
```

### 5.3 翻譯

```python
translation_prompt = """
English to French translation:
Dog -> chien
Cat -> chat
Bird -> oiseau
Computer ->"""
```

### 5.4 程式碼生成

```python
code_prompt = """
# Python function to calculate fibonacci
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# Haskell function to calculate fibonacci
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)

# Python function to reverse a list
def reverse(lst):"""
```

---

## 六、挑戰與限制

### 6.1 任務複雜度

Few-shot Learning 對簡單任務效果好，但複雜推理任務仍困難。

### 6.2 範例選擇

不同範例會顯著影響結果，需要精心設計。

### 6.3 標記噪聲

少量範例中的噪聲會被放大。

---

## 七、未來方向

1. **更高效的 Few-shot 方法**
2. **跨模態 Few-shot Learning**
3. **結構化知識的結合**

---

## 結語

Few-shot Learning 是 AI 發展的重要里程碑，它展示了我們可以通過「教學」而非「訓練」來利用大型模型的能力。這種新範式正在改變我們對 AI 系統設計的思考方式。

---

*延伸閱讀：[Few-shot+Learning+NLP+2020](https://www.google.com/search?q=few-shot+learning+NLP+GPT-3+2020)
[meta-learning+few-shot+survey](https://www.google.com/search?q=meta-learning+few-shot+survey+2020)*