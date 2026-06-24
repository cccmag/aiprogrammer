# 貝氏學習理論

## 貝氏觀點vs頻率派觀點

機器學習中存在兩種主要的機率論觀點：

**頻率派**：參數 θ 是固定的未知常數，資料是隨機的
**貝氏派**：參數 θ 是隨機變數，我們透過資料更新對它的信念

貝氏學習的核心優勢在於**不確定性的量化**——不僅給出預測值，還給出預測的信心程度。

## 貝氏定理

貝氏學習的數學基礎是貝氏定理：

```
P(θ | D) = P(D | θ) * P(θ) / P(D)
```

其中：
- P(θ) 是**先驗分布**（Prior）——對 θ 的初始信念
- P(D | θ) 是**似然函數**（Likelihood）——給定 θ 下資料的機率
- P(θ | D) 是**後驗分布**（Posterior）——看到資料後對 θ 的更新信念
- P(D) 是**邊際似然**（Marginal Likelihood）——歸一化常數

### 共軛先驗

當先驗和後驗屬於同一分布族時，稱為共軛先驗（Conjugate Prior）。這使得貝氏更新具有閉式解。

**Beta-Binomial 共軛**：

- 似然：Binomial(n, θ) — 伯努利試驗的和
- 先驗：Beta(α, β)
- 後驗：Beta(α + k, β + n - k)

在程式中：

```python
bayesian_update(prior_alpha=2, prior_beta=2, heads=7, tails=3)
# posterior: Beta(9, 5)
```

先驗 Beta(2,2)（均勻分佈，平均 0.5）→ 後驗 Beta(9,5)（平均 0.6429）。

## 貝氏預測

貝氏預測透過邊際化參數來整合不確定性：

```
P(y_new | x_new, D) = ∫ P(y_new | x_new, θ) P(θ | D) dθ
```

這稱為**後驗預測分布**（Posterior Predictive Distribution）。與頻率派不同，貝氏預測自然地考慮了參數的不確定性。

**範例**：在 Beta-Binomial 模型中，預測下一次試驗成功的機率：

```
P(y=1 | D) = E[θ | D] = (α + k) / (α + β + n)
```

## 貝氏學習的步驟

```
初始信念     →  收集資料   →  更新信念   →  做出預測
(Prior)          (Data)      (Posterior)    (Predictive)
```

1. **指定先驗**：P(θ) — 反映先驗知識或信念
2. **定義模型**：P(D | θ) — 資料的產生過程
3. **計算後驗**：P(θ | D) ∝ P(D | θ) P(θ)
4. **預測**：P(y_new | D) = ∫ P(y_new | θ) P(θ | D) dθ

## MAP 估計 vs 完全貝氏

**MAP 估計**（Maximum a Posteriori）：

```
θ̂ = argmax P(θ | D) = argmax [log P(D | θ) + log P(θ)]
```

MAP 找到後驗分布的眾數（mode），忽略了不確定性。

**完全貝氏**則保留整個後驗分布，邊際化所有未知量。

| 方法 | 優點 | 缺點 |
|------|------|------|
| MAP | 計算簡單，等於正則化 MLE | 只給點估計，無不確定性 |
| 完全貝氏 | 完整的不確定性量化 | 積分可能無閉式解 |

## 先驗的選擇

先驗的選擇是貝氏學習中最具爭議的方面：

| 先驗類型 | 說明 | 範例 |
|----------|------|------|
| 無資訊先驗 | 儘量不影響後驗 | 均勻分佈 |
| 共軛先驗 | 計算方便 | Beta, Gaussian |
| 弱資訊先驗 | 加入少量合理資訊 | 中心化、有限方差 |
| 階層先驗 | 多層次的先驗結構 | HLM |

## 貝氏方法的優勢

1. **自然處理不確定性**：後驗分布量化了參數的信念程度
2. **避免過擬合**：邊際化相當於自動的模型平均
3. **先驗知識整合**：可以融入領域知識
4. **在線學習**：後驗可作為新的先驗，實現增量更新
5. **模型比較**：邊際似然自然支持貝氏因子比較

## 高斯過程：貝氏非參數方法

高斯過程將貝氏方法擴展到非參數設定。GP 不是對參數 θ 指定先驗，而是直接對函數 f 指定先驗：

```
f ~ GP(m(x), k(x, x'))
```

其中 m 是均值函數，k 是核函數（協方差函數）。

## 小結

貝氏學習提供了與頻率派不同的學習視角：

| 方面 | 頻率派 | 貝氏派 |
|------|--------|--------|
| 參數 | 固定常數 | 隨機變數 |
| 不確定性 | 信賴區間 | 後驗分布 |
| 正則化 | 懲罰項 | 先驗分布 |
| 預測 | 點估計 | 完整分布 |

---

**下一步**：[程式實作回顧](focus_code.md)

## 延伸閱讀

- [Bayesian Inference Introduction](https://www.google.com/search?q=Bayesian+inference+machine+learning+introduction)
- [Conjugate Prior Explained](https://www.google.com/search?q=conjugate+prior+explained+simply)
- [Gaussian Process Introduction](https://www.google.com/search?q=Gaussian+process+machine+learning+intro)
- [Bayesian vs Frequentist](https://www.google.com/search?q=Bayesian+vs+frequentist+machine+learning)
