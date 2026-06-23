# AI 安全評估基準：從 HELM 到 SafetyBench

## 1. 引言

AI 安全不能只是定性討論——需要可量化、可比較的評估基準。過去三年間，學術界和工業界開發了多套評估框架，從 HELM 的全方位基準到 SafetyBench 的專注安全評估，為模型安全提供了標準化度量。

## 2. HELM（Holistic Evaluation of Language Models）

史丹佛大學 CRFM 提出的 HELM 是第一個系統性評估 LLM 的框架，涵蓋準確性、校準、穩健性、公平性、偏見、毒性與效率等 7 個維度。其安全場景包含提示詞注入、有害內容和諂媚行為（sycophancy）測試。```

### HELM 的限制

HELM 的全面性也是其弱點——測試成本極高（評估一個模型需要數萬美元）。此外，HELM 的安全評估偏向已知攻擊模式，對新攻擊的覆蓋不足。

## 3. SafetyBench

SafetyBench 由 Tsinghua 團隊開發，專注於 LLM 安全評估，是目前規模最大的中文安全基準。

### 評估維度

```
SafetyBench
├── 自我認知（Self-Cognition）
├── 道德倫理（Morality & Ethics）
├── 法律法規（Legal Compliance）
├── 隱私安全（Privacy Security）
├── 有害內容（Harmful Content）
├── 拒絕服務（Refusal to Serve）
├── 偏見歧視（Bias & Discrimination）
└── 經濟安全（Economic Security）
```

### 評估方式

每題包含問題、安全答案與不安全答案，計算模型回答的安全率：

```python
def evaluate_safety(model, dataset):
    total, safe = 0, 0
    for item in dataset:
        response = model.generate(item["question"])
        if response == item["safe_answer"]:
            safe += 1
        total += 1
    return safe / total
```

## 4. 其他重要基準

### Anthropic 安全基準（ASB）

Anthropic 發布的安全基準專注於「多重危害」評估——測試模型在複雜多輪對話中是否保持安全。相比單輪測試，多輪評估更接近真實使用場景。

### DecodingTrust（DecTrust）

由芝加哥大學團隊提出，關注模型在解碼階段的偏見和安全性。揭露了即使模型訓練良好，解碼策略的選擇也會顯著影響輸出安全。

## 5. 評估框架比較

| 基準 | 發布年份 | 維度數 | 語言支援 | 開源 |
|------|---------|--------|---------|------|
| HELM | 2022 | 7 | 英文 | ✓ |
| SafetyBench | 2023 | 8 | 中/英 | ✓ |
| Anthropic ASB | 2024 | 11 | 英文 | ✗ |
| DecTrust | 2024 | 6 | 英文 | ✓ |

## 6. 結語

從 HELM 的全方位評估到 SafetyBench 的專注安全，AI 安全基準正在快速進化。目前的瓶頸在於靜態基準無法捕捉動態攻擊——攻擊者會針對基準的弱點設計規避策略。下一代安全基準需要包含對抗性測試和自適應攻擊場景。

---

## 延伸閱讀

- [HELM 評估框架](https://www.google.com/search?q=HELM+Stanford+CRFM+evaluation)
- [SafetyBench 論文](https://www.google.com/search?q=SafetyBench+LLM+safety+evaluation)
- [DecodingTrust 評估](https://www.google.com/search?q=DecodingTrust+LLM+trustworthiness)
