# Policy Gradient 詳解

Policy Gradient 直接優化策略函數。

## 1. 策略梯度定理

∇J(π) = E[∇ log π(a|s) * G]

## 2. REINFORCE 演算法

```python
loss = -log_prob(action) * return_
loss.backward()
```

## 3. 優勢

- 可以處理連續動作空間
- 更平滑的策略收斂

## 4. 方差問題

使用基線來減少方差：
advantage = return - baseline

---

## 延伸閱讀

- [Policy Gradient 論文](https://www.google.com/search?q=REINFORCE+policy+gradient+Williams+1992)
- [PPO 論文](https://www.google.com/search?q=PPO+proximal+policy+optimization+Schulman+2017)