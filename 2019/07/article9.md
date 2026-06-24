# XLNet：超越 BERT 的自回歸預訓練

## 前言

2019 年 6 月，Google Brain 發布了 XLNet，這是又一個超越 BERT 的預訓練語言模型。XLNet 採用了一種新穎的自回歸預訓練方法，結合了 BERT 和傳統語言模型的優點。

## XLNet 的核心思想

### 解決 BERT 的問題

BERT 的 MLM（遮罩語言模型）有一個根本問題：

```
問題：預訓練和微調之間的不一致

預訓練時：[MASK] token 是人造的
微調時：[MASK] token 不存在

這導致預訓練和微調之間存在 gap
```

### 排列語言模型（Permutation Language Model）

XLNet 提出了排列語言模型來解決這個問題：

```python
# BERT 的方式
# 輸入: "The cat [MASK] on the mat"
# 預測: "sat"

# XLNet 的方式
# 對於句子 "The cat sat on the mat"
# 隨機排列: "sat The cat on mat the"
# 輸入: "sat The cat on mat" (可以看到部分上下文)
# 預測: "the" (不能看到目標詞)
```

### 雙向上下文

```
┌─────────────────────────────────────────────────────┐
│           XLNet 的雙向上下文                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   假設排列為: [x1, x3, x4, x2, x5]                  │
│                                                     │
│   預測 x2 時可以看到: x1, x3, x4                    │
│   預測 x5 時可以看到: x1, x3, x4, x2                │
│                                                     │
│   這樣每個詞都可以「看到」雙向上下文，                │
│   同時保持自回歸的形式！                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 架構改進

### Transformer-XL

XLNet 使用了 Transformer-XL 的架構，解決了固定長度上下文的問題：

```python
# Transformer-XL 的循環機制
# 記憶單元
memory = [h_{t-1}, h_{t-2}, ..., h_{t-n}]

# 新的隱藏狀態
h_t = Attention(Q(h_t), K([memory; h_t]), V([memory; h_t]))
```

### 優勢

```python
# Transformer-XL 的優勢
xlnet_advantages = {
    "長期依賴": "可以處理任意長度的文本",
    "效率": "重用之前的計算結果",
    "一致性": "解決碎片化問題",
}
```

---

## 實驗結果

### 在 GLUE 上的表現

| 模型 | 資料 | SQuAD 2.0 | MNLI | SST-2 |
|------|------|-----------|------|-------|
| BERT-base | 13GB | 83.1% | 86.7% | 94.9% |
| XLNet-base | 126GB | 86.1% | 87.8% | 95.4% |

### 大模型對比

| 模型 | 參數量 | SQuAD 2.0 | RTE |
|------|--------|-----------|-----|
| BERT-large | 340M | 86.3% | 70.4% |
| RoBERTa-large | 355M | 89.4% | 79.4% |
| XLNet-large | 340M | 89.8% | 83.8% |

---

## 與 BERT 的比較

### 對比表格

```
┌─────────────────────────────────────────────────────┐
│              BERT vs XLNet                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   項目           BERT          XLNet               │
│   ────────────────────────────────────────────────  │
│   預訓練任務     MLM          Permutation LM       │
│   雙向性        遮罩         排列實現               │
│   架構          Transformer  Transformer-XL        │
│   長文本        固定長度      循環機制               │
│   數據需求      13GB         126GB                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 結語

XLNet 的貢獻在於：

1. **創新的預訓練方式**：透過排列實現雙向建模
2. **引入 Transformer-XL**：解決長期依賴問題
3. **更大的訓練數據**：展示數據規模的重要性

XLNet 和 BERT 的競爭推動了預訓練模型的快速發展。

---

**延伸閱讀**

- [XLNet Paper](https://www.google.com/search?q=XLNet+paper+Google+Brain)
- [Transformer-XL](https://www.google.com/search?q=Transformer+XL+paper)
- [XLNet+vs+BERT](https://www.google.com/search?q=XLNet+vs+BERT+comparison)