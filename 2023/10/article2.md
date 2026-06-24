# PAC 可學習性證明

## 從定義到證明

在 focus2 中我們介紹了 PAC 學習的定義。本文將給出完整的 PAC 可學習性證明，從 Hoeffding 不等式開始，逐步推導樣本複雜度邊界。

## 工具：Hoeffding 不等式

Hoeffding 不等式是 PAC 證明的核心工具。設 Z₁, ..., Z_n 是獨立隨機變數，取值在 [0,1] 中，則：

```
P[|(1/n)ΣZ_i - E[Z]| ≥ ε] ≤ 2exp(-2nε²)
```

在學習問題中，對於固定的 h，令 Z_i = L(y_i, h(x_i))，經驗風險 R̂(h) = (1/n)Σ Z_i，真實風險 R(h) = E[Z]。

```
P[|R̂(h) - R(h)| ≥ ε] ≤ 2exp(-2nε²)
```

## 一致性案例（Realizable Case）

一致性假設：存在 h* ∈ H 使得 R(h*) = 0。

### 步驟 1：固定 h，偏差邊界

對於任意固定 h ∈ H：

```
P[|R̂(h) - R(h)| ≥ ε] ≤ 2exp(-2nε²)
```

### 步驟 2：Uniform 收斂

假若所有 h ∈ H 同時近似 R̂(h) 和 R(h)。使用 Union Bound：

```
P[sup_{h∈H} |R̂(h) - R(h)| ≥ ε] ≤ Σ_h P[|R̂(h) - R(h)| ≥ ε]
                                                    ≤ 2|H|exp(-2nε²)
```

### 步驟 3：誤差邊界

令 δ = 2|H|exp(-2nε²)，解出 n：

```
n ≥ (1/(2ε²)) * log(2|H|/δ)
```

當 n 滿足此條件時，以至少 1 - δ 的機率，對於所有 h ∈ H：

```
|R̂(h) - R(h)| ≤ ε
```

### 步驟 4：ERM 的表現

設 ĥ 是 ERM 解（R̂(ĥ) = 0 因為一致性假設），則：

```
R(ĥ) = R(ĥ) - R̂(ĥ) + R̂(ĥ) ≤ ε + 0 = ε
```

因此 R(ĥ) ≤ ε 以至少 1 - δ 的機率成立。

## Agnostic 案例

非一致性假設下，不存在完美的 h*。我們要證明：

```
R(ĥ) ≤ min_{h∈H} R(h) + ε
```

### 步驟 1：三角不等式

```
R(ĥ) - R(h*) = (R(ĥ) - R̂(ĥ)) + (R̂(ĥ) - R̂(h*)) + (R̂(h*) - R(h*))
```

因為 ĥ 最小化 R̂，所以 R̂(ĥ) - R̂(h*) ≤ 0，因此：

```
R(ĥ) - R(h*) ≤ (R(ĥ) - R̂(ĥ)) + (R̂(h*) - R(h*))
```

### 步驟 2：Uniform 收斂

與一致性案例同樣的手法：

```
P[sup|R̂(h) - R(h)| ≥ ε] ≤ 2|H|exp(-2nε²)
```

### 步驟 3：組合邊界

設事件 E 發生當 sup|R̂(h) - R(h)| ≤ ε。在 E 下：

```
R(ĥ) ≤ R̂(ĥ) + ε ≤ R̂(h*) + ε ≤ R(h*) + 2ε
```

令 ε' = 2ε：

```
R(ĥ) ≤ R(h*) + ε'
```

### 步驟 4：樣本複雜度

```
n ≥ (2/(ε'²)) * log(2|H|/δ)
```

注意 agnostic 案例需要的樣本數是一致性案例的 **1/ε 倍** 對比 **1/ε² 倍**——精度要求對 agnostic 學習的影響更大。

## 有限 H 到無限 H

當 H 為無限時，|H| 項被 VC 維度取代。此時的證明需要更多的技術工具：

1. **對稱化**：引入幽靈樣本
2. **生長函數**：取代 |H|
3. **Sauer 引理**：用 VC 維度上界生長函數
4. **VC 不等式**：最終的泛化邊界

詳細證明將在下一篇文章中展開。

## 證明的關鍵洞察

PAC 證明的每一步都可以總結為：

```
Hoeffding → Union Bound → Uniform Convergence → PAC Guarantee
```

| 步驟 | 工具 | 結果 |
|------|------|------|
| 單個 h | Hoeffding | |R̂ - R| ≤ ε |
| 所有 h | Union Bound | 同時收斂 |
| ERM | 最優化論證 | R(ĥ) ≈ min R(h) |
| 反解 | 代數運算 | 樣本複雜度 n(ε,δ) |

## 小結

PAC 可學習性證明展示了統計學習理論的典型推理方式：

- 使用集中不等式控制隨機偏差
- 使用 Union Bound 處理假說空間
- 從 Uniform 收斂推導 ERM 的誤差
- 反解樣本複雜度

## 延伸閱讀

- [Understanding PAC Learning Proof](https://www.google.com/search?q=PAC+learning+proof+step+by+step)
- [Hoeffding's Inequality Applications](https://www.google.com/search?q=Hoeffding+inequality+machine+learning+proof)
- [Agnostic PAC Learning](https://www.google.com/search?q=agnostic+PAC+learning+explained)
