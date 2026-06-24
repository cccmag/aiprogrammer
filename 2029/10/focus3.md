# 公平性評估方法

## 從統計平權到個體公平的量化指標（2021-2029）

### 前言

公平性不是一個單一的數學概念。同一套模型，用不同的公平性指標評估，可能得到完全相反的結論。理解各種指標的假設與取捨，是負責任 AI 工程師的核心能力。

### 四大公平性指標家族

```python
import numpy as np
import pandas as pd

class FairnessMetrics:
    """公平性指標計算工具箱"""
    
    @staticmethod
    def demographic_parity(y_pred: np.ndarray, sensitive: np.ndarray):
        """人口統計平權：各群體接受率應相等"""
        groups = np.unique(sensitive)
        rates = {}
        for g in groups:
            mask = sensitive == g
            rates[f'group_{g}'] = y_pred[mask].mean()
        return rates
    
    @staticmethod
    def equal_opportunity(y_true: np.ndarray, y_pred: np.ndarray,
                          sensitive: np.ndarray):
        """平等機會：各群體的真陽性率應相等"""
        groups = np.unique(sensitive)
        tpr = {}
        for g in groups:
            mask = (sensitive == g) & (y_true == 1)
            if mask.sum() == 0:
                tpr[f'group_{g}'] = None
            else:
                tpr[f'group_{g}'] = (y_pred[mask] == 1).mean()
        return tpr
    
    @staticmethod
    def equalized_odds(y_true: np.ndarray, y_pred: np.ndarray,
                       sensitive: np.ndarray):
        """均等機會：各群體的 FPR 與 TPR 應相等"""
        groups = np.unique(sensitive)
        result = {}
        for g in groups:
            mask_pos = (sensitive == g) & (y_true == 1)
            mask_neg = (sensitive == g) & (y_true == 0)
            tpr = (y_pred[mask_pos] == 1).mean() if mask_pos.sum() > 0 else None
            fpr = (y_pred[mask_neg] == 1).mean() if mask_neg.sum() > 0 else None
            result[f'group_{g}'] = {'TPR': tpr, 'FPR': fpr}
        return result
    
    @staticmethod
    def predictive_parity(y_true: np.ndarray, y_pred: np.ndarray,
                          sensitive: np.ndarray):
        """預測平權：各群體的精確率應相等"""
        groups = np.unique(sensitive)
        precision = {}
        for g in groups:
            mask = (sensitive == g) & (y_pred == 1)
            if mask.sum() == 0:
                precision[f'group_{g}'] = None
            else:
                precision[f'group_{g}'] = (y_true[mask] == 1).mean()
        return precision
```

### 指標衝突案例

```python
def demonstrate_impossibility():
    """展示不可能定理：無法同時滿足所有公平性指標"""
    np.random.seed(42)
    n = 1000
    
    # 兩群體、不平衡的基礎比率
    sensitive = np.array([0] * 700 + [1] * 300)
    y_true = np.array([1] * 400 + [0] * 300 + [1] * 50 + [0] * 250)
    
    # 一個「完美校準」的模型
    y_pred = np.array([1] * 350 + [0] * 350 + [1] * 80 + [0] * 220)
    
    fm = FairnessMetrics()
    
    dp = fm.demographic_parity(y_pred, sensitive)
    eo = fm.equal_opportunity(y_true, y_pred, sensitive)
    
    print("Demographic Parity:", dp)
    print("Equal Opportunity:", eo)
    print("註：當基礎比率不同時，DP 與 EO 不可能同時滿足")
```

### 個體公平性

群體公平性指標之外，個體公平要求「相似個體應獲得相似預測」：

```python
from sklearn.metrics.pairwise import cosine_similarity

def individual_fairness(X: np.ndarray, y_pred: np.ndarray,
                        similarity_threshold: float = 0.95) -> float:
    """計算個體公平性分數
    
    找到所有相似對（cosine similarity > threshold），
    檢查它們是否被一致預測
    """
    sim_matrix = cosine_similarity(X)
    n = len(y_pred)
    violations = 0
    total_pairs = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i, j] >= similarity_threshold:
                total_pairs += 1
                if y_pred[i] != y_pred[j]:
                    violations += 1
    
    if total_pairs == 0:
        return 1.0
    return 1 - violations / total_pairs

# 使用範例
X = np.random.randn(100, 5)
y_pred = np.random.randint(0, 2, 100)
fairness_score = individual_fairness(X, y_pred)
print(f"Individual Fairness Score: {fairness_score:.3f}")
```

### 交叉性評估（Intersectionality）

單一維度的公平性評估可能掩蓋交叉群體的偏見：

```python
def intersectional_analysis(df: pd.DataFrame, y_pred: str,
                            attrs: list) -> pd.DataFrame:
    """交叉性分析：同時檢查多個受保護屬性的組合"""
    results = []
    df['predicted'] = y_pred
    
    # 生成所有屬性組合
    from itertools import product
    unique_vals = [df[a].unique() for a in attrs]
    
    for combo in product(*unique_vals):
        mask = pd.Series([True] * len(df))
        for attr, val in zip(attrs, combo):
            mask &= (df[attr] == val)
        
        if mask.sum() >= 10:  # 最小樣本數
            acceptance = df.loc[mask, 'predicted'].mean()
            results.append({
                'combination': combo,
                'sample_size': mask.sum(),
                'acceptance_rate': acceptance,
            })
    
    return pd.DataFrame(results)
```

### 評估方法演進

| 年份 | 方法 |
|------|------|
| 2021 | 單一維度 DP/EO 指標 |
| 2022 | 交叉性分析工具 |
| 2023 | 因果公平性框架 |
| 2024 | 反事實公平性評估 |
| 2025 | 動態公平性監控儀表板 |
| 2027 | 公平性自動化測試套件 |
| 2029 | 跨模態公平性評估（文字+影像） |

### 小結

公平性評估沒有銀彈。工程師需要理解業務上下文，選擇合適的指標組合，並接受 trade-off。關鍵是：將公平性評估嵌入 CI/CD 管線，而非事後補救。

---

**下一步**：[透明度與可解釋性報告](focus4.md)

## 延伸閱讀

- [Fairness Metrics 綜述](https://www.google.com/search?q=fairness+metrics+machine+learning+survey)
- [Impossibility Theorem of Fairness](https://www.google.com/search?q=impossibility+theorem+fairness+machine+learning)
- [Intersectional Fairness](https://www.google.com/search?q=intersectional+fairness+AI)
