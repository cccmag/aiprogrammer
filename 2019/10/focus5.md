# ALBERT 與模型優化

## 前言

隨著預訓練模型規模不斷增大，模型壓縮和優化成為重要研究方向。2019 年 9 月，Google 發布了 ALBERT（A Lite BERT），提出了一種高效的輕量級 BERT 變體。本篇文章將探討 ALBERT 的設計理念和模型優化技術。

## 模型規模的挑戰

### BERT 模型的規模

預訓練模型的規模不斷增大：

| 模型 | 參數量 |
|------|--------|
| BERT BASE | 110M |
| BERT LARGE | 340M |
| GPT-2 | 1.5B |
| T5 | 11B |

### 規模帶來的問題

1. **記憶體限制**：大模型需要大量 GPU 記憶體
2. **訓練速度**：訓練時間隨模型規模線性增長
3. **部署成本**：在邊緣裝置上部署困難

## ALBERT 的設計

### 核心創新：引數共享

ALBERT 的主要創新是跨層引數共享（Cross-layer Parameter Sharing）：

```
BERT：每層有獨立的注意力權重和前饋網路權重
ALBERT：所有層共享相同的注意力權重和前饋網路權重
```

### 對比示意

```
BERT LARGE（24層）：
Layer 1: W_attn, W_ff
Layer 2: W_attn, W_ff
...
Layer 24: W_attn, W_ff
總共：24 × 2 = 48 組權重

ALBERT BASE（12層）：
Layer 1-12: 共享 W_attn, W_ff
總共：1 組權重
```

### 減少的效果

ALBERT BASE 僅有 12M 參數，遠小於 BERT BASE 的 110M：

| 組件 | BERT BASE | ALBERT BASE |
|------|-----------|-------------|
| 嵌入層 | 23M | 23M |
| 注意力 | 36M | 3.8M |
| 前饋網路 | 85M | 3.8M |
| 其他 | 1M | 1M |
| **總計** | **110M** | **12M** |

## 句子順序預測（SOP）

### NSP 的問題

ALBERT 的另一個創新是替換 Next Sentence Prediction（NSP）為 Sentence Order Prediction（SOP）。

研究發現：
- NSP 任務相對簡單（主題預測 vs 連貫性預測）
- NSP 可能會引入偽負例

### SOP 的設計

SOP 使用兩個相鄰的段落作為正樣本，交換順序後作為負樣本：

```
正樣本：段落 A + 段落 B
負樣本：段落 B + 段落 A
```

這要求模型學習細緻的連貫性差異。

## 模型蒸餾

### DistilBERT

除了 ALBERT，另一種流行的模型壓縮技術是蒸餾（Distillation）。

DistilBERT 的做法：
- 使用 BERT 作為教師模型
- 訓練一個較小的學生模型
- 學生模型學習教師模型的行為

```
DistilBERT：
- 參數量：66M（BERT 的 60%）
- 效能：保留 97% 的效能
- 訓練速度：提升 60%
```

### TinyBERT

華為諾亞方舟實驗室提出了 TinyBERT：

- 4 層 Transformer
- 隱藏維度 312
- 在 GLUE 上達到 BERT 96% 的效能

## 其他優化技術

### 權重剪枝

```python
# 結構化剪枝示例
# 移除注意力頭
for head in heads_to_remove:
    del attention_weights[head]
```

### 量化

```
FP32（32位浮點）→ INT8（8位整數）
記憶體減少：4x
效能損失：<1%
```

### 知識蒸餾

知識蒸餾的核心思想是讓小模型學習大模型的「暗知識」：

```python
# 蒸餾損失
loss = alpha * KL(student_logits, teacher_logits) + (1-alpha) * CE(student_logits, labels)
```

## ALBERT 的效能

### GLUE 基準測試

| 模型 | 參數量 | GLUE 分數 |
|------|--------|-----------|
| BERT BASE | 110M | 79.6 |
| ALBERT BASE | 12M | 82.3 |
| BERT LARGE | 340M | 86.2 |
| ALBERT LARGE | 18M | 88.7 |

### 訓練效率

ALBERT 的訓練效率顯著提升：

```
ALBERT BASE vs BERT BASE：
- 訓練記憶體：減少 70%
- 訓練時間：減少 60%
```

## 結論

ALBERT 展示了模型優化的多種可能性：

1. **引數共享**：大幅減少參數量
2. **SOP**：更好的預訓練信號
3. **蒸餾**：壓縮模型的通用方法

這些技術為在資源受限環境中部署大型模型提供了可能。

---

**延伸閱讀**

- [ALBERT 論文](https://www.google.com/search?q=ALBERT+Google+2019)
- [模型蒸餾 DistilBERT](https://www.google.com/search?q=DistilBERT+knowledge+distillation)
- [模型壓縮技術](https://www.google.com/search?q=model+compression+neural+network)