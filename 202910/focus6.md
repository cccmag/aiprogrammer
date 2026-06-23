# 全球 AI 監管比較

## EU AI Act、美國 AI EO、中國生成式 AI 管理辦法（2022-2029）

### 三大監管路徑

全球 AI 監管在 2022 年之後快速分化為三大路徑：**歐盟的人權本位**、**美國的創新優先**、**中國的安全與控制**。

### 比較架構

```python
class RegulatoryComparison:
    def __init__(self):
        self.regions = {
            "EU": {
                "framework": "EU AI Act",
                "effective": "2026 (phased)",
                "approach": "Risk-based",
                "has_fines": True,
                "max_penalty": "35M EUR or 7% revenue",
                "req_registration": True,
                "req_explainability": True,
            },
            "USA": {
                "framework": "AI Executive Order + Blueprint",
                "effective": "2023-2025",
                "approach": "Sectoral + voluntary",
                "has_fines": False,
                "max_penalty": "N/A",
                "req_registration": False,
                "req_explainability": False,
            },
            "China": {
                "framework": "Generative AI Measures",
                "effective": "2023",
                "approach": "Centralized control",
                "has_fines": True,
                "max_penalty": "Unknown",
                "req_registration": True,
                "req_explainability": True,
            },
        }

    def compliance_check(self, system_type: str, deploy_region: str) -> dict:
        """檢查特定 AI 系統在特定區域的合規要求"""
        region = self.regions.get(deploy_region, {})
        return region
```

### 關鍵比較維度

| 維度 | 歐盟 | 美國 | 中國 |
|------|------|------|------|
| 立法形式 | 統一法案 | 行政命令 + 自願框架 | 部門規章 |
| 風險分類 | 四級制 | 無統一分類 | 內容安全分類 |
| 高風險定義 | 特定應用領域 | 由各機構自訂 | 社會穩定 + 國家安全 |
| 罰則 | 高額罰款 | 無直接罰款 | 撤銷許可 + 罰款 |
| 透明義務 | 詳盡的技術文件 | 自願報告 | 演算法備案 |
| 基礎模型規範 | ✅ GPAI 章節 | 未明確規範 | ✅ 生成式內容標記 |

### 監管合規檢查器

```python
class ComplianceChecker:
    def __init__(self):
        self.requirements = {
            "EU": ["risk_assessment", "technical_doc", "human_oversight",
                   "accuracy", "robustness", "transparency"],
            "USA": ["self_assessment", "watermark"],
            "China": ["algorithm_filing", "content_review", "user_id_protection",
                      "training_data_legality"],
        }

    def check(self, region: str, capabilities: set) -> dict:
        needed = self.requirements.get(region, [])
        return {
            "missing": [r for r in needed if r not in capabilities],
            "compliant": len(needed) == 0,
            "compliance_pct": len(capabilities & set(needed)) / len(needed) * 100
            if needed else 100,
        }
```

### 監管趨勢

**2022-2023**：歐盟 AI Act 草案討論、美國 AI 行政命令發布、中國生成式 AI 管理辦法實施。

**2024**：AI Act 正式通過、美國各州開始立法、中國發布全球 AI 治理倡議。

**2025-2026**：AI Act 分階段生效、美國 NIST 推出 AI 安全測試平台、各國開始討論邊境 AI 治理。

**2027-2029**：預測三大監管體系將出現趨同——所有主要經濟體都將要求高風險 AI 系統進行註冊、透明度和人機協作。

### 監管套利的風險

企業可能將高風險 AI 系統部署在監管較鬆的區域——這正是「布魯塞爾效應」的反面。2026 年後，預計歐盟將要求進口 AI 系統同樣符合 AI Act 標準，類似 GDPR 的域外效力。

---

**下一步**：[負責任 AI 的未來](focus7.md)

## 延伸閱讀

- [EU AI Act 全文](https://www.google.com/search?q=EU+AI+Act+full+text)
- [US AI Executive Order 2023](https://www.google.com/search?q=US+AI+executive+order+2023+safe+secure)
- [China Generative AI Measures](https://www.google.com/search?q=China+generative+AI+regulation+2023)
