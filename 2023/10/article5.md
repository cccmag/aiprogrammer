# Rademacher 複雜度

## 超越 VC 維度

VC 維度是衡量假說空間複雜度的經典工具，但它有一個重要缺點：**VC 維度不依賴於資料分布**。

Rademacher 複雜度是 VC 維度的現代替代方案，它對資料分布敏感，能給出更緊的泛化邊界。

## 直觀理解

Rademacher 複雜度度量的是**假說空間與隨機雜訊的相關程度**。

給定隨機的 ±1 標記（Rademacher 隨機變數），如果存在一個假說 h ∈ H 能很好地擬合這些隨機標記，則說明 H 很複雜——它能「記住」雜訊。

## 定義

經驗 Rademacher 複雜度：

```
R̂_n(H) = E_σ [ sup_{h∈H} (1/n) Σ σ_i h(x_i) ]
```

其中 σ_i 是取值在 {+1, -1} 的 Rademacher 隨機變數（各以 1/2 機率取 +1 或 -1）。

**Rademacher 複雜度**是對資料分布的期望：

```
R_n(H) = E_{S~P^n} [ R̂_n(H) ]
```

### 解讀

- R_n(H) ≈ 0：H 無法擬合隨機雜訊——簡單的假說空間
- R_n(H) 較大：H 能擬合隨機雜訊——複雜的假說空間
- 最大值為 1（當 H 包含所有可能函數時）

## Rademacher 泛化邊界

Rademacher 複雜度的核心結果是以下的泛化邊界：

**定理**：對任意 δ > 0，以至少 1 - δ 的機率，對所有 h ∈ H：

```
R(h) ≤ R̂(h) + R_n(H) + √(log(1/δ)/(2n))
```

這個邊界比 VC 維度邊界更緊的原因：

1. R_n(H) 依賴於資料分布 P，而非最壞情況
2. 沒有 log(n/d) 因子
3. 可以處理實值函數，不限於二分類

### 可實現的邊界（Rademacher vs VC）

| 邊界類型 | 形式 | 緊度 |
|---------|------|------|
| VC 維度 | O(√(d/n · log(n/d))) | 鬆 |
| Rademacher | R_n(H) + O(√(1/n)) | 更緊 |

## 常見假說空間的 Rademacher 複雜度

### 線性函數類

對於 H = {x → w·x | ||w||₂ ≤ B, ||x||₂ ≤ R}：

```
R_n(H) ≤ B·R / √n
```

這表明：
- 權重範數越小，複雜度越低
- 資料範數越小，複雜度越低
- 收斂速率為 O(1/√n)

### 核方法

對 RKHS H 中的單位範數球：

```
R_n(H) ≤ √(tr(K)/n) / n = √(Σ λ_i / n) / n
```

其中 λ_i 是核矩陣 K 的特徵值。這解釋了為什麼核方法在特徵值快速衰減時表現良好。

## Rademacher 複雜度的優點

| 優點 | 說明 |
|------|------|
| 資料依賴性 | 對不同分布給出不同邊界 |
| 更緊的邊界 | 沒有 log 因子 |
| 適用範圍廣 | 分類、回歸、結構化預測 |
| 可計算 | 可以透過蒙地卡羅估計 |

## Rademacher 複雜度的計算

實際中可以透過蒙地卡羅方法估計 Rademacher 複雜度：

```python
def estimate_rademacher(X, model_class, n_trials=1000):
    n = len(X)
    rademacher = 0
    for _ in range(n_trials):
        sigma = np.random.choice([-1, 1], n)
        sup = max(np.abs(model_class.fit_predict(X, sigma)))
        rademacher += sup
    return rademacher / n_trials / n
```

## 與其他複雜度度量的關係

```
VC(H) → 生長函數 G_H(n)
                ↓
         Sauer 引理
                ↓
       Rademacher ≤ O(√(VC(H)/n))
```

VC 維度給出的是 Rademacher 複雜度的上界，但反過來不成立——Rademacher 複雜度可以遠小於 VC 維度邊界。

## 小結

Rademacher 複雜度是現代學習理論中最重要的複雜度度量：

| 概念 | VC 維度 | Rademacher |
|------|---------|-----------|
| 依賴分布 | 否 | 是 |
| 邊界緊度 | 鬆 | 較緊 |
| 適用範圍 | 二分類 | 分類、回歸 |
| 計算難度 | 理論計算 | 可蒙地卡羅估計 |

## 延伸閱讀

- [Rademacher Complexity Explained](https://www.google.com/search?q=Rademacher+complexity+machine+learning)
- [Rademacher vs VC Dimension](https://www.google.com/search?q=Rademacher+complexity+vs+VC+dimension)
- [Rademacher Complexity Bounds](https://www.google.com/search?q=Rademacher+generalization+bounds)
