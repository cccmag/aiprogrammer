# 因果 AI 在醫療：從預測到治療決策

## 前言

醫療 AI 是最不該犯錯的領域。傳統機器學習模型可以準確預測疾病風險，但如果無法回答「為什麼這個病人是高風險？」或「如果改變治療方案會怎樣？」，臨床醫生就不會信任它。因果 AI 正在改變這一切——從相關預測走向因果決策。

## 為什麼醫療需要因果推論？

醫療數據充滿混淆偏誤（confounding bias）：病情嚴重的病人更可能接受某種治療，而他們的預後本來就較差。若只用相關性分析，可能會得出「治療反而有害」的錯誤結論。

```python
import numpy as np
from sklearn.linear_model import LogisticRegression


def simulate_clinical_data(n=1000):
    """Simulate: severity -> treatment, severity -> outcome, treatment -> outcome."""
    severity = np.random.uniform(0, 10, n)
    # Sick patients more likely to get treatment
    treatment_prob = 1 / (1 + np.exp(-(severity - 5)))
    treatment = np.random.binomial(1, treatment_prob)
    # Treatment helps, severity hurts
    logit_outcome = -2 + 0.5 * treatment - 0.3 * severity + np.random.normal(0, 1, n)
    outcome = 1 / (1 + np.exp(-logit_outcome))
    return severity, treatment, (outcome > 0.5).astype(float)


def naive_analysis(treatment, outcome):
    """Naive correlation: just compare treat vs no-treat."""
    treat_mean = outcome[treatment == 1].mean()
    no_treat_mean = outcome[treatment == 0].mean()
    return treat_mean - no_treat_mean


def causal_ate(severity, treatment, outcome):
    """Stratified ATE by severity level."""
    ate_total = 0.0
    for q in np.linspace(0.1, 0.9, 9):
        lo, hi = np.percentile(severity, q * 100), np.percentile(severity, (q + 0.1) * 100)
        mask = (severity >= lo) & (severity < hi)
        if mask.sum() > 0:
            ate = (outcome[treatment == 1 & mask].mean()
                   - outcome[treatment == 0 & mask].mean())
            ate_total += ate
    return ate_total / 9


sev, treat, outcome = simulate_clinical_data()
print(f"Naive ATE (biased): {naive_analysis(treat, outcome):.3f}")
print(f"Causal ATE (stratified): {causal_ate(sev, treat, outcome):.3f}")
```

## 個體治療效應（ITE）與反事實預測

群體層面的平均治療效應（ATE）對臨床決策幫助有限——醫生需要的是「這個特定病人」的治療效應。個體治療效應（ITE）正是為此而生：

```python
def estimate_ite(severity, treatment, outcome):
    """Estimate Individual Treatment Effect via T-learner."""
    # Train two models: one for treated, one for control
    treated = severity[treatment == 1].reshape(-1, 1)
    treated_out = outcome[treatment == 1]
    control = severity[treatment == 0].reshape(-1, 1)
    control_out = outcome[treatment == 0]

    from sklearn.ensemble import RandomForestRegressor
    model_treat = RandomForestRegressor(n_estimators=50).fit(treated, treated_out)
    model_control = RandomForestRegressor(n_estimators=50).fit(control, control_out)

    ite = model_treat.predict(severity.reshape(-1, 1)) - model_control.predict(severity.reshape(-1, 1))
    return ite


ite = estimate_ite(sev, treat, outcome)
print(f"\nITE (first 10 patients):")
for i in range(10):
    print(f"  Patient {i+1}: severity={sev[i]:.1f}, ITE={ite[i]:.3f}")
```

## 可解釋性在醫療中的特殊要求

醫療 XAI 不僅是技術問題，更是法規與倫理問題：

- **反事實解釋**：「如果三個月前開始治療，預後會好多少？」
- **SHAP 的臨床應用**：標示哪些特徵對診斷貢獻最大（例如某項血液指標）。
- **因果圖的透明性**：模型使用的特徵路徑必須能被醫生審視。

## 2026 年的醫療因果 AI 案例

- **Sepsis 治療最佳化**：使用 do-calculus 比較不同抗生素方案的因果效應。
- **個人化腫瘤學**：反事實模型預測特定基因突變對化療反應的影響。
- **臨床試驗外推**：從 RCT 數據推論到真實世界族群，校正選擇性偏誤。

## 結語

因果 AI 讓醫療機器學習不再是「只會預測的黑箱」。當醫生可以問「為什麼」並得到基於因果結構的回答時，AI 才從輔助工具轉變為可信賴的臨床夥伴。2026 年的 FDA 與歐盟法規對醫療 AI 的可解釋性要求日益嚴格，因果方法的引入已經從選項變成必然。

---

**延伸閱讀**
- [Causal Inference in Healthcare](https://www.google.com/search?q=causal+inference+healthcare+AI+clinical+decision+support)
- [ITE 估計方法回顧](https://www.google.com/search?q=individual+treatment+effect+estimation+meta+learners)
- [XAI 在臨床應用的挑戰](https://www.google.com/search?q=explainable+AI+clinical+medicine+challenges)
