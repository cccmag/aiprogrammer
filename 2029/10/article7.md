# EU AI Act 合規指南：從分類到實作

## 前言

歐盟 AI Act（EU AI Act）是全球第一部全面性 AI 監管法規，於 2026 年全面生效。它根據風險等級對 AI 系統進行分類，並對高風險系統施加嚴格要求。本文提供合規的技術實作指引。

## 風險分類的 Python 實作

```python
from enum import Enum

class RiskCategory(Enum):
    UNACCEPTABLE = "不可接受風險"
    HIGH = "高風險"
    LIMITED = "有限風險"
    MINIMAL = "最低風險"

class AIActClassifier:
    HIGH_RISK_AREAS = [
        "生物特徵辨識", "關鍵基礎設施", "教育與職業訓練",
        "就業與員工管理", "基本服務存取", "執法",
        "移民與邊境管理", "司法與民主程序"
    ]

    def classify(self, use_case: str, sector: str) -> RiskCategory:
        if "社會評分" in use_case or "即時人臉辨識" in use_case:
            return RiskCategory.UNACCEPTABLE
        if sector in self.HIGH_RISK_AREAS:
            return RiskCategory.HIGH
        if "聊天機器人" in use_case or "內容生成" in use_case:
            return RiskCategory.LIMITED
        return RiskCategory.MINIMAL

    def compliance_requirements(self, category: RiskCategory) -> list:
        base = ["建立風險管理系統", "資料治理措施", "技術文件準備"]
        if category == RiskCategory.UNACCEPTABLE:
            return ["禁止部署"]
        if category == RiskCategory.HIGH:
            return base + [
                "人為監督機制", "透明度義務",
                "準確性與穩健性評估", "CE 標誌申請"
            ]
        if category == RiskCategory.LIMITED:
            return ["透明度揭露", "使用者告知義務"]
        return ["自願行為準則"]

classifier = AIActClassifier()
use_cases = [
    ("應徵者篩選系統", "就業與員工管理"),
    ("即時人臉辨識監控", "執法"),
    ("客服聊天機器人", "客戶服務"),
]
for use_case, sector in use_cases:
    cat = classifier.classify(use_case, sector)
    print(f"{use_case} -> {cat.value}")
    print(f"  要求: {classifier.compliance_requirements(cat)}\n")
```

## 技術文件自動化

```python
def generate_technical_documentation(system_name: str, category: RiskCategory) -> str:
    doc = f"""# 技術文件：{system_name}

## 系統概述
- 系統名稱：{system_name}
- 風險分類：{category.value}
- 製表日期：{__import__('datetime').datetime.now().strftime('%Y-%m-%d')}

## 合規檢查清單
1. 風險管理系統：□ 已建立
2. 資料治理：□ 已實施
3. 透明度揭露：□ 已準備
4. 人為監督：□ 已設計
5. 準確性評估：□ 已完成
6. CE 標誌：□ 待申請
"""
    return doc
```

## 結語

EU AI Act 的合規需要跨部門協作。建議建立合規檢查清單、導入技術文件管理系統，並定期進行法規更新追蹤。

---

**延伸閱讀**

- [EU AI Act 全文](https://www.google.com/search?q=EU+AI+Act+full+text+regulation+2024)
- [歐盟 AI Act 合規指南](https://www.google.com/search?q=EU+AI+Act+compliance+guide+2026)
- [CE 標誌申請流程](https://www.google.com/search?q=CE+marking+AI+systems+EU+requirements)
