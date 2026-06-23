# 紅隊自動化工具：Garak 與 PyRIT

## 1. 引言

AI 紅隊測試是系統性尋找 LLM 系統漏洞的過程。手動紅隊耗時且不全面，因此自動化工具成為主流。目前最受關注的兩套工具是微軟的 PyRIT（Python Risk Identification Toolkit）和 Garak，各有不同的設計哲學。

## 2. Garak：模型安全探測框架

Garak 由 Leon Derczynski 開發，專注於探測 LLM 的潛在弱點。其設計核心理念是「探測探測再探測」——針對模型的每一個安全面向進行系統性測試。

### Garak 的主要模組

```
garak/
├── probes/           # 探測器：測試特定弱點
│   ├── encoding.py   # 編碼繞過測試
│   ├── injection.py  # 提示詞注入測試
│   ├── jailbreak.py  # 越獄測試
│   └── toxicity.py   # 有毒內容測試
├── detectors/        # 檢測器：判斷回應是否違規
├── generators/       # 產生器：連接不同模型後端
└── harness/          # 測試流程控制
```

### 使用範例

```python
# garak 掃描測試
import garak
from garak.harness import Harness
from garak.probes import encoding, injection

h = Harness()
h.add_probe(injection.Probe())
h.add_probe(encoding.Probe())
h.configure(model="openai/gpt-4")

results = h.run()
print(results.summary())
```

## 3. PyRIT：微軟的紅隊框架

PyRIT 是 Microsoft AI Red Team 開發的工具，注重操作的結構化和可重複性。與 Garak 的探測模式不同，PyRIT 更像一個完整的攻擊框架。

### PyRIT 的核心概念

```python
from pyrit.orchestrator import RedTeamingOrchestrator
from pyrit.prompt_target import AzureMLChatTarget
from pyrit.chat_message_normalizer import GenericSystemSquash

target = AzureMLChatTarget(
    endpoint="https://my-model.openai.azure.com/",
    api_key="..."
)

orchestrator = RedTeamingOrchestrator(
    prompt_target=target,
    adversarial_chat=RedTeamingBot(
        objective="取得系統提示內容",
        conversation_objective="誘導模型洩漏 system prompt"
    )
)

result = orchestrator.run()
print(f"攻擊成功: {result.success}")
print(f"繞過次數: {result.attempts}")
```

### 支援的攻擊類別

| 攻擊類型 | Garak | PyRIT |
|---------|-------|-------|
| 提示詞注入 | ✓ | ✓ |
| 越獄 | ✓ | ✓ |
| 編碼繞過 | ✓ | ✓ |
| 多輪攻擊 | 有限 | ✓ |
| 紅隊聊天機器人 | ✗ | ✓ |
| 自動目標調整 | ✗ | ✓ |

## 4. 如何選擇？

Garak 適合快速掃描和 CI/CD 整合——它可以在幾分鐘內對一個模型執行數百種測試。PyRIT 則適合深入的紅隊演練——它的 RedTeamingOrchestrator 能夠模擬真實攻擊者的行為模式。

## 5. 結語

Garak 和 PyRIT 代表了兩種互補的紅隊自動化策略：廣泛掃描與深度攻擊。實際使用中建議兩者並用——Garak 作為定期安全掃描，PyRIT 用於深入的安全評估。紅隊測試不是一次性活動，而應融入 AI 系統的開發生命週期。

---

## 延伸閱讀

- [Garak GitHub 倉庫](https://www.google.com/search?q=Garak+LLM+security+scanning)
- [PyRIT 微軟紅隊工具](https://www.google.com/search?q=Microsoft+PyRIT+red+teaming)
- [AI 紅隊測試最佳實踐](https://www.google.com/search?q=AI+red+teaming+best+practices)
