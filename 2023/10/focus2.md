# PAC 學習理論

## Probably Approximately Correct

PAC（Probably Approximately Correct）學習框架由 Leslie Valiant 在 1984 年提出，是學習理論最重要的數學框架之一。

核心問題：**給定 n 個樣本，我們能否保證學到的模型以高機率接近最優模型？**

## PAC 可學習的定義

一個概念類 C 是 PAC 可學習的，如果存在一個學習演算法 A 和函數 m_H(ε, δ)，使得對於任意 ε > 0、δ > 0、以及 C 上的任意目標概念 c：

當樣本數 n ≥ m_H(ε, δ) 時，以至少 1 - δ 的機率有：

```
R(ĥ) ≤ ε
```

其中 ĥ 是演算法 A 輸出的假說。

這裡：
- **ε**（epsilon）是準確度參數——我們允許的誤差
- **δ**（delta）是信心參數——我們允許失敗的機率
- **m_H(ε, δ)** 是樣本複雜度——達到給定精度所需的最小樣本數

## 一致性 PAC 學習

在一致性（Realizable）案例中，存在一個假說 h* ∈ H 使得 R(h*) = 0。此時 ERM 的樣本複雜度為：

```
m_H(ε, δ) ≥ (1/ε) * log(|H|/δ)
```

其中 |H| 是假說空間的大小。

### 推導

從 Hoeffding 不等式出發。對於固定的 h，經驗風險和真實風險的差異：

```
P[|R̂(h) - R(h)| ≥ ε] ≤ 2exp(-2nε²)
```

對所有 h ∈ H 取 union bound：

```
P[∃h ∈ H: |R̂(h) - R(h)| ≥ ε] ≤ 2|H|exp(-2nε²)
```

令右側等於 δ，解出 n：

```
n ≥ (1/(2ε²)) * log(2|H|/δ)
```

這給出了一個泛化邊界：在足夠多的樣本下，ERM 的真實風險接近經驗風險。

## Agnostic PAC 學習

在非一致性（Agnostic）案例中，我們不假設存在完美的假說。此時目標是逼近 H 中的最優假說：

```
R(ĥ) ≤ inf_{h∈H} R(h) + ε
```

樣本複雜度變為：

```
n ≥ (2/ε²) * log(2|H|/δ)
```

與一致性案例相比，agnostic 學習需要更多的樣本（分子從 1 變為 2），因為我們需要同時估計每個假說的風險。

## 樣本複雜度的直觀理解

```
樣本複雜度 n ≈ (複雜度度量) / ε²
```

- 假說空間越複雜（|H| 越大），需要的樣本越多
- 精度要求越高（ε 越小），需要的樣本越多
- 對數項意味著 |H| 對樣本複雜度的影響比 ε 小得多

### 範例

考慮布林函數的學習。若輸入維度為 d，則 |H| = 2^(2^d)。代入公式：

```
n ≈ (1/ε) * 2^d
```

樣本數隨維度指數增長——這就是**維度災難**（Curse of Dimensionality）。

## PAC 學習的意義

PAC 框架最重要的貢獻是將學習問題轉化為統計問題：

1. **樣本複雜度**是有限的，且可以量化
2. **收斂速率**可以通過假說空間的複雜度來控制
3. **ERM 策略**在可學習問題上是有效的

但 PAC 框架也有侷限性：它要求資料是 IID 的，且對敵對資料不設防。

## 小結

| 概念 | 含義 | 邊界 |
|------|------|------|
| 一致性 PAC | 存在完美假說 | n ≥ (1/ε)log(|H|/δ) |
| Agnostic PAC | 不存在完美假說 | n ≥ (2/ε²)log(2|H|/δ) |
| 樣本複雜度 | 達到精度 ε 所需 n | 依 H 的複雜度增長 |

---

**下一步**：[VC 維度與學習能力](focus3.md)

## 延伸閱讀

- [Valiant's PAC Learning Paper](https://www.google.com/search?q=Valiant+PAC+learning+1984)
- [PAC Learning Explained](https://www.google.com/search?q=PAC+learning+explained+introduction)
- [Hoeffding's Inequality](https://www.google.com/search?q=Hoeffding+inequality+machine+learning)
