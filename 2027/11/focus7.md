# AI 安全工具與最佳實踐

## 從開源工具到企業級防護（2024-2026）

### 前言

AI 安全領域的工具生態在 2024-2026 年間快速成長。從 Google 的 Garak 到微軟的 Counterfit，從開源紅隊框架到商業級的安全閘道，開發者現在有豐富的工具可用。

### 工具概覽

| 工具 | 作者 | 用途 |
|------|------|------|
| Garak | NVIDIA | LLM 漏洞掃描 |
| Counterfit | Microsoft | AI 系統安全測試 |
| LLM Guard | Protect AI | 輸入輸出過濾 |
| Rebuff | Protect AI | 提示詞注入防護 |
| Guardrails AI | Guardrails AI | 結構化輸出驗證 |

### Garak：LLM 漏洞掃描

Garak 支援提示詞注入、越獄、資料提取、偏見等測試：

```python
from garak import probe

def scan_model(model: str):
    results = {}
    for p in probe.load_probes():
        p.probe(model)
        results[p.name] = p.success_rate
    return results
```

### Rebuff：提示詞注入防護

```python
from rebuff import Rebuff
rb = Rebuff(api_key="your-key")
result = rb.detect_injection("Ignore previous instructions...")
if result.injection_score > 0.5:
    print("偵測到注入嘗試")
```

### 最佳實踐

- **開發**：結構化輸出、輸入消毒、最小權限
- **測試**：紅隊測試、偏見審計、對抗性測試
- **營運**：即時監控、異常偵測、事故回應計畫

### 縱深防禦流程

```
輸入消毒 → 注入偵測 → 安全提示 + 結構化輸出 → PII 過濾 → 稽核日誌
```

### 小結

AI 安全工具從 2024 年的雛形階段發展到 2026 年的成熟生態。選擇工具時應考慮：覆蓋的攻擊面、整合難度、社群活躍度。沒有任何工具能提供 100% 的安全保障——**深度防禦 + 持續監控**才是唯一可靠的策略。

---

**下一步**：[回到本期焦點](focus.md)

## 延伸閱讀

- [Garak LLM Vulnerability Scanner](https://www.google.com/search?q=Garak+LLM+vulnerability+scanner+NVIDIA)
- [Rebuff Prompt Injection](https://www.google.com/search?q=Rebuff+prompt+injection+protection)
- [LLM Guard Protect AI](https://www.google.com/search?q=LLM+Guard+Protect+AI)
- [Microsoft Counterfit](https://www.google.com/search?q=Microsoft+Counterfit+AI+security)
