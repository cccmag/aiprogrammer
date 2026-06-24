# 損失函數與梯度下降

## 機器學習的核心問題

機器學習的目標是找到一組參數 θ，使模型在訓練資料上的表現最好。這個「表現好壞」由損失函數衡量，「找到參數」的過程由優化演算法完成。

## 常見的損失函數

### 均方誤差（MSE）

```
MSE = (1/n) · Σ(y_i - ŷ_i)²
```

適用於回歸問題。MSE 對大誤差給予較大的懲罰（因為誤差被平方）。

```python
def mse_loss(y_pred, y_true):
    return np.mean((y_pred - y_true) ** 2)
```

### 交叉熵損失

```
CE = -Σ y_i · log(ŷ_i)
```

適用於分類問題。交叉熵來自資訊理論，衡量兩個機率分布之間的距離。

```python
def cross_entropy_loss(y_pred, y_true):
    return -np.sum(y_true * np.log(y_pred + 1e-8))
```

### 二元交叉熵（BCE）

```
BCE = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```

適用於二元分類。

### 比較

| 損失函數 | 適用任務 | 輸出層啟用 | 優點 |
|---------|---------|-----------|------|
| MSE | 回歸 | Linear | 直觀、可微 |
| CE | 多分類 | Softmax | 梯度更強 |
| BCE | 二分類 | Sigmoid | 機率解釋 |

## 梯度下降

### 基本思想

梯度下降（Gradient Descent）是最常用的優化演算法：

```
θ ← θ - η · ∇θ L(θ)
```

視覺化：想像你在山頂（高損失），梯度指向最陡的上坡方向。你想下山，所以往梯度的反方向走。

```python
def gradient_descent(theta, grad, lr=0.01):
    return theta - lr * grad
```

### 三種變體

**批量梯度下降（BGD）**：使用全部資料計算梯度
```
θ ← θ - η · (1/N) · Σ ∇L_i(θ)
```
優點：梯度準確
缺點：計算量大

**隨機梯度下降（SGD）**：每次只用一個樣本
```
θ ← θ - η · ∇L_i(θ)
```
優點：計算快、有隨機性可逃脫局部最小值
缺點：梯度不穩定

**小批量梯度下降（Mini-batch SGD）**：折衷方案
```
θ ← θ - η · (1/B) · Σ ∇L_i(θ)
```

## 進階優化器

### Momentum

模擬物理動量：

```
v_t = β·v_(t-1) + (1-β)·∇θ
θ ← θ - η · v_t
```

### Adam

Adaptive Moment Estimation 結合 Momentum 和 RMSProp：

```python
m_t = β1·m_(t-1) + (1-β1)·∇θ
v_t = β2·v_(t-1) + (1-β2)·(∇θ)²
m̂_t = m_t / (1-β1^t)
v̂_t = v_t / (1-β2^t)
θ ← θ - η · m̂_t / (√v̂_t + ε)
```

Adam 是深度學習中最常用的優化器。

## 學習率與收斂

學習率 η 是最重要的超參數之一：

- η 太大：震盪或不收斂
- η 太小：收斂過慢
- η 適中：穩定收斂

### 學習率排程

```python
# 階梯式衰減
lr = initial_lr * (0.5 ** (epoch // decay_step))

# 餘弦退火
lr = min_lr + 0.5 * (max_lr - min_lr) * (1 + cos(epoch/T * π))

# 循環學習率
lr = cyclic(lr_min, lr_max, step_size)
```

## 損失景觀

高維空間的損失函數通常不是凸函數，存在多個局部最小值和鞍點。

```
損失
│   ╱╲        ╱╲
│  ╱  ╲  ╱╲  ╱  ╲
│ ╱    ╲╱  ╲╱    ╲
│╱      ╲    ╱      ╲
└──────────────────── 參數
```

有趣的是，在高維空間中，鞍點遠比局部最小值常見。但 SGD 和 Adam 通常能有效應對這些挑戰。

---

## 延伸閱讀

- [SGD 介紹](https://www.google.com/search?q=stochastic+gradient+descent+tutorial)
- [Adam 論文 2014](https://www.google.com/search?q=Adam+optimizer+Kingma+Ba+2014)
- [Loss Landscape 視覺化](https://www.google.com/search?q=neural+network+loss+landscape+visualization)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」精選文章。*
