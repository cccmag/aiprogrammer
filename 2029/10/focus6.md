# 全球 AI 監管比較

## EU AI Act、美國行政命令、中國管理辦法（2022-2029）

### 前言

2022 年之後，全球主要經濟體競相推出 AI 監管框架。歐盟走「風險分級」路線，美國偏「產業自願」，中國則強調「內容安全與社會穩定」。三條路徑反映了不同的社會價值觀與產業政策。

### 歐盟 AI Act：風險分級模式

EU AI Act 是全球第一部全面的 AI 法規，採用風險分級架構：

```python
from enum import Enum

class RiskCategory(Enum):
    UNACCEPTABLE = "不可接受風險"    # 禁止
    HIGH = "高風險"                  # 嚴格規範
    LIMITED = "有限風險"             # 透明度義務
    MINIMAL = "最小風險"             # 無規範

class EUAIActCompliance:
    """EU AI Act 合規檢查器（簡化版）"""
    
    RISK_RULES = {
        RiskCategory.UNACCEPTABLE: [
            '社會評分系統',
            '即時人臉辨識（公共空間）',
            '針對兒童的操縱性 AI',
        ],
        RiskCategory.HIGH: [
            '生物識別',
            '關鍵基礎設施',
            '教育與職業訓練',
            '就業與員工管理',
            '信用與保險評估',
            '執法與司法',
        ],
        RiskCategory.LIMITED: [
            '聊天機器人',
            '情緒辨識',
            '深偽技術',
        ],
        RiskCategory.MINIMAL: [
            '垃圾郵件過濾',
            '遊戲 AI',
            '庫存管理',
        ],
    }
    
    @classmethod
    def classify(cls, use_case: str) -> RiskCategory:
        """根據使用案例分類風險等級"""
        for category, examples in cls.RISK_RULES.items():
            if any(ex in use_case for ex in examples):
                return category
        return RiskCategory.MINIMAL
    
    @classmethod
    def requirements_for(cls, category: RiskCategory) -> list:
        """返回特定風險等級的要求清單"""
        base = ['風險管理系統', '資料治理', '技術文件']
        if category == RiskCategory.HIGH:
            return base + [
                '透明度報告',
                '人工監督',
                '準確性與強健性',
                '稽核軌跡',
            ]
        elif category == RiskCategory.LIMITED:
            return ['透明度揭露']
        return []

# 範例
use_cases = [
    "信用評分系統",
    "垃圾郵件過濾器",
    "即時人臉辨識監控",
    "庫存管理系統",
]

for case in use_cases:
    risk = EUAIActCompliance.classify(case)
    reqs = EUAIActCompliance.requirements_for(risk)
    print(f"{case}: {risk.value}")
    for r in reqs:
        print(f"  - {r}")
```

### 美國：去中心化的產業指引

美國採取較軟性的監管策略：

```python
class USAIBlueprint:
    """美國 AI 監管框架概述"""
    
    FRAMEWORKS = {
        'AI Bill of Rights (2023)': [
            '安全與有效的系統',
            '不受演算法歧視',
            '資料隱私保護',
            '通知與透明度',
            '人工替代選項',
        ],
        'NIST AI Risk Management Framework': [
            'Govern（治理）',
            'Map（映射）',
            'Measure（衡量）',
            'Manage（管理）',
        ],
        'Executive Order 14110 (2023)': [
            '新興 AI 安全測試',
            '隱私保護技術研究',
            '公平性與公民權利',
            '消費者與勞工保護',
            '國際合作',
        ],
    }
    
    @staticmethod
    def check_voluntary_compliance(company_size: str, sector: str) -> dict:
        """檢查自願遵循狀況"""
        compliance = {
            'has_AI_Bill_of_Rights_adherence': sector in ['healthcare', 'finance'],
            'follows_NIST_RMF': company_size == 'large',
            'EO_14110_applicable': company_size == 'large',
        }
        return compliance

# 美國模式的特色：無單一聯邦 AI 法，靠行政命令 + 自願指引
blueprint = USAIBlueprint()
print("US AI監管特色：")
for fw, principles in blueprint.FRAMEWORKS.items():
    print(f"\n{fw}:")
    for p in principles:
        print(f"  - {p}")
```

### 中國：內容安全與社會穩定

中國的 AI 監管強調控制與安全：

```python
class ChinaAIRegulation:
    """中國 AI 監管框架"""
    
    REGULATIONS = {
        '生成式 AI 管理辦法 (2023)': [
            '內容審核機制',
            '標籤義務（AI 生成內容標示）',
            '訓練資料合法性',
            '未成年人保護',
            '算法備案制度',
        ],
        '算法推薦管理規定 (2022)': [
            '算法備案',
            '用戶畫像標籤管理',
            '算法停止與刪除機制',
            '禁止差別待遇',
        ],
        '深度合成管理規定 (2023)': [
            '深度合成標示',
            '內容真實性審核',
            '技術安全評估',
        ],
    }
    
    @staticmethod
    def registration_required(tech_type: str) -> bool:
        """檢查是否需要算法備案"""
        return tech_type in ['推薦算法', '排序算法', '生成式 AI']
    
    @staticmethod
    def content_filter_rules() -> list:
        return [
            "禁止生成煽動顛覆國家政權的內容",
            "禁止傳播虛假信息",
            "禁止歧視性內容",
            "禁止侵犯他人知識產權",
        ]

print("=== 主要經濟體 AI 監管比較 ===\n")
print("| 面向 | EU AI Act | 美國框架 | 中國辦法 |")
print("|------|-----------|----------|----------|")
print("| 法律效力 | 強制性法規 | 自願指引+行政命令 | 強制性法規 |")
print("| 監管邏輯 | 風險分級 | 創新優先 | 安全優先 |")
print("| 高風險定義 | 明確列舉 | 行業自定義 | 國家安全相關 |")
print("| 罰則 | 營收 7% | 無統一罰則 | 吊銷許可+罰款 |")
print("| 透明度 | 強制揭露 | 自願揭露 | 算法備案 |")
```

### 監管趨同趨勢

| 年份 | 事件 |
|------|------|
| 2022 | 中國算法備案、美國 AI 問責法案提案 |
| 2023 | 歐盟 AI Act 草案通過、生成式 AI 監管浪潮 |
| 2024 | AI Act 正式批准 |
| 2025 | 各國監管上路、合規成本顯現 |
| 2027 | 跨國 AI 監管互認談判 |
| 2029 | 全球 AI 治理公約初步框架 |

### 小結

三條監管路徑反映了不同的治理哲學：歐盟以人權為中心，美國以創新為中心，中國以穩定為中心。2029 年，跨國 AI 系統將需要同時滿足多套監管要求，「合規工程」將成為 AI 開發的標準環節。

---

**下一步**：[負責任 AI 的未來](focus7.md)

## 延伸閱讀

- [EU AI Act 全文](https://www.google.com/search?q=EU+AI+Act+full+text)
- [NIST AI RMF](https://www.google.com/search?q=NIST+AI+Risk+Management+Framework)
- [中國生成式 AI 管理辦法](https://www.google.com/search?q=generative+AI+regulation+China)
- [全球 AI 監管比較](https://www.google.com/search?q=global+AI+regulation+comparison+2025)
