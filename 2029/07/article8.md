# AI 安全評估標準

## 概述

建立統一的 AI 安全評估標準是產業落地的重要基礎。本文介紹主流評估框架與實作方法。

## 主要評估框架

### OWASP ML Top 10

對應到可量化指標：

```python
SECURITY_DOMAINS = {
    "ML01": "對抗性攻擊",
    "ML02": "資料中毒",
    "ML03": "模型竊取",
    "ML04": "供應鏈漏洞",
    "ML05": "後門植入",
    "ML06": "隱私洩露",
    "ML07": "提示詞注入",
    "ML08": "權限越界"
}
```

## 量化評分系統

```python
class AISecurityScore:
    def evaluate_adversarial_robustness(self, model, loader, eps=0.03):
        correct = sum(
            (model(pgd_attack(model, x, y, eps)).argmax(1) == y).sum().item()
            for x, y in loader
        )
        return {"score": (correct / len(loader.dataset)) * 10}
```

## 安全等級分類

```python
def classify(score):
    if score >= 8: return "L4: 先進防護"
    if score >= 6: return "L3: 強固防護"
    if score >= 4: return "L2: 基礎防護"
    return "L1: 待改進"
```

## 完整評估報告

```python
def full_security_audit(auditor, datasets):
    results = {
        "adversarial": auditor.evaluate_adversarial_robustness(
            model, datasets["test"]),
        "privacy": auditor.evaluate_membership_inference(
            model, datasets["train"], datasets["holdout"]),
    }
    overall = np.mean([v["score"] for v in results.values()])
    return {"overall": overall, "level": classify(overall),
            "recommendations": [f"加強{domain}"
            for domain, s in results.items() if s["score"] < 6]}
```

## 標準合規性檢查

```python
def compliance_check(model_card):
    required_fields = [
        "model_architecture", "training_data",
        "evaluation_results", "limitations",
        "ethical_considerations", "security_measures"
    ]
    missing = [f for f in required_fields
               if f not in model_card]
    return {
        "compliant": len(missing) == 0,
        "missing_fields": missing
    }
```

參考資料：https://www.google.com/search?q=AI+safety+evaluation+standards+framework+2026
