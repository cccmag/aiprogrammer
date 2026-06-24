# 鍵-值-查詢 機制

## 資訊檢索的類比

Query-Key-Value（QKV）是注意力機制的核心抽象。理解這個抽象的最好方式，是從資訊檢索系統的視角來思考。

### 資料庫查詢

想像你有一個資料庫，裡面儲存了許多文件，每份文件都有：
- **Key（鍵）**：文件的索引或標籤
- **Value（值）**：文件的實際內容

當你提出一個問題（Query，查詢）時：
1. 系統將你的查詢與所有文件的 Key 進行比對
2. 找到最相關的 Key
3. 返回對應的 Value

注意力機制將這個過程完全可微化：不是只選擇一個文件，而是對所有文件進行加權求和，權重由 Query 與 Key 的相似度決定。

## QKV 的數學定義

### 線性投影

在實際實現中，Q、K、V 是透過線性投影從輸入中得到的：

```
Q = X W_q      # 查詢投影
K = X W_k      # 鍵投影
V = X W_v      # 值投影
```

其中 W_q、W_k、W_v 是可學習的權重矩陣。

這種投影的設計有幾個重要的理由：

**角色分離**：即便 Query 和 Key 來自相同的輸入，透過不同的投影矩陣，它們可以學習不同的表示空間。

**維度控制**：投影允許將注意力計算的維度（d_k）與模型維度（d_model）解耦。

**容量擴展**：多個投影矩陣為模型提供了更多的可學習參數。

### QKV 的維度關係

在標準 Transformer 中：
- d_model：模型的隱藏維度（通常是 512 或 768）
- d_k：Key 的維度（通常是 d_model / h，其中 h 是注意力頭數）
- d_v：Value 的維度（通常等於 d_k）

保持 d_k 較小的原因：
1. 點積 Q K^T 的計算複雜度為 O(d_k)
2. 縮放因子 √d_k 的有效性依賴於 d_k 的大小
3. 不同注意力頭的 d_k 之和等於 d_model，確保了總參數量

## Query 的設計

### Query 的來源

Query 可以來自不同的上下文：

**Self-Attention 中的 Query**：
- 來自編碼器或解碼器當前層的輸出
- 每個位置的 Query 與所有位置的 Key 進行交互
- Query 和 Key 的表示空間可能不同（透過不同的投影矩陣）

**Cross-Attention 中的 Query**：
- 來自解碼器當前層的輸出
- Query 關注編碼器最後一層的輸出（Key 和 Value）
- 使得解碼器能夠獲取輸入序列的資訊

### Query 的作用

Query 的角色是「提問」。它決定了模型當前的「關注焦點」。在多頭注意力中，不同的頭實際上是在提出不同類型的問題：

- 頭 A：「當前的語法角色是什麼？」
- 頭 B：「當前的語義主題是什麼？」
- 頭 C：「當前位置與前置詞的關係是什麼？」

## Key 的設計

### Key 與 Query 的匹配

Key 的角色是「被匹配」。每個 Key 決定了對應位置能夠回應哪些 Query。如果一個位置的 Key 與某個 Query 的點積較大，這個位置就會在注意力中獲得較高的權重。

### 特殊的 Key 模式

研究發現，某些特殊 token（如 BERT 的 [CLS]）的 Key 往往與大量 Query 都有較高的匹配度，使它們成為注意力的「集散中心」。

## Value 的設計

### 值的實際內容

Value 是注意力機制最終傳遞的「資訊內容」。與 Key 不同，Value 不需要與 Query 直接交互——它只是在注意力權重確定後被加權求和。

這種設計實現了「關注與內容」的分離：Key 決定「是否被關注」，Value 決定「被關注時傳遞什麼」。

### Value 投影的重要性

Value 投影使得模型可以選擇性地壓縮或過濾被傳遞的資訊。例如，模型可以學習在不重要的細節上投以較低的 Value 權重。

## QKV 的擴展

### Multi-Query Attention

為了減少 KV 快取的記憶體消耗，Multi-Query Attention（Shazeer，2019）讓所有注意力頭共享相同的 K 和 V，但保留各自獨立的 Q：

```
共享 K, V：K_head₁ = K_head₂ = ... = K_headₕ
獨立 Q：Q_head₁ ≠ Q_head₂ ≠ ... ≠ Q_headₕ
```

這在推論時大幅減少了 KV 快取的記憶體開銷。

### Grouped-Query Attention

GQA（Ainslie 等人，2023）是 MQA 的折衷方案：將注意力頭分成 G 組，每組共享一組 KV：

```
G = 2：頭 1-4 共享 K₁,V₁，頭 5-8 共享 K₂,V₂
```

GQA 在模型品質和推論效率之間取得了良好的平衡，被 Llama 2/3 採用。

## 結論

QKV 機制是注意力架構中最優雅的設計之一。它將資訊檢索的概念轉化為一個完全可微的神經網路元件，並透過角色分離實現了靈活的設計空間。理解 QKV 的本質，是掌握現代注意力機制的關鍵。

---

**延伸閱讀**
- [Shazeer 2019: Fast Transformer Decoding with Multi-Query Attention](https://www.google.com/search?q=Multi+Query+Attention+2019)
- [GQA: Training Generalized Multi-Query Transformer Models](https://www.google.com/search?q=Grouped+Query+Attention+GQA)
- [Transformer QKV 詳解](https://www.google.com/search?q=transformer+query+key+value+explained)
