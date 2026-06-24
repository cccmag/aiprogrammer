# 圖注意力網路 GAT

## 圖神經網路的挑戰

圖神經網路（GNN）的目標是學習圖結構資料的表示。傳統的 GNN 方法（如 GCN、GraphSAGE）依賴於預先定義的聚合函數，通常是對鄰居節點的特徵進行平均或加權求和。

這種方法有兩個根本限制：
1. **靜態權重**：鄰居節點的權重是根據圖的結構預先確定的（如 GCN 的歸一化鄰接矩陣），而不是根據節點的內容動態調整的
2. **等權重假設**：所有鄰居節點被賦予相同或固定的重要性，無法區分「重要」和「不重要」的鄰居

## GAT 的解決方案

2018 年，Veličković 等人提出了圖注意力網路（Graph Attention Network，GAT），將注意力機制引入圖神經網路。

### 注意力在圖上的定義

GAT 的關鍵創新是：每個節點在聚合鄰居資訊時，使用注意力機制動態計算每個鄰居的重要性。

對於節點 i 及其鄰居 j，注意力分數計算如下：

```
e_{ij} = LeakyReLU(a^T [W h_i || W h_j])
```

其中：
- h_i、h_j：節點 i 和 j 的特徵向量
- W：可學習的權重矩陣（將節點特徵投影到更高層的表示空間）
- a：可學習的注意力向量
- ||：向量拼接操作

### 歸一化與聚合

注意力權重透過 softmax 歸一化：

```
α_{ij} = softmax_j(e_{ij}) = exp(e_{ij}) / Σ_{k∈N_i} exp(e_{ik})
```

節點的新特徵是所有鄰居特徵的加權和：

```
h_i' = σ(Σ_{j∈N_i} α_{ij} W h_j)
```

### GAT 的實現

```python
def gat_layer(h, adj, W, a):
    # h: 節點特徵 (n, d)
    # adj: 鄰接矩陣 (n, n)
    n = h.shape[0]
    Wh = h @ W  # (n, d')
    
    # 計算所有節點對的注意力分數
    Wh_i = Wh[:, None, :]  # (n, 1, d')
    Wh_j = Wh[None, :, :]  # (1, n, d')
    concat = np.concatenate([Wh_i.repeat(n, axis=1),
                             Wh_j.repeat(n, axis=0)], axis=-1)
    e = LeakyReLU(concat @ a)  # (n, n, 1)
    e = e.squeeze(-1)
    
    # 遮罩非鄰居節點
    e = np.where(adj > 0, e, -1e9)
    alpha = softmax(e, axis=-1)
    
    # 聚合
    h_out = alpha @ Wh
    return h_out, alpha
```

## Multi-Head 注意力在圖上的應用

與 Transformer 類似，GAT 也使用了多頭注意力來穩定學習過程：

```
h_i' = ||_{k=1}^K σ(Σ_{j∈N_i} α_{ij}^k W^k h_j)
```

在中間層，不同頭的輸出被拼接；在最後一層，不同頭的輸出被平均：

```
h_i' = σ(1/K Σ_k Σ_{j∈N_i} α_{ij}^k W^k h_j)
```

### 多頭注意力的視覺化

在 Cora 資料集（論文引用網路）上，GAT 的不同注意力頭學會了關注論文的不同特徵：

- 頭 1：關注研究主題相似性
- 頭 2：關注引用關係強度
- 頭 3：關注發表年份接近性

## GAT 的優勢

### 與 GCN 的比較

| 特性 | GCN | GAT |
|------|-----|-----|
| 聚合權重 | 固定（根據度數） | 動態（根據內容） |
| 歸一化 | 對稱歸一化 | Softmax 歸一化 |
| 歸納學習 | 困難 | 支援（可處理未見過的圖） |
| 可解釋性 | 低 | 高（注意力權重可視化） |

### 歸納與轉導學習

GCN 依賴於具體的圖結構，在訓練時需要看到整個圖（轉導學習）。而 GAT 的注意力計算是基於節點內容的，可以泛化到完全未見過的圖結構（歸納學習）。

## 應用案例

### 引用網路分析

在 Cora、Citeseer、Pubmed 等引用網路上，GAT 達到當時最先進的分類準確率。注意力權重的可視化顯示，GAT 學會了識別不同領域的論文之間的細微差異。

### 知識圖譜

GAT 被廣泛應用於知識圖譜的連結預測和關係推理。節點之間的注意力權重反映了關係類型的重要性，提供了可解釋的推理路徑。

### 藥物發現

在分子圖中，GAT 的注意力權重揭示了化學結構中的關鍵功能基團。原子之間的注意力強度與化學鍵的類型高度相關。

## GAT 的變體

### GATv2

Brody 等人（2022）發現原始 GAT 的表達力受到「靜態注意力」的限制——所有節點對的注意力排序在所有查詢下是相同的。GATv2 將注意力向量應用到拼接之後：

```
e_{ij} = a^T LeakyReLU(W [h_i || h_j])
```

GATv2 的注意力是「動態」的，可以表達更複雜的注意力模式。

### GaAN（門控注意力網路）

GaAN 引入了門控機制，讓每個注意力頭具有不同的權重：

```
h_i' = Σ_k g_{ik} × (Σ_{j∈N_i} α_{ij}^k W^k h_j)
```

其中 g_{ik} 是透過一個小型網路計算的門控值。

## 結論

GAT 將注意力機制的應用從序列資料擴展到了圖結構資料，展示了注意力作為一種通用關係學習機制的潛力。它的動態加權機制和可解釋性，使其成為圖神經網路中最受歡迎的模型之一。

---

**延伸閱讀**
- [GAT: Graph Attention Networks](https://www.google.com/search?q=Graph+Attention+Network+GAT+2018)
- [GATv2: How Attentive are Graph Attention Networks?](https://www.google.com/search?q=GATv2+improved+graph+attention)
- [GCN: Semi-Supervised Classification with Graph Convolutional Networks](https://www.google.com/search?q=Graph+Convolutional+Network+GCN)
