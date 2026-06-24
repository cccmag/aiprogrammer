# 模型剪枝與蒸餾（2017-2028）

## 剪枝：去除冗餘參數

剪枝的概念來自生物神經科學：人腦會定期修剪不常用的神經連結。同樣地，神經網路中有大量參數對最終結果貢獻極小。

## 剪枝策略

**非結構化剪枝：** 將權重矩陣中接近零的元素設為零。稀疏度可達 90%，但需要特殊硬體支援。

```python
import numpy as np

def magnitude_prune(weights, sparsity=0.5):
    threshold = np.percentile(np.abs(weights), sparsity * 100)
    pruned = np.where(np.abs(weights) < threshold, 0, weights)
    return pruned

# 結構化剪枝：移除整個 channel
def channel_prune(conv_weights, keep_ratio=0.7):
    l2_norms = np.linalg.norm(conv_weights, axis=(0, 1, 2))
    keep_idx = np.argsort(l2_norms)[-int(len(l2_norms) * keep_ratio):]
    return conv_weights[:, :, :, keep_idx]
```

**結構化剪枝：** 移除整個 channel、filter 或 layer。可以利用現有硬體加速，但靈活性較低。

## 剪枝流程

```
訓練完整模型
    │
    ▼
評估權重重要性（L1/L2 norm、Hessian 等）
    │
    ▼
移除不重要的參數
    │
    ▼
微調（Fine-tune）恢復精度
    │
    ▼
重複直到達到目標壓縮率
```

## 知識蒸餾：大模型教小模型

知識蒸餾（Knowledge Distillation）由 Geoffrey Hinton 在 2015 年提出。核心概念是讓一個大型「教師模型」教導一個小型「學生模型」。

## 蒸餾的數學

學生模型的損失函數包含兩部分：

```
L = α * L_hard + (1-α) * L_soft

L_hard: 與真實標籤的交叉熵
L_soft: 與教師模型軟標籤的交叉熵
```

其中軟標籤使用「溫度參數」T 來控制分布的平滑度：

```python
def softmax_with_temperature(logits, temperature=3.0):
    exp_logits = np.exp(logits / temperature)
    return exp_logits / np.sum(exp_logits)
```

## 蒸餾架構

```
教師模型（大）                 學生模型（小）
    │                              │
    ▼                              ▼
軟標籤 logits ──────►   蒸餾損失 ◄──── 軟標籤 logits
                               │
真實標籤 ──────►   真實標籤損失 ◄──── 預測
```

## LLM 蒸餾的挑戰

LLM 的蒸餾與傳統 CNN 不同。2023-2024 年的研究發現，直接蒸餾 LLM 的 logits 效果有限，因為 LLM 的知識主要儲存在 attention pattern 中。新方法如：

- **MINILLM**：使用隱藏狀態對齊
- **DistilBERT**：保留 97% 性能，減少 40% 參數
- **知識蒸餾 + 量化聯合最佳化**

## 延伸閱讀

- [Hinton 2015: Distilling the Knowledge in a Neural Network](https://www.google.com/search?q=Hinton+distilling+knowledge+neural+network+2015)
- [Pruning Neural Networks: A Survey](https://www.google.com/search?q=pruning+neural+networks+survey+deep+learning)
- [Knowledge Distillation of LLMs](https://www.google.com/search?q=knowledge+distillation+large+language+models)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」焦點系列之三。*
