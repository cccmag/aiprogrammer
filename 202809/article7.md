# 可解釋性評估：如何衡量一個解釋的好壞

## 前言

當我們有了 SHAP 值、LIME 係數、反事實解釋之後，一個關鍵問題浮現：**如何判斷這些解釋是否正確？** 2026 年的 XAI 社群已經提出了多維度的評估框架，從忠誠度到穩定性，從人類認知到法規合規。

## 六個評估維度

### 1. 忠誠度（Fidelity）

忠誠度衡量解釋在多大程度上真實反映了模型的決策邏輯：

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification


def fidelity_score(model, X, explain_func, n_samples=100):
    """Test if explanation is faithful to model."""
    correct = 0
    for i in range(min(n_samples, X.shape[0])):
        x = X[i:i+1]
        pred = model.predict(x)[0]
        explanation = explain_func(model, x)

        # Remove top positive feature
        top_feat = explanation["importance"][0]
        x_perturbed = x.copy()
        x_perturbed[0, top_feat] = 0

        pred_after = model.predict(x_perturbed)[0]
        if pred_after != pred:
            correct += 1  # Feature removal changed prediction -> faithful
    return correct / n_samples


def dummy_shap(model, x):
    """Simplified SHAP for demonstration."""
    coefs = np.abs(x[0])
    return {"importance": np.argsort(-coefs)}
```

### 2. 穩定性（Stability）

對相似的輸入，解釋應該也相似。這是 LIME 長期被批評的痛點：

```python
def stability_score(model, explain_func, x_base, n_perturb=50):
    """Measure variance of explanations across similar inputs."""
    explanations = []
    for _ in range(n_perturb):
        noise = np.random.normal(0, 0.01, x_base.shape)
        x_pert = x_base + noise
        explanations.append(explain_func(model, x_pert))

    # Compute pairwise similarity
    similarities = []
    for i in range(len(explanations)):
        for j in range(i + 1, len(explanations)):
            sim = 1 - np.linalg.norm(
                explanations[i]["importance"] - explanations[j]["importance"]
            ) / len(x_base[0])
            similarities.append(sim)
    return float(np.mean(similarities))
```

### 3. 簡潔性（Simplicity / Sparsity）

人類能同時處理的資訊有限。好的解釋應該只包含最重要的特徵：

```python
def sparsity_score(explanation, k=3):
    """Fraction of features needed for the top-k explanation."""
    total = len(explanation["importance"])
    top_k = explanation["importance"][:k]
    return k / total if total > 0 else 0.0
```

### 4. 可理解性（Comprehensibility）

這是最難量化的維度，通常透過使用者實驗評估：

- **時間度量**：使用者多快能理解解釋並做出正確決策？
- **正確率**：使用者根據解釋能否正確預測模型的行為？
- **滿意度調查**：使用者認為解釋是否合理？

### 5. 覆蓋率（Coverage）

解釋應涵蓋模型的關鍵決策邊界，而非只針對少數樣本：

```python
def coverage_score(model, explain_func, X):
    """Fraction of samples with high-fidelity explanations."""
    scores = []
    for i in range(X.shape[0]):
        x = X[i:i+1]
        pred = model.predict(x)[0]
        expl = explain_func(model, x)
        top_feats = expl["importance"][:3]
        x_masked = x.copy()
        x_masked[0, top_feats] = 0
        new_pred = model.predict(x_masked)[0]
        scores.append(new_pred != pred)
    return np.mean(scores)
```

### 6. 計算效率（Efficiency）

```python
import time

def efficiency_score(model, explain_func, X, n_samples=20):
    start = time.time()
    for _ in range(n_samples):
        idx = np.random.randint(X.shape[0])
        explain_func(model, X[idx:idx+1])
    elapsed = time.time() - start
    return elapsed / n_samples
```

## 綜合評估框架

```python
def comprehensive_evaluation(model, X, explain_func):
    return {
        "fidelity": fidelity_score(model, X, explain_func),
        "stability": stability_score(model, explain_func, X[0:1]),
        "sparsity": np.mean([sparsity_score(explain_func(model, X[i:i+1]))
                            for i in range(min(20, X.shape[0]))]),
        "efficiency_seconds": efficiency_score(model, explain_func, X)
    }


X, y = make_classification(n_samples=200, n_features=10, random_state=42)
model = RandomForestClassifier(n_estimators=50).fit(X, y)

metrics = comprehensive_evaluation(model, X, dummy_shap)
for k, v in metrics.items():
    print(f"{k}: {v:.3f}")
```

## 2026 年的評估標準趨勢

- **XAI Benchmark**：Kaggle 與 NeurIPS 持續舉辦可解釋性競賽，提供標準化評估套件。
- **法規驅動的指標**：歐盟 AI Act 要求高風險系統提供「有意義的解釋」，雖然沒有明確定義量化指標，但忠誠度與穩定性已被業界接受為基本要求。
- **人類-模型協作實驗**：越來越多研究關注解釋是否真的幫助人類做出更好的決策。

## 結語

衡量解釋的好壞本身就是一個開放性問題。沒有一個指標能全面反映解釋的品質——忠誠度高的解釋可能太複雜，簡潔的解釋可能不忠誠。實務上需要根據應用場景權衡，在法規、效能、使用者體驗之間找到平衡點。

---

**延伸閱讀**
- [Quantitative Evaluation of XAI Methods](https://www.google.com/search?q=quantitative+evaluation+XAI+methods+fidelity+stability)
- [XAI Benchmark Suite](https://www.google.com/search?q=XAI+benchmark+explainability+evaluation+framework)
- [歐盟 AI Act 可解釋性要求](https://www.google.com/search?q=EU+AI+Act+explainability+requirements+high+risk)
