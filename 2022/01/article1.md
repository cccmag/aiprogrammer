# 神經元數學模型

## 從生物到數學

生物神經元通過樹突接收訊號，在細胞體中進行處理，然後通過軸突傳遞輸出訊號。

```
生物神經元：
樹突 ──→ 細胞體 ──→ 軸突 ──→ 突觸 ──→ 下一個神經元
```

人工神經元是對這個過程的數學抽象：

```
人工神經元：
x1 ── w1 ──┐
x2 ── w2 ──┼──→ Σ(wi·xi + b) ──→ σ(·) ──→ 輸出
...         │
xn ── wn ──┘
```

## McCulloch-Pitts 模型

1943 年，Warren McCulloch 和 Walter Pitts 提出了最早的神經元數學模型：

```
y = f(Σ wi·xi - θ)
```

其中 f 是階梯函數，θ 是閾值。

這個模型可以表示 AND、OR、NOT 等邏輯運算，但權重是手動設定的，無法學習。

## Rosenblatt 感知器

1958 年，Frank Rosenblatt 引入了可學習的權重：

```
y = sign(w·x + b)
```

學習規則：w ← w + η·(y - ŷ)·x

感知器可以自動從資料中學習權重，這是最早的監督式學習演算法之一。

## 現代的數學模型

現代深度學習中的神經元可以表示為：

```
y = σ(W·x + b)
```

其中：
- x ∈ ℝⁿ：輸入向量
- W ∈ ℝ^(m×n)：權重矩陣
- b ∈ ℝ^m：偏置向量
- σ：非線性啟用函數

### 向量化表示

在實踐中，我們使用向量和矩陣運算來同時處理多個樣本和多個神經元：

```
Y = σ(X·W^T + b)
```

其中 X ∈ ℝ^(B×n), W ∈ ℝ^(m×n), b ∈ ℝ^m。

### 為什麼需要偏置？

偏置 b 使決策邊界可以不經過原點，增加了模型的靈活性：

```
沒有偏置：y = sign(w·x) → 決策邊界必過原點
有偏置：  y = sign(w·x + b) → 任意直線
```

## 從單神經元到多層網路

單個神經元是對生物神經元的高度簡化。實際生物神經網路有以下特點：

1. **高度連接**：一個神經元可能連接到上萬個其他神經元
2. **非線性互動**：生物神經元之間的互動遠比簡單加權和複雜
3. **動態調整**：突觸權重會隨時間動態變化

人工神經網路的發展趨勢是：在保持計算可行的前提下，逐步增加模型的生物合理性。

## 神經元的可解釋性

學習完成後的神經元可以解讀為「特徵檢測器」：

- 在圖像網路的底層：檢測邊緣、紋理
- 在中層：檢測形狀、物體部件
- 在高層：檢測完整物體概念

## 計算圖視角

從現代深度學習框架的角度，神經元是計算圖中的一個節點：

```python
# 使用 PyTorch 定義一個神經元
import torch.nn as nn

neuron = nn.Linear(10, 1)  # 10 個輸入，1 個輸出
output = torch.sigmoid(neuron(input))
```

計算圖自動追蹤運算路徑，支援自動微分——這是 PyTorch、TensorFlow 等框架的核心能力。

---

## 延伸閱讀

- [McCulloch-Pitts 1943](https://www.google.com/search?q=McCulloch+Pitts+1943+neuron+model)
- [Rosenblatt Perceptron 1958](https://www.google.com/search?q=Rosenblatt+perceptron+1958)
- [Neural Network 數學基礎](https://www.google.com/search?q=neural+network+mathematical+foundation)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
