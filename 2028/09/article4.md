# 因果發現實戰：從觀察數據中挖掘因果結構

## 前言

因果圖是因果推論的骨架，但真實世界中的因果結構往往未知。因果發現（Causal Discovery）就是要從觀察數據中自動推導變數之間的因果關係。2026 年的因果發現工具已經成熟到可以處理數千變數的規模。

## 三類主流方法

### 1. 基於約束的方法（PC 演算法）

PC 演算法從完全連接圖開始，逐步移除條件獨立性成立的邊，最後對剩餘邊進行定向。

```python
import numpy as np
from itertools import combinations
from scipy.stats import pearsonr


def partial_corr(X: np.ndarray, i: int, j: int, condition: list[int]) -> float:
    """Compute partial correlation p(i,j | condition)."""
    n = X.shape[0]
    if not condition:
        return pearsonr(X[:, i], X[:, j])[0]
    # Linear regression residual approach
    Z = X[:, condition]
    Z = np.column_stack([np.ones(n), Z])
    beta_i = np.linalg.lstsq(Z, X[:, i], rcond=None)[0]
    beta_j = np.linalg.lstsq(Z, X[:, j], rcond=None)[0]
    resid_i = X[:, i] - Z @ beta_i
    resid_j = X[:, j] - Z @ beta_j
    return pearsonr(resid_i, resid_j)[0]


def pc_algorithm(data: np.ndarray, names: list[str],
                 alpha: float = 0.05) -> list[tuple[int, int]]:
    n_vars = data.shape[1]
    adj = [[True] * n_vars for _ in range(n_vars)]
    np.fill_diagonal(adj, False)

    for i, j in combinations(range(n_vars), 2):
        r, p = pearsonr(data[:, i], data[:, j])
        if p > alpha:
            adj[i][j] = adj[j][i] = False

    for k in range(n_vars):
        for i, j in combinations(range(n_vars), 2):
            if not adj[i][j]:
                continue
            r = partial_corr(data, i, j, [k])
            test_stat = np.abs(r) * np.sqrt((data.shape[0] - 3) / (1 - r**2))
            if test_stat < 1.96:
                adj[i][j] = adj[j][i] = False

    edges = []
    for i, j in combinations(range(n_vars), 2):
        if adj[i][j]:
            edges.append((names[i], names[j]))
    return edges


# Demo: X -> Y, X -> Z, Y -> Z (chain)
np.random.seed(42)
X = np.random.randn(200)
Y = 0.8 * X + 0.6 * np.random.randn(200)
Z = 0.5 * Y + 0.5 * np.random.randn(200)
data = np.column_stack([X, Y, Z])

edges = pc_algorithm(data, ["X", "Y", "Z"], alpha=0.05)
print("PC Algorithm discovered edges:")
for u, v in edges:
    print(f"  {u} -- {v}")
```

### 2. 基於分數的方法（GES）

Greedy Equivalence Search（GES）從空圖開始，逐步加入使 BIC 分數改善最多的邊，再進行刪除階段最佳化。

### 3. 基於函數因果模型的方法（LiNGAM）

LiNGAM 假設資料來自線性非高斯系統，利用獨立成分分析（ICA）恢復因果順序：

```python
from sklearn.decomposition import FastICA


def lingam_discovery(data: np.ndarray, names: list[str]) -> list[tuple[str, str]]:
    ica = FastICA(n_components=data.shape[1], random_state=42)
    S = ica.fit_transform(data)  # Independent components
    W = ica.mixing_  # Mixing matrix
    B = np.linalg.inv(W) - np.eye(data.shape[1])
    B_perm = np.argsort([np.argmax(np.abs(B[i])) for i in range(len(B))])
    edges = []
    for i in B_perm:
        for j in range(i):
            if abs(B[B_perm[j], i]) > 0.1:
                edges.append((names[B_perm[j]], names[i]))
    return edges


edges_lingam = lingam_discovery(data, ["X", "Y", "Z"])
print("\nLiNGAM discovered edges:")
for u, v in edges_lingam:
    print(f"  {u} -> {v}")
```

## 實戰評估：模擬 vs 真實資料

在模擬資料上，PC 演算法的精確率通常高於召回率——它傾向於輸出較少但可信度高的邊。LiNGAM 在非高斯資料上表現出色但對高斯資料失效。GES 則在中等樣本量（n > 500）時表現最穩定。

## 2026 年的因果發現工具

- **CausalNex**：基於 DoWhy 的圖形化因果發現工具。
- **TETRAD**：卡內基梅隆大學開發的經典套件，2026 年已全面支援 Python。
- **causal-learn**：華人學者主導的開源專案，實作了 20+ 種因果發現演算法。

## 結語

因果發現是因果 AI 最有挑戰性也最有潛力的環節。沒有一種演算法在所有情境下通用——選擇哪種方法取決於資料的生成機制、樣本量、以及領域知識的可用性。未來趨勢是將先驗知識與數據驅動的發現結合，走向「人機協作」的因果建模。

---

**延伸閱讀**
- [PC 演算法詳解](https://www.google.com/search?q=PC+algorithm+causal+discovery+Spirtes+Glymour)
- [LiNGAM 論文](https://www.google.com/search?q=LiNGAM+non+gaussian+causal+discovery)
- [causal-learn Python 套件](https://www.google.com/search?q=causal+learn+Python+causal+discovery+library)
