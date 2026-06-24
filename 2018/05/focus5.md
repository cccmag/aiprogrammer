# 訓練神經網路：學習率、批次大小、正則化

## 前言

訓練一個成功的類神經網路需要掌握多項技術：正確的學習率、合適的批次大小、以及防止過擬合的正則化方法。

## 學習率（Learning Rate）

學習率是最重要的超參數之一。

### 學習率過大

```
訓練 loss
    │
    │  ╱╲  ╱╲
    │ ╱  ╲╱  ╲  ← 振盪、不收斂
    │╱
    └────────────────────► 迭代
```

### 學習率過小

收斂太慢，訓練時間過長。

### 學習率衰減

```python
# 固定衰減
lr = initial_lr * (1 / (1 + decay * epoch))

# 指數衰減
lr = initial_lr * (decay ** epoch)

# 台階衰減
lr = initial_lr * (0.5 ** (epoch // 10))
```

## 批次大小（Batch Size）

| 批次大小 | 優點 | 缺點 |
|----------|------|------|
| SGD (batch=1) | 快速收斂到好結果 | 梯度估計嘈音大 |
| Mini-batch (32-256) | 穩定收斂、GPU 高效 | 需要調整 |
| Full batch | 精確梯度估計 | 記憶體限制、容易卡在局部最小 |

## 正則化

### 1. L2 正則化

在損失函數中添加權重衰減項：

```python
loss = original_loss + lambda * np.sum(weights**2)
```

### 2. Dropout

隨機丢棄一部分神經元：

```python
class Dropout:
    def __init__(self, rate):
        self.rate = rate

    def forward(self, x):
        self.mask = np.random.rand(*x.shape) > self.rate
        return x * self.mask

    def backward(self, dout):
        return dout * self.mask
```

### 3. Early Stopping

當驗證集表現開始下降時停止訓練。

## 梯度爆炸與消失

### 梯度爆炸

症狀：訓練 loss 變成 NaN。

解決方案：
- 梯度裁剪（Gradient Clipping）
- 更好的權重初始化（Xavier, He）
- 使用 ReLU 活化函數

### 梯度消失

症狀：前面的層幾乎不更新。

解決方案：
- 使用 ReLU 活化函數
- 殘差連接（ResNet）
- 批次標準化（Batch Normalization）

## 結語

訓練類神經網路是一個經驗性的過程，需要不斷嘗試和調整。理解這些基本技術將幫助你訓練出更好的模型。

---

**延伸閱讀**

- [深度學習最佳化](https://www.google.com/search?q=deep+learning+optimization+2018)
- [正則化技術](https://www.google.com/search?q=regularization+deep+learning)

---

*本篇文章為「AI 程式人雜誌 2018 年 5 月號」類神經網路導論系列之一。*