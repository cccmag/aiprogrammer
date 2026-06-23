# 因果發現演算法（2002-2028）

## 從數據中學習因果結構

因果發現的目標是直接從觀測數據推斷 DAG。這是因果推論中最具挑戰性的問題之一。

## 經典演算法

### PC 演算法（2002）

基於條件獨立檢定逐步移除邊，再確定方向。簡單但需要大量統計檢定，高維數據效果不佳。

### GES 演算法（2002）

貪婪等價搜索：從空圖開始，反覆添加/刪除邊，用 BIC 分數評估模型擬合度。

### LiNGAM（2006）

假設非高斯噪聲與線性關係，可以唯一識別因果方向。核心直覺：若 $X\to Y$，則 $X$ 與殘差 $Y-\beta X$ 獨立；反方向則不成立。

## NOTEARS（2018）

用連續優化取代離散搜索，將 DAG 約束轉化為平滑懲罰項。這是因果發現的重要突破，使深度學習可直接用於結構學習。

## 深度因果發現（2020-2028）

DAG-GNN、Causal Variational Autoencoder 等模型用神經網路學習非線性因果結構。到 2028 年，因果發現已應用於基因調控網路與金融風險建模。

## Python 範例：LiNGAM

```python
import numpy as np
from lingam import DirectLiNGAM

np.random.seed(0)
X = np.random.uniform(size=1000)
Y = 2 * X + np.random.uniform(size=1000)
Z = 0.5 * Y + np.random.normal(size=1000)
data = np.column_stack([X, Y, Z])

model = DirectLiNGAM()
model.fit(data)
print("因果順序:", model.causal_order_)
print("鄰接矩陣:\n", model.adjacency_matrix_)
```

參考：[搜尋 因果發現演算法](https://www.google.com/search?q=%E5%9B%A0%E6%9E%9C%E7%99%BC%E7%8F%BE%E6%BC%94%E7%AE%97%E6%B3%95) | [搜尋 NOTEARS causal](https://www.google.com/search?q=NOTEARS+causal+discovery)
