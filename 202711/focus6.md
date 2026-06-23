# AI 治理與法規遵循

## 從歐盟 AI Act 到全球監管格局（2023-2026）

### 全球 AI 監管地圖

2023 年以來，各國政府和國際組織紛紛推出 AI 監管框架：

| 法規 | 地區 | 核心要求 | 生效時間 |
|------|------|----------|----------|
| EU AI Act | 歐盟 | 風險分級、透明度、人為監督 | 2025-2027 分階段實施 |
| China AI Law | 中國 | 演算法備案、內容審查、標示要求 | 2023（生成式 AI 辦法） |
| US Executive Order | 美國 | 安全測試、紅隊報告、標準制定 | 2023（行政命令） |
| Canada AIDA | 加拿大 | 影響評估、透明度報告 | 2025 起草中 |
| Japan AI Guidelines | 日本 | 軟性法規、行業自律 | 2024 |
| Brazil AI Bill | 巴西 | 消費者保護、問責機制 | 2025 審議中 |

### EU AI Act 的風險分級

歐盟 AI Act 是當前最具影響力的 AI 法規，將 AI 系統分為四級：

```
不可接受風險 (禁止)
  ├─ 社會評分系統
  ├─ 即時生物識別監控
  └─ 針對兒童的操控系統

高風險 (嚴格規範)
  ├─ 就業、教育、信用評估
  ├─ 關鍵基礎設施
  └─ 執法與司法

有限風險 (透明度義務)
  ├─ 聊天機器人（需告知使用者）
  └─ 深度偽造（需標示）

最低風險 (無規範)
  └─ 垃圾郵件過濾、遊戲 AI
```

### 企業合規實務

對於台灣的 AI 開發者，以下實務建議適用於多數法規：

```python
class AIComplianceChecklist:
    def __init__(self):
        self.checks = []
    
    def add_transparency(self):
        # 告知使用者正在與 AI 互動
        self.checks.append("告知義務：標示 AI 生成內容")
    
    def add_fairness(self):
        # 定期檢測模型是否有偏見
        self.checks.append("公平性：每季執行偏見審計")
    
    def add_right_to_explain(self):
        # 提供解釋機制
        self.checks.append("可解釋性：記錄決策依據")
    
    def add_data_protection(self):
        # GDPR / 個資法遵循
        self.checks.append("資料保護：資料最小化與刪除機制")
```

### AI 治理框架

良好的 AI 治理需要三個層次：

1. **治理委員會**：跨部門的 AI 倫理委員會，審查高風險 AI 專案
2. **技術控制**：模型卡、資料卡、系統卡
3. **持續監控**：生產環境中的模型行為監控和告警

### 模型卡範例

模型卡是 AI 治理的核心文件：

```yaml
model_name: example-chat-2026
version: 2.1.0
license: MIT
training_data:
  - source: 開源語料
  - size: 1.5T tokens
  - languages: zh, en
evaluation:
  - bias_test: passed
  - toxicity: 0.02%
  - accuracy: 89.5%
limitations:
  - 可能產生幻覺
  - 訓練資料截止於 2025-12
```

### 小結

AI 治理從 2023 年的自願性框架快速演進到 2026 年的強制性法規。企業需要在**創新速度**和**合規成本**之間取得平衡。關鍵建議：儘早建立 AI 治理架構，因為法規只會越來越嚴格。

---

**下一步**：[AI 安全工具與最佳實踐](focus7.md)

## 延伸閱讀

- [EU AI Act Overview](https://www.google.com/search?q=EU+AI+Act+overview+2025)
- [NIST AI Risk Management Framework](https://www.google.com/search?q=NIST+AI+risk+management+framework)
- [Taiwan AI Regulation](https://www.google.com/search?q=Taiwan+AI+regulation+2025)
