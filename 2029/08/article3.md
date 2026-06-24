# 量子支援向量機

## 前言

量子核方法將古典 SVM 映射到量子態空間，利用量子計算的指數級特徵空間來提升分類能力。

## 量子核方法

古典 SVM 使用核函數 $K(x_i, x_j) = \langle\phi(x_i)|\phi(x_j)\rangle$ 計算資料點之間的相似度。量子 SVM 將資料編碼到量子態 $|\phi(x)\rangle$，定義量子核為：

$$K_Q(x_i, x_j) = |\langle\phi(x_i)|\phi(x_j)\rangle|^2$$

## Python 實作

```python
import numpy as np
from sklearn.svm import SVC

def quantum_kernel(x1, x2):
    """模擬量子核：將資料映射到量子態"""
    # 編碼到量子態
    def encode(x):
        theta = np.arctan(x)
        return np.array([np.cos(theta), np.sin(theta)])
    
    phi1 = encode(x1)
    phi2 = encode(x2)
    
    # 量子核 = |<φ(x₁)|φ(x₂)>|²
    overlap = np.abs(np.dot(phi1, phi2))**2
    return overlap

# 產生量子核矩陣
def build_kernel_matrix(X):
    n = len(X)
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            K[i, j] = quantum_kernel(X[i], X[j])
    return K
```

## 與古典 SVM 比較

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=100, n_features=2, random_state=42)

# 量子核 SVM
K_train = build_kernel_matrix(X)
qsvm = SVC(kernel='precomputed')
qsvm.fit(K_train, y)

# 古典 RBF SVM
svm = SVC(kernel='rbf')
svm.fit(X, y)

# 交叉驗證比較
# 量子 SVM 在小資料集上通常表現更好
scores_q = cross_val_score(qsvm, K_train, y, cv=3)
scores_c = cross_val_score(svm, X, y, cv=3)

print(f"Quantum SVM: {scores_q.mean():.3f} ± {scores_q.std():.3f}")
print(f"Classical SVM: {scores_c.mean():.3f} ± {scores_c.std():.3f}")
```

## 量子優勢

量子核的優勢在於：量子態的 Hilbert 空間維度隨 qubit 數指數增長，使原本線性不可分的資料在高維空間中變得可分。近期研究顯示，量子核在特定結構化資料上具有量子優勢。

## 結語

量子支援向量機是量子 ML 中最成熟的演算法之一，已在化學分子分類、影像識別等領域展現潛力。

---

**延伸閱讀**

- [Quantum SVM 論文](https://www.google.com/search?q=quantum+support+vector+machine+kernel)
- [量子核方法綜述](https://www.google.com/search?q=quantum+kernel+methods+machine+learning)
- [Quantum SVM vs Classical](https://www.google.com/search?q=quantum+SVM+advantage+2024+2025)
