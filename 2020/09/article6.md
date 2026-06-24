# CNN 的數學原理

## 前言

理解 CNN 的數學原理有助於更好地設計和最佳化模型。本文深入探討卷積神經網路的數學基礎。

---

## 一、卷積的數學定義

### 連續卷積

```
(f * g)(t) = ∫ f(τ) g(t - τ) dτ
```

### 離散卷積

```
(f * g)[n] = Σ f[m] g[n - m]
```

### 2D 卷積

```
(I * K)[i, j] = Σ Σ I[m, n] · K[i-m, j-n]
            = Σ Σ I[i-m, j-n] · K[m, n]
```

---

## 二、卷積層的計算

### 輸入輸出關係

假設：
- 輸入：$C_{in}$ 通道，高 $H$，寬 $W$
- 卷積核：$C_{out}$ 個，每個 $C_{in} × K_h × K_w$

輸出：
- $C_{out}$ 通道
- 高 $H' = (H - K_h + 2P) / S + 1$
- 寬 $W' = (W - K_w + 2P) / S + 1$

其中 $P$ 是 padding，$S$ 是 stride。

### 參數數量

```
卷積層參數 = C_out × (C_in × K_h × K_w + 1)
```

例如：輸入 3 通道，輸出 64 通道，3×3 卷積：
```
參數 = 64 × (3 × 3 × 3 + 1) = 64 × 28 = 1792
```

---

## 三、池化的數學

### 最大池化

```python
# 數學上：選擇區域內最大值
pool[i, j] = max(區域內所有值)
```

### 平均池化

```python
# 數學上：計算區域內平均值
pool[i, j] = (1/K²) × Σ 區域內所有值
```

### 池化與不變性

池化提供了對小的平移和旋轉的不變性。

---

## 四、激活函數的梯度

### ReLU

```
Forward: f(x) = max(0, x)
Backward: f'(x) = 1 if x > 0 else 0
```

### Sigmoid

```
Forward: σ(x) = 1 / (1 + e^(-x))
Backward: σ'(x) = σ(x) × (1 - σ(x))
```

### Softmax

```
σ(z)_i = e^{z_i} / Σ e^{z_j}
∂σ_i/∂z_j = σ_i × (δ_ij - σ_j)
```

---

## 五、反向傳播中的卷積

### 卷積層的梯度

假設損失對輸出的梯度為 ∂L/∂y，則：

```
∂L/∂K[i,j] = Σ Σ ∂L/∂y[m,n] × I[m-i, n-j]
```

### 捲積操作

卷積層的反向傳播也是一個捲積操作（可能需要翻轉卷積核）。

---

## 六、感受野

### 計算感受野

第 $k$ 層的理論感受野：
```
RF_k = RF_{k-1} + (f_k - 1) × ∏_{i=1}^{k-1} s_i
```

其中 $f_k$ 是第 $k$ 層的卷積核大小，$s_i$ 是第 $i$ 層的 stride。

### 例子

```
Layer1: Conv 3x3, stride 1 -> RF = 3
Layer2: Conv 3x3, stride 1 -> RF = 3 + (3-1) = 5
Layer3: Conv 3x3, stride 2 -> RF = 5 + (3-1) × 1 = 7
```

---

## 七、捲積運算的複雜度

### 時間複雜度

對於一個卷積層：
```
Time = O(H' × W' × C_out × C_in × K_h × K_w)
```

### 空間複雜度

```
Space = O(C_in × C_out × K_h × K_w)  # 權重
      + O(H' × W' × C_out)           # 輸出
```

### 深度可分離卷積

標准卷積：
```
Complexity = C_in × C_out × K_h × K_w × H' × W'
```

深度可分離卷積：
```
Complexity = C_in × K_h × K_w × H' × W' + C_out × H' × W'
          ≈ 1/(K_h × K_w) × 標准卷積
```

---

## 八、頻率視角

### 卷積定理

```
F(f * g) = F(f) × F(g)
```

卷積在空間域等價於在頻率域的乘法。

### 對應關係

| 空間域 | 頻率域 |
|--------|--------|
| 卷積 | 乘法 |
| 乘法 | 卷積 |

---

## 結語

深入理解 CNN 的數學原理有助於更好地理解模型行為、診斷問題，以及進行有效的優化。

---

*延伸閱讀：[CNN+mathematics+convolutional+neural+network+explained](https://www.google.com/search?q=CNN+mathematics+convolutional+neural+network+explained)*