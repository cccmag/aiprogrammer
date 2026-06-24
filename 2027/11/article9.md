# 企業 AI 安全治理實務

## 1. 引言

當 AI 系統從實驗室進入生產環境，安全性不再是研究問題而是營運問題。企業需要建立從開發到部署的完整 AI 安全治理框架，包含風險評估、安全測試、事件回應、持續監控等環節。

## 2. AI 安全治理框架

### NIST AI Risk Management Framework

NIST 的 AI RMF 是目前最具影響力的治理框架，包含四大功能：**GOVERN（治理）**—安全文化與角色責任；**MAP（測繪）**—風險識別與分類；**MEASURE（評估）**—安全測試與紅隊演練；**MANAGE（管理）**—風險緩解與事件回應。

### 風險評估範例

```python
def assess_prompt_injection_risk(config):
    score = 0
    if config["user_input"] == "direct": score += 3
    if config["tool_access"] == "elevated": score += 2
    if config["input_filter"] == "none": score += 3
    return {
        "risk": "high" if score >= 5 else "medium",
        "mitigations": ["implement_input_filter",
                        "restrict_tool_permissions"]
    }
```

## 3. AI 安全營運（AISecOps）

### 事件回應程序

```python
def respond_to_incident(incident_type, severity):
    isolate_model(incident_type)     # 隔離受影響的模型
    log_attack_chain(incident_type)  # 記錄攻擊鏈
    execute_mitigation(incident_type, severity)
    notify_stakeholders(incident_type, severity)
```

### 持續監控指標

| 指標 | 說明 | 告警閾值 |
|------|-----|---------|
| 拒絕率 | 模型拒絕不安全請求的比例 | < 80% |
| 異常輸出率 | 輸出包含敏感資訊的比例 | > 0.1% |
| API 查詢異常 | 單一 IP 查詢量突然暴增 | > 3σ |
| 模型漂移 | 輸出分布與基線的差異 | > KL 0.05 |
| 延遲異常 | 回應時間的異常變化 | > 2x 基線 |

## 4. 第三方安全管理

供應商（如 OpenAI、Anthropic、Google）的 AI 服務也需要納入企業安全管理範圍：

```python
class ThirdPartyAISecurity:
    def __init__(self, vendors):
        self.vendors = vendors

    def vendor_security_assessment(self, vendor_name):
        vendor = self.vendors[vendor_name]
        checks = {
            "SOC2 Type II": vendor.soc2_type2,
            "red_team_frequency": vendor.red_team_freq,
            "data_retention": vendor.data_retention_days,
            "eu_ai_act": vendor.eu_ai_act_compliant,
        }
        return all(checks.values())
```

## 5. 實務案例

某大型銀行部署客服 LLM 的安全架構：使用者 → WAF（注入過濾）→ LLM 閘道（內容檢查）→ 私有雲部署的 LLM（無網路存取）→ 輸出過濾器（PII 遮罩）→ 審計日誌。關鍵決策包括私有部署、無網路存取、雙層過濾、完整審計。

## 6. 結語

企業 AI 安全治理不是一次性專案，而是持續的流程。NIST AI RMF 提供了框架，但實際落地需要整合到現有的安全營運體系中。關鍵是將 AI 安全視為企業風險管理的一部分，而非獨立的技術問題。

---

## 延伸閱讀

- [NIST AI RMF 完整文件](https://www.google.com/search?q=NIST+AI+Risk+Management+Framework)
- [OWASP AI 安全指南](https://www.google.com/search?q=OWASP+AI+security+guidance)
- [金融業 AI 治理指引](https://www.google.com/search?q=financial+services+AI+governance)
