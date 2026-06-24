# 資訊理論在機器學習的應用

## 從通訊到學習

資訊理論與機器學習看似屬於不同領域，但兩者的核心問題具有深刻的相似性：通訊是在雜訊中恢復信號，學習是從數據中發現規律。Shannon 的熵與互資訊在機器學習中扮演著關鍵角色。

## 熵：決策樹的指標

決策樹演算法（如 ID3、C4.5）使用資訊增益（Information Gain）來選擇分割特徵。資訊增益就是父節點的熵與子節點加權熵的差值：

$$Gain(S, A) = H(S) - \sum_{v \in A} \frac{|S_v|}{|S|} H(S_v)$$

選擇資訊增益最大的特徵作為當前節點的分割依據，本質上就是在最大化分割前後的不確定性減少。

```python
def info_gain(parent_entropy, children, child_entropies, sizes):
    total = sum(sizes)
    weighted = sum(s/total * e for s, e in zip(sizes, child_entropies))
    return parent_entropy - weighted
```

## 互資訊：特徵選擇與相依性

互資訊可以捕捉非線性相關，遠比相關係數強大。在特徵選擇中，我們選擇 $I(X_i; Y)$ 最大的特徵子集。此外，互資訊也被用於：
- 獨立性測試
- 聚類評估（Normalized Mutual Information）
- 因果推斷

## 資訊瓶頸

資訊瓶頸（Information Bottleneck, IB）由 Tishby 在 1999 年提出，它將學習視為一個壓縮問題：找到一個表示 $T$，在保留關於 $Y$ 的資訊的同時壓縮 $X$。

$$\min I(T; X) - \beta I(T; Y)$$

其中 $\beta$ 控制壓縮與預測的權衡。IB 方法已被應用於：
- 深度學習表示分析
- 聚類演算法
- 語音與圖像處理

## KL 散度與損失函數

KL 散度衡量兩個機率分布之間的差異：

$$D_{KL}(P||Q) = \sum_{x} P(x) \log \frac{P(x)}{Q(x)}$$

在機器學習中，KL 散度無所不在：
- **交叉熵損失**：分類問題的標準損失函數
- **VAE 損失**：ELBO 中的 KL 項
- **變分推斷**：最小化近似後驗與真實後驗的 KL 散度

```python
def kl_divergence(P, Q):
    return sum(p * math.log2(p/q) for p, q in zip(P, Q) if p > 0)
```

## 總結

資訊理論為機器學習提供了三個關鍵貢獻：
1. **量化不確定性**：熵與交叉熵作為損失函數的核心
2. **量化依賴性**：互資訊用於特徵選擇與表示學習
3. **理論下界**：通道編碼定理與率失真理論為學習問題提供效能上限

## 參考資源

- https://www.google.com/search?q=information+gain+decision+tree+ID3+C4.5+entropy+splitting+criterion
- https://www.google.com/search?q=mutual+information+feature+selection+nonlinear+dependence+measure+machine+learning
- https://www.google.com/search?q=information+bottleneck+method+Tishby+deep+learning+representation+compression
- https://www.google.com/search?q=KL+divergence+cross+entropy+loss+VAE+variational+inference+machine+learning
