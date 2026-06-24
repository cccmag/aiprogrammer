# XLNet 與 RoBERTa

## 前言

2019 年中期，NLP 領域迎來了兩個重要的 BERT 挑戰者：Google/CMU 的 XLNet 和 Facebook 的 RoBERTa。這兩個模型在多個基準測試中超越了 BERT，進一步推動了預訓練技術的發展。本篇文章將深入探討這兩個模型的創新之處。

## XLNet

### 發布背景

2019 年 6 月，Google Brain 和 CMU 團隊發布了 XLNet，這是一個新的預訓練語言模型，在多項基準測試中超越了 BERT。

### 排列語言模型

XLNet 的核心創新是「排列語言模型」（Permutation Language Model）：

**BERT 的 MLM 問題**：
```
輸入：The [MASK] is a pet animal
問題：[MASK] token 在訓練時出現，但推斷時不出現
```

**XLNet 的解決方案**：
```
不使用 [MASK]，而是用排列組合

句子：The cat sat on the mat
可能的排列：cat sat on the mat the
             the mat on sat cat
             ...
```

XLNet 預測時不依賴 [MASK]，而是透過排列來學習雙向上下文。

### 雙向注意力與 Transformer-XL

XLNet 還借鑒了 Transformer-XL 的技術：

**分段遞迴機制**：
```python
# 處理長序列時重用之前的隱藏狀態
hidden_states = concat(prev_hidden, current_segment)
```

這使 XLNet 能夠處理更長的依賴關係。

### XLNet 的配置

| 配置 | 層數 | 隱藏維度 | 參數量 |
|------|------|----------|--------|
| XLNet BASE | 12 | 768 | 110M |
| XLNet LARGE | 18 | 1024 | 340M |

## RoBERTa

### 發布背景

2019 年 7 月，Facebook AI 發布了 RoBERTa（Robustly Optimized BERT Approach），這是對 BERT 的深度最佳化版本。RoBERTa 在多個基準測試中刷新紀錄。

### RoBERTa 的改進

RoBERTa 團隊認為 BERT 訓練不足是效能不如預期的原因，並進行了多項改進：

#### 1. 更多的訓練資料

RoBERTa 使用了更大的語料庫：
- **原始 BERT**：16GB
- **RoBERTa**：160GB（包含 Books Corpus、English Wikipedia、CC-News、OpenWebText、Stories）

#### 2. 更長時間訓練

- **原始 BERT**：1M 步，批次大小 256
- **RoBERTa**：500K 步，批次大小 8K

#### 3. 移除 Next Sentence Prediction

RoBERTa 發現 NSP 任務對效能沒有幫助，因此將其移除。

#### 4. 動態遮蔽

訓練時每次遇到一個序列就重新隨機遮蔽，而不是預先計算好遮蔽。

### RoBERTa 的效能

RoBERTa 在多個基準測試中超越了 BERT 和 XLNet：

| 基準 | BERT | XLNet | RoBERTa |
|------|------|-------|---------|
| MNLI | 86.2% | 89.8% | 90.2% |
| SST-2 | 93.5% | 95.6% | 95.3% |
| QNLI | 92.3% | 93.9% | 94.7% |

## 兩者的比較

### 設計理念

| 方面 | XLNet | RoBERTa |
|------|-------|---------|
| 核心創新 | 排列語言模型 | 訓練最佳化 |
| 注意力 | 雙向（透過排列） | 雙向 Transformer |
| 資料處理 | 標準 | 更大、更好 |

### 優勢比較

**XLNet 的優勢**：
- 更好地處理雙向依賴
- 在某些任務上表現更好

**RoBERTa 的優勢**：
- 訓練更穩定
- 在大多数任務上表現更好
- 訓練效率更高

## 對 NLP 領域的影響

### 最佳化成為主流

XLNet 和 RoBERTa 的成功告訴我們：

> 不僅要改變模型架構，還要在訓練過程中進行最佳化。

### 資料的重要性

RoBERTa 特別強調了訓練資料的重要性：

```
更多、更高品質的訓練資料 → 更好的模型效能
```

### 推動研究

這兩個模型的出現推動了後續研究：

- ELECTRA：更高效的預訓練
- ALBERT：引數共享
- Megatron-LM：更大規模訓練

## 結論

XLNet 和 RoBERTa 分別從不同角度推動了預訓練技術的發展。XLNet 的排列語言模型提供了一種新的學習雙向表示的方法，而 RoBERTa 的系統性最佳化展示了「細節決定成敗」的道理。這些工作為後續的研究奠定了重要基礎。

---

**延伸閱讀**

- [XLNet 論文](https://www.google.com/search?q=XLNet+language+model+2019)
- [RoBERTa 論文](https://www.google.com/search?q=RoBERTa+Facebook+2019)
- [XLNet vs BERT](https://www.google.com/search?q=XLNet+vs+RoBERTa+comparison)