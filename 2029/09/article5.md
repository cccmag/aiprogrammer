# AI 輔助實驗設計

## 從經驗驅動到數據驅動

傳統實驗設計依賴研究人員的直覺和經驗，容易陷入偏誤。貝氏優化和主動學習將實驗設計轉變為系統化優化問題，大幅提高實驗效率。

## 貝氏優化與主動學習

貝氏優化利用高斯過程代理模型，在探索（exploration）與利用（exploitation）之間取得平衡。主動學習則迭代選擇最有資訊量的樣本進行標註，減少所需實驗次數。

```python
# 貝氏優化示意：最大化 f(x) = sin(x) + noise
import numpy as np

class GaussianProcess:
    def __init__(self, length_scale=0.5):
        self.length_scale = length_scale
        self.X_obs = []
        self.y_obs = []
    
    def kernel(self, x1, x2):
        return np.exp(-0.5 * ((x1 - x2) / self.length_scale) ** 2)
    
    def update(self, x, y):
        self.X_obs.append(x)
        self.y_obs.append(y)
    
    def predict(self, x_star):
        if not self.X_obs:
            return 0.0, 1.0
        K = np.array([[self.kernel(xi, xj) for xj in self.X_obs] for xi in self.X_obs])
        k_s = np.array([self.kernel(x, xi) for xi in self.X_obs])
        mu = k_s @ np.linalg.solve(K, self.y_obs)
        sigma = self.kernel(x, x) - k_s @ np.linalg.solve(K, k_s.reshape(-1, 1))
        return mu, np.sqrt(sigma)
    
    def propose(self, x_candidates):
        scores = []
        for x in x_candidates:
            mu, sigma = self.predict(x)
            scores.append(mu + 1.96 * sigma)  # UCB
        return x_candidates[np.argmax(scores)]

gp = GaussianProcess()
for i in range(5):
    x_next = gp.propose(np.linspace(0, 6, 50))
    y_obs = np.sin(x_next) + np.random.randn() * 0.1
    gp.update(x_next, y_obs)
print(f"建議下個實驗點: x = {x_next:.3f}")
```

## 自動化合成平台

AI 與機器人結合形成「自動化科學家」平台。例如，利物浦大學的移動機器人可自主進行化學實驗，優化光催化產氫條件。這些平台 24 小時運作，大幅提升產能。

## 實驗設計中的公平性

AI 輔助設計需注意數據偏差問題。如果訓練數據集中在某些化學空間，模型可能忽略有潛力的新區域。多樣性獎勵和多目標優化有助於緩解此問題。

> 參考資料：https://www.google.com/search?q=AI+experimental+design+bayesian+optimization
