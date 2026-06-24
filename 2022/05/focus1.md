# 語言模型導論：n-gram 到神經網路

## n-gram 語言模型

n-gram 語言模型是最經典的統計語言模型。其核心假設是：第 n 個詞出現的機率只與前 n-1 個詞有關：

```
P(w_i | w_1, ..., w_{i-1}) ≈ P(w_i | w_{i-n+1}, ..., w_{i-1})
```

例如在 bigram 模型中，我們只考慮前一個詞：

```
P("sat" | "the", "cat") ≈ P("sat" | "cat")
```

**平滑技術**：n-gram 模型面臨稀疏性問題——大部分 n-gram 從未在訓練語料中出現。常見的平滑方法包括：

- **Laplace 平滑**：每個 n-gram 計數加 1
- **Kneser-Ney 平滑**：基於上下文多樣性的更高級平滑
- **Stupid Backoff**：當高階 n-gram 不存在時退回低階模型

## 神經網路語言模型的優勢

神經網路語言模型透過分散式表示解決了 n-gram 的稀疏性問題：

```python
# n-gram 需要存儲所有出現過的詞序列
ngram_counts["the cat sat"] = 3
ngram_counts["the dog ran"] = 1

# 神經網路透過詞向量捕捉語義相似性
# "cat" 和 "dog" 的向量相似，所以模型可以泛化
```

**神經語言模型的關鍵優勢**：
1. **分散式表示**：每個詞由一個稠密向量表示，捕捉語義和語法特徵
2. **泛化能力**：相似的詞可以共享統計強度
3. **連續空間**：在連續向量空間中進行機率建模

## 從 Bengio 到現代架構

2003 年 Bengio 等人提出了第一個神經機率語言模型（NNLM），使用前饋神經網路：

```
lookup table (詞嵌入)
    → 隱藏層 (tanh)
    → softmax 輸出層
```

NNLM 證明了神經網路可以比 n-gram 取得更好的困惑度，但計算成本較高。後續的 RNN 語言模型（Mikolov 2010）進一步解決了固定上下文視窗的限制。

## 語言模型的評估：困惑度

困惑度（Perplexity, PPL）是語言模型最常用的評估指標：

```
PPL = exp(-1/N * sum(log P(w_i | context)))
```

困惑度越低，表示模型對測試資料的預測能力越強。一個均勻隨機模型的困惑度等於詞彙量大小。

## 小結

從 n-gram 到神經網路，語言模型的發展代表了從「離散計數」到「連續表示」的轉變。神經網路不僅解決了稀疏性問題，還為後續的詞嵌入、序列建模和預訓練技術奠定了基礎。

---

**下一步**：[Word2vec 與詞嵌入](focus2.md)

## 延伸閱讀

- [Statistical Language Models 簡介](https://www.google.com/search?q=statistical+language+model+n+gram)
- [Bengio NNLM 論文](https://www.google.com/search?q=Bengio+neural+probabilistic+language+model)
- [Perplexity 解釋](https://www.google.com/search?q=perplexity+language+model+evaluation)
