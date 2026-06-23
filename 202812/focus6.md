# AI 安全與監管進展

## 從自願承諾到強制合規

2028 年是 AI 監管從「軟性指引」轉向「強制法律」的一年。EU AI Act 全面實施、CVE 納入 AI 漏洞、全球治理框架成形。

### EU AI Act 全面實施

2028 年 6 月，歐盟 AI Act 正式生效。其核心要求：

- **高風險 AI 系統**：必須通過 CE 認證，包含可解釋性報告與人為監督機制
- **通用 AI（GPAI）**：訓練資料須公開摘要，模型須通過紅隊測試
- **處罰機制**：違規最高處以全球年營收 7% 的罰款

### AI 安全漏洞通報

2028 年 11 月，CVE（Common Vulnerabilities and Exposures）正式納入 AI 安全漏洞分類。常見的 AI 漏洞包括：

```python
ai_vulnerabilities = {
    "CVE-2028-001": "Prompt Injection — 繞過系統提示",
    "CVE-2028-002": "Model Inversion — 從輸出還原訓練資料",
    "CVE-2028-003": "Adversarial Patch — 實體世界對抗攻擊",
    "CVE-2028-004": "Supply Chain Poisoning — 汙染開源模型權重",
}
for cve, desc in ai_vulnerabilities.items():
    severity = "HIGH" if "繞過" in desc or "還原" in desc else "MEDIUM"
    print(f"{cve}: {desc} [{severity}]")
```

### 全球治理進展

- **美國**：NIST AI 安全框架 3.0 發布，新增 Agent 安全指引
- **中國**：新一代 AI 治理規範要求生成內容浮水印標準化
- **聯合國**：28 國簽署《AI 安全合作框架》，建立跨國 AI 事故通報機制

### 安全技術突破

2028 年的 AI 安全技術出現三大突破：

1. **可證明安全浮水印**：基於加密簽章的生成內容標記，理論上不可偽造
2. **即時對抗檢測**：在推論過程中檢測輸入是否為對抗樣本，延遲增加 <5%
3. **聯邦紅隊測試**：多家機構共享對抗攻擊手法，聯合提升模型安全性

### 2028 年的數據

```python
from _code.annual_report import ANNUAL_METRICS
safety_metric = ANNUAL_METRICS[4]  # AI Safety Incidents
print(f"AI 安全事故: Q1={safety_metric.q1} → Q4={safety_metric.q4}")
print(f"全年降幅: {safety_metric.growth():+.0f}% (下降為改善)")
```

AI 安全事故在 2028 年下降了 50%，證明監管與安全技術正在發揮作用。

## 延伸閱讀

- [EU AI Act 2028 enforcement](https://www.google.com/search?q=EU+AI+Act+2028+enforcement+penalties)
- [CVE AI vulnerabilities 2028](https://www.google.com/search?q=CVE+AI+vulnerabilities+2028+classification)
- [Global AI safety framework 2028](https://www.google.com/search?q=2028+global+AI+safety+cooperation+framework)
