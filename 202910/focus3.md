# 公平性評估方法

## Demographic Parity、Equal Opportunity、Equalized Odds（2021-2029）

### 公平性的數學定義

公平性不是單一概念——至少有 21 種不同的公平性定義。最常用的三種如下。

### Demographic Parity（人口統計平權）

要求模型對不同群體的正面預測率相等：

```python
def demographic_parity(y_pred: list, groups: list) -> float:
    """計算人口統計平權差異（越小越公平）"""
    unique_groups = set(groups)
    rates = {}
    for g in unique_groups:
        mask = [i for i, grp in enumerate(groups) if grp == g]
        preds = [y_pred[i] for i in mask]
        rates[g] = sum(preds) / len(preds) if preds else 0

    values = list(rates.values())
    return max(values) - min(values)  # 理想值為 0
```

### Equal Opportunity（平等機會）

要求模型對**真實為正**的樣本，在不同群體中有相同的真陽性率（TPR）：

```python
def equal_opportunity(y_true: list, y_pred: list, groups: list) -> float:
    """計算 TPR 差異"""
    metrics = {}
    for g in set(groups):
        mask = [i for i, grp in enumerate(groups) if grp == g and y_true[i] == 1]
        if not mask:
            continue
        tpr = sum(y_pred[i] for i in mask) / len(mask)
        metrics[g] = tpr

    if len(metrics) < 2:
        return 0.0
    return max(metrics.values()) - min(metrics.values())
```

### Equalized Odds（均等化勝算）

同時要求**真陽性率（TPR）和假陽性率（FPR）**在群體間相等：

```python
def equalized_odds(y_true: list, y_pred: list, groups: list) -> dict:
    """同時檢查 TPR 與 FPR 的群體差異"""
    def rate_for(y_true_seg, y_pred_seg, positive):
        if not y_true_seg:
            return 0.0
        mask = [i for i in range(len(y_true_seg)) if y_true_seg[i] == (1 if positive else 0)]
        if not mask:
            return 0.0
        return sum(y_pred_seg[i] for i in mask) / len(mask)

    all_groups = set(groups)
    tprs, fprs = {}, {}
    for g in all_groups:
        mask = [i for i, grp in enumerate(groups) if grp == g]
        yt = [y_true[i] for i in mask]
        yp = [y_pred[i] for i in mask]
        tprs[g] = rate_for(yt, yp, True)
        fprs[g] = rate_for(yt, yp, False)

    return {
        "TPR_disparity": max(tprs.values()) - min(tprs.values()),
        "FPR_disparity": max(fprs.values()) - min(fprs.values()),
    }
```

### 公平性悖論

```python
# 公平性悖論範例：滿足 DP 可能違反 EO
def fairness_paradox_demo():
    data = {
        "group_A": {"good": 80, "bad": 20, "pred_pos": 50},
        "group_B": {"good": 40, "bad": 60, "pred_pos": 50},
    }
    # DP = 0.5-0.5 = 0 ✅
    # EO: TPR_A = 50/80=0.625, TPR_B = 50/40 > 1 ❌

    dp_a = data["group_A"]["pred_pos"] / 100
    dp_b = data["group_B"]["pred_pos"] / 100
    print(f"DP disparity: {abs(dp_a - dp_b):.2f}")

    tpr_a = data["group_A"]["pred_pos"] / data["group_A"]["good"]
    tpr_b = data["group_B"]["pred_pos"] / data["group_B"]["good"]
    print(f"EO disparity: {abs(tpr_a - tpr_b):.2f}")
```

### 公平性指標選用建議

| 場景 | 建議指標 | 原因 |
|------|---------|------|
| 徵才篩選 | Equal Opportunity | 避免遺漏合格者 |
| 信用評分 | Demographic Parity | 要求貸款核准率一致 |
| 醫療診斷 | Equalized Odds | FPR 與 TPR 同等重要 |
| 刑事司法 | Predictive Parity | 確保預測精確度一致 |

---

**下一步**：[透明度與可解釋性報告](focus4.md)

## 延伸閱讀

- [Fairness Metrics 綜述](https://www.google.com/search?q=20+fairness+definitions+AI)
- [Demographic Parity vs Equal Opportunity](https://www.google.com/search?q=demographic+parity+equal+opportunity+difference)
- [Equalized Odds 論文](https://www.google.com/search?q=equalized+odds+Hardt+2016)
