# 反事實推理與干預（2000-2028）

## 什麼是反事實？

反事實（Counterfactual）思考：「如果當時沒有抽菸，現在會得肺癌嗎？」形式化為 $Y_{X=x}(u)$——在個體 $u$ 上施加干預 $X=x$ 後的結果。

## 干預 vs. 條件

條件機率 $P(Y|X=x)$ 與干預機率 $P(Y|do(X=x))$ 本質不同。條件機率只是篩選數據，干預則改變整個數據生成機制。SCM 中，干預相當於移除所有指向 $X$ 的邊。

## 反事實的計算

給定 SCM 和觀察證據，反事實推理三步驟：

1. **外推**（Abduction）：用證據更新外生變數的後驗分佈
2. **干預**（Action）：將模型中 $X$ 設為反事實值
3. **預測**（Prediction）：用更新後的模型計算 $Y$

## 生成式反事實

2020 年代後期，GAN 與擴散模型被用於生成反事實樣本。例如：給定一張「狼」的圖片，生成「如果背景不是雪地，模型還會分類為狼嗎？」這與 XAI（可解釋 AI）深度結合。

## Python 範例：簡單干預計算

```python
import numpy as np

# 模擬數據: X -> Y
np.random.seed(42)
X = np.random.normal(0, 1, 1000)
Y = 2 * X + np.random.normal(0, 0.5, 1000)

# 條件期望 E[Y|X=1]
cond = np.mean(Y[X > 0.99 & (X < 1.01)])
print(f"E[Y|X=1] ≈ {cond:.2f}")

# 干預 do(X=1): 直接設定 X=1，Y=2*1+noise
interv = 2 * 1 + np.random.normal(0, 0.5, 10000)
print(f"E[Y|do(X=1)] ≈ {np.mean(interv):.2f}")
```

參考：[搜尋 反事實推理](https://www.google.com/search?q=%E5%8F%8D%E4%BA%8B%E5%AF%A6%E6%8E%A8%E7%90%86) | [搜尋 Counterfactual XAI](https://www.google.com/search?q=Counterfactual+XAI)
