# WhyLabs / Arize AI 可觀測性平台

## 前言

WhyLabs 與 Arize AI 是兩大 AI 可觀測性平台。兩者皆提供模型監控與漂移檢測，但在設計哲學上有所不同。本文比較兩者功能，並以 WhyLabs 為例展示實作。

---

## 一、WhyLabs 平台

WhyLabs 以 **whylogs** 開源函式庫為核心，能在不儲存原始資料的前提下產生統計摘要（profiles），兼顧隱私與可觀測性。

### 1.1 安裝與設定

```bash
pip install whylogs whylabs-client
```

### 1.2 記錄推論資料

```python
import whylogs as why
from whylogs.api.writer.whylabs import WhyLabsWriter

writer = WhyLabsWriter(
    org_id="my-org",
    dataset_id="model-prod",
    api_key="YOUR_API_KEY"
)

with why.logger(mode="rolling", interval_sec=60) as logger:
    for batch in production_stream:
        logger.log(batch)
        profile = logger.profile()
        writer.write(profile)
```

whylogs 會自動計算每個特徵的 min/max/mean/stddev/分位數以及缺失值比例。

---

## 二、Arize AI 平台

Arize AI 強調 **端到端可觀測性**，從資料管線到模型推論一網打盡。其核心特色是 **Embedding 視覺化** 與 **切片分析（Slicing）**。

```python
import arize

from arize.api import Client
from arize.utils.types import ModelTypes

arize_client = Client(
    space_key="YOUR_SPACE_KEY",
    api_key="YOUR_API_KEY"
)

arize_client.log_prediction(
    model_id="fraud-detector",
    model_version="v2.3",
    prediction_id="pred_12345",
    features={"amount": 2500.0, "location": "TW"},
    prediction=0.1,
    actual=1.0,
    tags={"experiment": "threshold-v2"}
)
```

Arize 的 Embedding 視覺化工具可以將 LLM 的向量表示投影到 2D 空間，直觀觀察語意漂移。

---

## 三、功能比較

| 功能 | WhyLabs | Arize AI |
|------|---------|----------|
| 開源核心 | whylogs（Apache 2.0） | 無（專有 SDK） |
| 資料保留 | 統計摘要，無原始資料 | 可選擇保留原始資料 |
| Embedding 監控 | 基礎支援 | 完整視覺化與切片 |
| LLM 支援 | 逐步擴充 | Traces + Spans |
| 部署模式 | SaaS / 自託管 | SaaS / 自託管 |
| 價格模型 | 基於 profile 數量 | 基於預測事件數量 |

---

## 四、根因分析實例

當模型準確率突然下降時，WhyLabs 會自動進行根因分析：

```python
from whylabs.tools.root_cause import analyze_drift

result = analyze_drift(
    reference_profile=ref,
    target_profile=target,
    target_metric="accuracy",
    granularity="feature"
)

for feature, score in result.feature_importance():
    if score > 0.1:
        print(f"Feature {feature} contributes {score:.1%} to drift")
```

這能幫助團隊快速定位是哪個特徵的分布變化導致了模型衰退。

---

## 五、選擇建議

- **重視隱私與開源生態** → WhyLabs + whylogs
- **需要 Embedding 深度分析** → Arize AI
- **LLM 應用監控** → Arize（Tracing 較成熟）
- **預算有限** → WhyLabs（profile-based 計費較可控）

---

## 結語

WhyLabs 與 Arize AI 代表了 AI 可觀測性的兩條路線：輕量統計摘要 vs 完整資料保留。選擇時應根據資料敏感性、監控深度與預算綜合考量。

---

## 參考資料

- https://www.google.com/search?q=WhyLabs+whylogs+model+monitoring
- https://www.google.com/search?q=Arize+AI+observability+platform
