# 2. 聯合熵、條件熵與互資訊

## 聯合熵

當我們同時考慮兩個隨機變數 $X$ 與 $Y$ 時，聯合熵（Joint Entropy）衡量它們共同的不確定性：

$$H(X, Y) = -\sum_{x \in X} \sum_{y \in Y} p(x, y) \log_2 p(x, y)$$

聯合熵滿足 $H(X, Y) \leq H(X) + H(Y)$，等號成立若且唯若 $X$ 與 $Y$ 獨立。

## 條件熵

條件熵（Conditional Entropy）$H(Y|X)$ 表示在已知 $X$ 的條件下，$Y$ 的平均不確定性：

$$H(Y|X) = \sum_{x \in X} p(x) H(Y|X=x)$$

鍊式法則（Chain Rule）建立了聯合熵與條件熵的關係：

$$H(X, Y) = H(X) + H(Y|X) = H(Y) + H(X|Y)$$

## 互資訊

互資訊（Mutual Information）衡量 $X$ 與 $Y$ 之間共享的資訊量：

$$I(X; Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X, Y)$$

互資訊的關鍵性質：
- $I(X; Y) \geq 0$（非負性）
- $I(X; Y) = 0$ 若且唯若 $X$ 與 $Y$ 獨立
- $I(X; Y) = H(X) = H(Y)$ 若 $X$ 與 $Y$ 一一對應

## 視覺化理解

```
            H(X,Y)
  ┌──────────────────────┐
  │       ┌───┐          │
  │  H(X) │MI │   H(Y)   │
  │       └───┘          │
  └──────────────────────┘
```

MI 即互資訊（Mutual Information），也就是兩個圓圈重疊的部分。$H(X)$ 是 $X$ 的總資訊，$H(X|Y)$ 是 $X$ 中不被 $Y$ 知道的資訊，兩者相減就是共同擁有的資訊量。

## 應用：特徵選擇

在機器學習中，互資訊常被用來做特徵選擇：計算每個特徵與標籤之間的互資訊，挑選互資訊最高的特徵子集。與相關係數不同，互資訊可以捕捉非線性關係。

## 參考資源

- https://www.google.com/search?q=joint+entropy+conditional+entropy+mutual+information+definition+chain+rule
- https://www.google.com/search?q=mutual+information+feature+selection+machine+learning+tutorial
- https://www.google.com/search?q=information+theory+Venn+diagram+entropy+mutual+information+visualization
