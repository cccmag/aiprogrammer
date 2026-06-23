# AI 安全評估標準

## 前言

隨著 AI 系統在各行各業的深度部署，標準化的安全評估框架已成為監管機構與企業的共同需求。2025–2026 年間，多個國際標準與評估框架陸續發布，為 AI 安全評估提供了可操作的指引。

## 主要標準框架

### OWASP LLM Top 10

OWASP 發布的 LLM 安全風險排行榜是最廣泛參考的評估框架，涵蓋提示詞注入、敏感資訊揭露、過度代理權限等十大風險類別：

```python
OWASP_RISKS = {
    "LLM01": "提示詞注入",
    "LLM02": "敏感資訊揭露",
    "LLM03": "供應鏈漏洞",
    "LLM04": "資料與模型毒化",
    "LLM05": "不當輸出處理",
    "LLM06": "過度代理權限",
    "LLM07": "系統提示遺漏",
    "LLM08": "向量嵌入弱點",
    "LLM09": "錯誤資訊",
    "LLM10": "無限制的消耗",
}

def assess_risk(model, category):
    test_cases = load_test_cases(category)
    failures = sum(1 for case in test_cases if model.is_vulnerable(case))
    return {"category": category, "risk_score": failures / len(test_cases)}
```

### NIST AI RMF

美國國家標準與技術研究院（NIST）提出的 AI 風險管理框架，強調治理、對應、測量、管理四個核心功能。

## 自動化評估 pipeline

將標準轉換為可自動執行的測試腳本，整合進模型發布流程：

```python
def security_evaluation_pipeline(model):
    results = {}
    for category in OWASP_RISKS:
        results[category] = assess_risk(model, category)
    overall = sum(r["risk_score"] for r in results.values()) / len(results)
    return {"pass": overall < 0.1, "details": results}
```

更多標準與工具可查閱 [https://www.google.com/search?q=AI+safety+evaluation+standards+2026](https://www.google.com/search?q=AI+safety+evaluation+standards+2026)。
