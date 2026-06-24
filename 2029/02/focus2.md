# LLM 驅動的文字資料生成（2022-2029）

## Prompt Engineering 到 Self-Instruct

LLM 的文字合成能力從 2022 年 ChatGPT 問世後快速演進。早期依賴人工編寫 Prompt，後來到 Self-Instruct 方法讓 LLM 自主產生訓練資料，再到 2025 年後的完全自主合成管線。

### Self-Instruct 與指令合成

2022 年 Stanford 的 Self-Instruct 論文開創了「用 LLM 訓練 LLM」的典範。方法分三步：種子指令生成、任務識別、實例生成。後續 Alpaca、Vicuna 等開源模型完全靠合成資料微調。

```python
# 合成文字分類資料範例
from _code.synthetic_data import SyntheticDataGenerator, SyntheticRecord

gen = SyntheticDataGenerator()
def classify_synthetic(text: str) -> str:
    labels = {"algorithm": "技術", "system": "技術", "essential": "評論", "standard": "評論"}
    for key, label in labels.items():
        if key in text.lower():
            return label
    return "其他"

for r in gen.generate_text(5):
    label = classify_synthetic(r.text)
    print(f"{label}: {r.text}")
```

### LLM 合成對話資料

2023-2025 年間，基於 LLM 的對話合成成為客服、教育等領域的核心方法。Back-Translation、Self-Consistency、Chain-of-Thought 等技術大幅提升合成對話的自然度。

### 2026-2029：合成資料工廠

2026 年後出現「合成資料工廠」（Synthetic Data Factory）架構：多個 LLM 協同工作，分別負責生成、審核、過濾、標註。單一管線每天可合成百萬級高品質文字樣本。

### 領域特化合成

2025 年後合成資料從通用走向領域特化。醫療領域：GPT-4 合成病歷與醫囑，保留醫療術語與診斷邏輯。法律領域：合成合約條款與判例分析，模擬不同法系的論證結構。金融領域：合成交易記錄與風險報告，涵蓋罕見的金融事件場景。

### 品質控制挑戰

合成文字常見問題包括：重複模式、事實幻覺、語意偏差。解決方案包括多模型投票驗證、Retrieval-Augmented Generation（RAG）校驗、以及人類反饋（RLHF）過濾。2027 年後 LLM-as-Judge 方法成為品質控制的主流——用一個 LLM 評估另一個 LLM 的生成品質。

## 延伸閱讀

- [Self-Instruct 2022](https://www.google.com/search?q=Self-Instruct+LLM+synthetic+data+Stanford+2022)
- [Synthetic data factory LLM 2026](https://www.google.com/search?q=synthetic+data+factory+LLM+generation+pipeline)
- [LLM synthetic text quality control](https://www.google.com/search?q=LLM+synthetic+text+quality+hallucination+control)
