# 焦點文章 3：梯度消失與梯度爆炸問題

## 前言

訓練 RNN 的最大挑戰是梯度消失與梯度爆炸問題。本章節詳細分析這個問題的成因與解決方案。

## 梯度計算：時間展開視角

將 RNN 在時間步展開後，可以看出梯度如何傳播：

```
_loss_∂ / ∂W = Σ_t (∂_loss_t / ∂W)
```

每個時間步都對權重 W 有貢獻，梯度是所有時間步梯度的總和。

## 問題成因

### 鏈式法則與梯度衰減

在時間步 t 的梯度需要反向傳播經過所有中間時間步：

```
∂h_t / ∂h_k = ∏_{i=k+1}^{t} (∂h_i / ∂h_{i-1})
```

對於 tanh 激活函數：

```
|∂h_i / ∂h_{i-1}| = |diag(1 - tanh²(a_i))| × |Wᵀ|
                  ≤ ||Wᵀ||
```

當 ||Wᵀ|| < 1 時，梯度在傳播過程中指数衰減。

## 梯度爆炸的徵兆

- 訓練 loss 為 NaN
- 權重值變得極大
- 梯度更新不穩定

```python
# 檢測梯度爆炸
if np.isnan(gradients).any() or np.abs(gradients).max() > 100:
    print("Gradient explosion detected!")
```

## 梯度消失的徵兆

- 長期依賴無法學習
- 網路只記住最近的輸入
- 訓練 loss 幾乎不下降

```python
# 檢測梯度消失
if np.abs(gradients).min() < 1e-10:
    print("Gradient vanishing detected!")
```

## 解決方案

### 1. 梯度裁剪（Gradient Clipping）

```python
def clip_gradients(gradients, max_norm=5.0):
    total_norm = np.sqrt(sum(np.sum(g**2) for g in gradients))
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1:
        return [g * clip_coef for g in gradients]
    return gradients
```

在反向傳播後、參數更新前套用：

```python
gradients = backpropagate(loss)
gradients = clip_gradients(gradients)
optimizer.step()
```

### 2. 權重初始化

使用適當的初始化方法：

```python
# Xavier 初始化
W = np.random.randn(hidden_size, hidden_size) * np.sqrt(2.0 / (hidden_size + hidden_size))
```

### 3. ReLU 替代 tanh

```python
def relu(x):
    return np.maximum(0, x)

def relu_gradient(x):
    return (x > 0).astype(float)
```

### 4. LSTM 與 GRU

使用具有「門控」機制的特殊 RNN 結構（見下章）。

## LSTM：專門的解決方案

LSTM 透過記憶細胞與門控機制，有效解決梯度消失問題：

```python
class LSTMCell:
    def __init__(self, input_size, hidden_size):
        # 輸入門
        self.W_i = np.random.randn(hidden_size, input_size + hidden_size)
        # 遺忘門
        self.W_f = np.random.randn(hidden_size, input_size + hidden_size)
        # 輸出門
        self.W_o = np.random.randn(hidden_size, input_size + hidden_size)
        # 候選值
        self.W_c = np.random.randn(hidden_size, input_size + hidden_size)
```

LSTM 的關鍵是梯度可以在記憶通道中直接流動，不會衰減。

## 總結

梯度消失與梯度爆炸是 RNN 訓練的核心挑戰。梯度裁剪是緩解問題的簡單有效方法，而 LSTM/GRU 從結構上解決了這個問題。

## 延伸閱讀

- https://www.google.com/search?q=vanishing+gradient+problem+RNN
- https://www.google.com/search?q=gradient+clipping+RNN+explained