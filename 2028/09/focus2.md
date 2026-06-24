# 因果圖與結構因果模型（1980-2028）

## Pearl 的因果三部曲

Judea Pearl 在 1980 年代開始研究貝氏網路，2000 年出版《Causality》奠定結構因果模型（SCM）。SCM 包含三個層級：關聯（Association）、干預（Intervention）、反事實（Counterfactuals）。

## 有向無環圖（DAG）

因果圖用 DAG 表示變數間的因果關係。節點是變數，箭頭代表因果方向。關鍵概念：

- **d-separation**：判斷兩個變數是否在給定條件下獨立
- **後門準則**（Back-door Criterion）：找出需要控制的混淆變數
- **前門準則**（Front-door Criterion）：透過中介變數識別因果效應

## do-calculus

Pearl 的 do-calculus 提供了三條規則，可以將包含 `do(x)` 的干預表達式轉化為僅含觀測分佈的表達式。這是因果識別的核心工具。

## 因果圖的現代應用

2020 年代，DoWhy（微軟）、CausalNex 等套件讓 SCM 落地。到 2028 年，因果圖已整合進主流 ML 框架，工程師可以在訓練前自動繪製因果假設圖。

## Python 範例：建立簡單因果圖

```python
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([
    ("抽菸", "肺癌"),
    ("基因", "抽菸"),
    ("基因", "肺癌"),
])
print("因果圖節點:", G.nodes)
print("因果圖邊:", G.edges)
```

參考：[搜尋 結構因果模型](https://www.google.com/search?q=%E7%B5%90%E6%A7%8B%E5%9B%A0%E6%9E%9C%E6%A8%A1%E5%9E%8B) | [搜尋 Judea Pearl Causality](https://www.google.com/search?q=Judea+Pearl+Causality)
