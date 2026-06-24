# 正則化：Dropout、BatchNorm

## 過擬合問題

深度神經網路參數眾多，非常容易過擬合——在訓練資料上表現很好，但在測試資料上表現很差。正則化技術就是為了解決這個問題。

```
誤差
│  訓練誤差 ──── 持續下降
│  測試誤差 ──── 先下降後上升（過擬合開始）
│
│           ╱╲
│   ╱╲    ╱  ╲
│  ╱  ╲  ╱    ╲
│ ╱    ╲╱      ╲
╶╱─────────────────── 訓練輪數
      ↑
   最佳停止點
```

## Dropout

Dropout 由 Nitish Srivastava 和 Geoffrey Hinton 在 2014 年提出。

### 核心思想

每次訓練疊代中，以機率 p 隨機「丟棄」一部分神經元（將其輸出設為零）：

```python
def dropout_forward(x, p=0.5, training=True):
    if not training:
        return x  # 推論時不使用 Dropout
    mask = np.random.binomial(1, 1-p, size=x.shape) / (1-p)
    return x * mask
```

### 為什麼有效？

1. **減輕共適應**：神經元不能依賴其他神經元的存在，必須學習更魯棒的特徵
2. **模型集成**：Dropout 相當於訓練了 2^n 個子網路的集成
3. **正則化效果**：類似於 L2 正則化，但更強大

### 使用建議

```python
model = MLP([
    Layer(784, 256, 'relu', dropout=0.5),
    Layer(256, 128, 'relu', dropout=0.3),
    Layer(128, 10, 'softmax')
])
```

- 輸入層：p 通常設為 0.2 以下
- 隱藏層：p 在 0.3-0.5 之間
- 卷積層：p 設較小（0.1-0.2）
- 推論時：不使用 Dropout

## Batch Normalization

Batch Normalization（BN）由 Sergey Ioffe 和 Christian Szegedy 在 2015 年提出。

### 核心思想

對每個小批量的資料進行歸一化，然後學習縮放和平移參數：

```
μ_B = (1/m) · Σ x_i           # 批量均值
σ²_B = (1/m) · Σ (x_i - μ_B)² # 批量變異數

x̂_i = (x_i - μ_B) / √(σ²_B + ε)  # 歸一化
y_i = γ · x̂_i + β                 # 縮放和平移
```

### 為什麼有效？

1. **減少內部協變數偏移**：每層輸入的分布在訓練過程中保持穩定
2. **允許更大的學習率**：歸一化使梯度更穩定
3. **輕微正則化**：由於批量統計量的隨機性
4. **減少對初始化的依賴**

### 在模型中的位置

```
輸入 → Linear → BN → ReLU → Linear → BN → ReLU → 輸出
```

BN 通常放在線性變換之後、啟用函數之前。

### Inference 時的 BN

推論時使用全局統計量而非批量統計量：

```python
class BatchNorm:
    def __init__(self, dim):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.running_mean = np.zeros(dim)
        self.running_var = np.ones(dim)
        self.momentum = 0.9

    def forward(self, x, training=True):
        if training:
            mean = x.mean(axis=0)
            var = x.var(axis=0)
            self.running_mean = (self.momentum * self.running_mean
                                + (1 - self.momentum) * mean)
            self.running_var = (self.momentum * self.running_var
                               + (1 - self.momentum) * var)
        else:
            mean = self.running_mean
            var = self.running_var
        x_norm = (x - mean) / np.sqrt(var + 1e-5)
        return self.gamma * x_norm + self.beta
```

## Layer Normalization

Layer Normalization 是 BN 的變體，對每個樣本而非每個特徵進行歸一化：

```
μ_l = (1/H) · Σ a_i           # 層均值
σ²_l = (1/H) · Σ (a_i - μ_l)² # 層變異數
```

LN 在 Transformer 和 RNN 中廣泛應用，因為它不受批量大小的影響。

## 實戰對比

| 方法 | 優點 | 缺點 | 適用場景 |
|------|------|------|---------|
| Dropout | 簡單有效 | 訓練時間稍長 | 全連接層 |
| BatchNorm | 加速訓練 | 依賴批量大小 | CNN、MLP |
| LayerNorm | 批次無關 | 計算成本較高 | Transformer、RNN |

### 現代實踐

現代深度學習通常組合使用多種正則化：
- CNN：BatchNorm + 輕微 Dropout
- Transformer：LayerNorm + Dropout
- LLM：LayerNorm + 權重衰減

---

## 延伸閱讀

- [Dropout 論文 2014](https://www.google.com/search?q=Dropout+a+simple+way+to+prevent+neural+networks+from+overfitting)
- [Batch Normalization 論文 2015](https://www.google.com/search?q=Batch+Normalization+Accelerating+Deep+Network+Training)
- [Layer Normalization 論文 2016](https://www.google.com/search?q=Layer+Normalization)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」歷史回顧系列之一。*
