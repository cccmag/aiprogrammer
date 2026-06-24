# 語言模型入門：從 Word2Vec 到 Beam Search

## 概述

本期的程式專案 `language_model.py` 是一個從零實作的語言模型套件，涵蓋了本期討論的四個核心概念：**Word2Vec（CBOW）**、**RNN 語言模型**、**Beam Search 解碼**和**困惑度評估**。

## 核心實作

### 1. CBOW（Continuous Bag-of-Words）

CBOW 是 Word2Vec 的兩種架構之一，透過上下文詞來預測目標詞：

```python
class CBOW:
    def forward(self, context_indices):
        # 對上下文詞向量取平均
        h = np.mean(self.W[context_indices], axis=0)
        # 投影到輸出層並計算 softmax
        u = h @ self.W2
        probs = softmax(u)
        return h, probs
```

**關鍵概念**：詞向量 `self.W` 是我們想學習的嵌入表示。訓練完成後，語義相近的詞會在向量空間中彼此靠近。

### 2. RNN 語言模型

基於循環神經網路的語言模型，使用上文的隱藏狀態來預測下一個詞：

```python
class RNNLM:
    def forward(self, inputs, hprev):
        for t in range(len(inputs)):
            xs[t] = one_hot(inputs[t])
            hs[t] = tanh(Wxh @ xs[t] + Whh @ hs[t-1] + bh)
            ps[t] = softmax(Why @ hs[t] + by)
        return hs, ps
```

**訓練方式**：使用 BPTT（Backpropagation Through Time）計算梯度，並透過交叉熵損失進行優化。

### 3. Beam Search 解碼

Beam Search 是比貪婪解碼更有效的生成策略，在每一步保留 k 個最可能的候選序列：

```python
def beam_search(model, start_idx, vocab_size, beam_width=3, max_len=10):
    sequences = [[[start_idx], 0.0]]
    for _ in range(max_len):
        for seq, score in sequences:
            # 對每個候選，擴展所有可能的下一詞
            probs = model.predict(seq[-1])
            for i in range(vocab_size):
                all_candidates.append((seq + [i], score - log(probs[i])))
        # 只保留 beam_width 個最佳候選
        sequences = sorted(all_candidates, key=lambda x: x[1])[:beam_width]
    return sequences
```

### 4. 困惑度（Perplexity）

困惑度是評估語言模型的標準指標，定義為交叉熵的指數：

```python
def perplexity(model, corpus_indices):
    total_loss = average_cross_entropy(model, corpus_indices)
    return exp(total_loss)
```

## 執行結果

```
=== Language Model Demo ===

--- CBOW Word2Vec ---
Epoch 0: loss=30.7609
Epoch 80: loss=24.4209

--- RNN Language Model ---
Epoch 0: loss=37.3504
Epoch 80: loss=32.2937

Perplexity on corpus: 5.2372

--- Beam Search Generation ---
Score=7.7762: the on the on the on the

Demo complete!
```

## 四合一的概念關聯

```
CBOW 詞嵌入
    ↓ 提供詞的向量表示
RNN 語言模型
    ↓ 生成下一個詞的機率分佈
Beam Search
    ↓ 在機率空間中搜尋最佳序列
困惑度（Perplexity）
    ↓ 評估生成品質的指標
```

## 延伸閱讀

- [完整程式碼](_code/language_model.py)
- [Word2Vec 原始論文](https://www.google.com/search?q=Efficient+Estimation+of+Word+Representations+in+Vector+Space)
- [RNN 語言模型教學](https://www.google.com/search?q=recurrent+neural+network+language+model+tutorial)
- [Beam Search 詳解](https://www.google.com/search?q=beam+search+decoding+nlp)
