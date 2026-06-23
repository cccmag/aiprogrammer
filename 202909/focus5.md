# AI 輔助實驗設計（2023-2029）

## 貝氏最佳化與主動學習

2023 年之後，主動學習（Active Learning）從機器學習研究走進真實實驗室。其核心思想是：讓 AI 決定「下一步該做什麼實驗」，以最少實驗次數取得最大資訊量。

```
貝氏最佳化工作流程：
初始數據 → 建立高斯過程模型 → 採集函數選取候選點
→ 執行實驗 → 更新模型 → 重複
```

## 高斯過程建模

高斯過程（GP）是實驗設計的標準工具，不僅給出預測值，還提供不確定性估計：

```python
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, RBF

def active_learning_loop(X_init, y_init, n_iterations=20):
    kernel = Matern(length_scale=1.0, nu=2.5)
    gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-6)
    gp.fit(X_init, y_init)
    for i in range(n_iterations):
        X_candidates = sample_candidates(10000)
        mean, std = gp.predict(X_candidates, return_std=True)
        acquisition = mean - 2.0 * std  # Lower Confidence Bound
        best_idx = np.argmin(acquisition)
        X_next = X_candidates[best_idx]
        y_next = run_experiment(X_next)
        gp.fit(np.vstack([X_init, X_next]), np.concatenate([y_init, y_next]))
```

## 自主實驗室

2024-2026 年間，世界各地的自主實驗室（Self-Driving Labs）相繼投入使用。這些實驗室整合了機械手臂、自動化合成設備和 AI 決策引擎。

知名系統包括：
- **A-Lab**（Berkeley/DeepMind）— 自動材料合成與分析
- **Ada**（IBM）— 自動化有機合成
- **ChemOS**（MIT/多倫多大學）— 化學探索最佳化平台

## 實驗規劃的數學基礎

```python
def expected_improvement(gp, X, y_best):
    mean, std = gp.predict(X, return_std=True)
    z = (mean - y_best) / (std + 1e-9)
    return (mean - y_best) * norm.cdf(z) + std * norm.pdf(z)
```

這條採集函數平衡了探索（高不確定性的區域）和利用（預測值最優的區域）。

## 2027-2029 趨勢

- **人機協作**：AI 負責實驗規劃和數據分析，人類專注於創意和異常案例
- **多目標最佳化**：同時優化多個互相衝突的性質（如活性 vs. 毒性）
- **端到端自動化**：從文獻閱讀到實驗執行的全自動化工作流

## 參考資源

- [貝氏最佳化實驗設計](https://www.google.com/search?q=Bayesian+optimization+experimental+design)
- [Self-Driving Lab 自主實驗室](https://www.google.com/search?q=self-driving+lab+automated+science)
- [Expected Improvement 採集函數](https://www.google.com/search?q=expected+improvement+acquisition+function)
