# 經驗風險最小化 ERM

## ERM：最直觀的學習原則

經驗風險最小化（Empirical Risk Minimization，ERM）是最基本的學習原則：**選擇在訓練資料上表現最好的模型**。

儘管 ERM 看起來簡單直接，但它包含了學習理論中最深刻的一組問題。

## ERM 的形式化

給定訓練樣本 S = {(x_i, y_i)}^n_{i=1} 和損失函數 L：

```
ĥ_ERM = argmin_{h∈H} (1/n) Σ^n_{i=1} L(y_i, h(x_i))
```

### 常見 ERM 實例

| 問題 | 損失函數 | H | 演算法 |
|------|---------|----|-------|
| 最小平方法 | (y - h(x))² | 線性函數 | 線性回歸 |
| 邏輯回歸 | log(1 + exp(-y·h(x))) | 線性函數 | 梯度下降 |
| SVM（原始） | max(0, 1 - y·h(x)) | 線性函數 | QP 求解 |
| 決策樹 | 0-1 損失近似 | 決策樹 | CART |

## ERM 的一致性

ERM 是一致的，當 H 是有限集且 ERM 能找到全局最優解。

更一般地，對於一致的 ERM：

```
R(ĥ_n) → inf_{h∈H} R(h)  as n → ∞
```

這意味著給足夠多的資料，ERM 最終會找到 H 中的最優假說。

### 一致性的條件

ERM 一致的充要條件是 H 上的 Uniform 收斂：

```
lim_{n→∞} P[sup_{h∈H} |R̂(h) - R(h)| > ε] = 0  for all ε > 0
```

這正是 VC 維度有限的條件。

## ERM 的失敗模式

### 過擬合（Overfitting）

當 H 複雜但樣本不足時，ERM 會記住訓練資料而非學習模式。

```
如果 VC(H) >> n，ERM 的泛化邊界無意義。
```

**經典範例**：用 n 次多項式擬合 n 個點——完美擬合但沒有預測能力。

### 欠擬合（Underfitting）

當 H 太簡單時，即使有無限資料也無法逼近真實函數。

```
如果 H 不包含真實函數，ERM 的偏差主導誤差。
```

**經典範例**：用線性模型擬合二次函數。

## 正則化 ERM

為了解決過擬合，引入正則化 ERM（RERM）：

```
ĥ_RERM = argmin_{h∈H} [ (1/n) Σ L(y_i, h(x_i)) + λΩ(h) ]
```

RERM 可以從多個角度理解：

| 視角 | RERM 的意義 | 公式 |
|------|------------|------|
| 學習理論 | 控制假說空間有效大小 | 降低 VC 維度 |
| 最佳化 | 加入懲罰項 | 條件數改善 |
| 貝氏 | 先驗分布的 MAP | log P(θ|D) |

## ERM 的實作考慮

### 1. 全域最佳化 vs 局部最優

ERM 要求找到 H 中的全局最優解，但對於非凸問題（神經網路）這通常是 NP 難的。實際上：

```
SGD 找到的局部極小值在實踐中表現良好。
```

理論解釋：高維損失函數的局部極小值接近全局極小值。

### 2. 隱式正則化

實際應用中的 ERM 往往伴隨著隱式正則化：

- SGD 的隨機性
- 小批次訓練
- 早停法
- 學習率調度

這些都影響 ERM 的有效解空間。

## ERM 的泛化邊界

對有限 H，ERM 的泛化邊界：

```
R(ĥ) ≤ min_{h∈H} R(h) + O(√(log|H|/n))
```

對無限 H（以 VC 維度 d 度量）：

```
R(ĥ) ≤ min_{h∈H} R(h) + O(√(d/n))
```

## 小結

ERM 是學習理論的出發點，理解它的優缺點是深入學習理論的關鍵：

| 優點 | 缺點 |
|------|------|
| 直觀且易實作 | 容易過擬合 |
| 有完整的理論分析 | 非凸問題難求解 |
| 一致性條件明確 | 需要選擇 H |

## 延伸閱讀

- [Empirical Risk Minimization](https://www.google.com/search?q=empirical+risk+minimization+explained)
- [ERM and Overfitting](https://www.google.com/search?q=ERM+overfitting+regularization)
- [Regularized ERM](https://www.google.com/search?q=regularized+empirical+risk+minimization)
