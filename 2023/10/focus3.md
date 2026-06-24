# VC 維度與學習能力

## 從有限到無限

前一期的 PAC 學習依賴於 |H|——假說空間的大小。但許多重要的假說空間（如實數線上的線性分類器）是無限的。

VC 維度（Vapnik-Chervonenkis Dimension）解決了這個問題：它度量假說空間的「複雜度」而非「大小」。

## 打散（Shattering）

一個假說空間 H **打散**（shatters）一個點集 S，如果 H 能實現 S 上所有可能的標記方式。

**範例**：實數線上的區間分類器 I_{a,b}(x) = 1{a ≤ x ≤ b}。對於兩個點，我們可以找到區間實現所有四種標記。但對於三個點，無法實現「中間為負、兩端為正」的模式。

```
兩個點：所有 4 種模式都可實現
三個點：中間為負無法實現
```

## VC 維度的定義

VC 維度 VC(H) 是 H 能打散的最大集合的大小：

```
VC(H) = max{ |S| : H shatters S }
```

如果 H 能打散任意大的集合，則 VC(H) = ∞。

### 常見 VC 維度

| 假說空間 | VC 維度 |
|---------|---------|
| 實數區間 | 2 |
| 軸對齊矩形 | 4 |
| d 維線性分類器 | d + 1 |
| 決策樹樁 | 1（實數特徵） |
| 神經網路（備註） | O(W log W) |

## VC 維度與 PAC 學習

VC 維度最重要的結果是它完全刻劃了 PAC 可學習性：

**定理**：一個假說空間 H 是 PAC 可學習的**若且唯若** VC(H) 是有限的。

### 泛化邊界

當 VC(H) = d 時，泛化邊界為：

```
R(h) ≤ R̂(h) + O(√(d/n * log(n/d) + (1/n) * log(1/δ)))
```

這個邊界告訴我們：

- 如果 d 很小（簡單模型），邊界很緊
- 如果 d 很大（複雜模型），需要更多樣本
- 如果 d ≈ n（樣本數等於 VC 維度），邊界無意義

## 證明思路

VC 維度泛化邊界的證明分為三步：

**第一步：對稱化**（Symmetrization）

引入幽靈樣本 S'，用 R̂'(h) 近似 R(h)：

```
P[|R(h) - R̂(h)| > ε] ≤ 2P[|R̂'(h) - R̂(h)| > ε]
```

**第二步：置換**（Permutation）

固定 2n 個樣本，考慮所有可能的標記交換。引入生長函數 G_H(n)：

```
P[sup|R̂'(h) - R̂(h)| > ε] ≤ 2G_H(2n) * exp(-nε²/2)
```

**第三步：VC 不等式**

生長函數的上界由 Sauer 引理給出：

```
G_H(n) ≤ Σ_{i=0}^d C(n, i) ≤ (en/d)^d
```

代入後得到完整的 VC 泛化邊界。

## 生長函數與 VC 維度

生長函數 G_H(n) 是 H 在 n 個點上能實現的最大標記方式數量：

- 當 n ≤ d 時：G_H(n) = 2^n（所有模式都可實現）
- 當 n > d 時：G_H(n) ≤ (en/d)^d

這一指數到多項式的轉變是 VC 理論的核心。

## 小結

VC 維度是學習理論中最重要的概念之一：

| 概念 | 意義 | 公式 |
|------|------|------|
| 打散 | H 能否實現所有標記 | 2^|S| 種模式 |
| VC 維度 | 能打散的最大點數 | VC(H) |
| 生長函數 | 實際可實現的模式數 | G_H(n) ≤ (en/d)^d |
| 泛化邊界 | R(h) ≤ R̂(h) + O(√d/n) | — |

---

**下一步**：[偏差-變異權衡](focus4.md)

## 延伸閱讀

- [VC Dimension Explained](https://www.google.com/search?q=VC+dimension+explained+simply)
- [Sauer's Lemma](https://www.google.com/search?q=Sauer+lemma+VC+dimension)
- [Vapnik-Chervonenkis Theory](https://www.google.com/search?q=Vapnik+Chervonenkis+theory+overview)
