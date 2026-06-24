# 邊緣-雲端協同架構

## 三層協同模式

即時 AI 系統的延遲要求從毫秒到秒不等，單一架構無法滿足所有場景：邊緣端負責極低延遲的推論，雲端處理複雜模型和全域聚合。

## 邊緣推論代理

邊緣裝置運行輕量化的量化模型，處理即時請求：

```python
import onnxruntime as ort
import numpy as np

class EdgeInferenceAgent:
    def __init__(self, model_path, fallback_url):
        self.session = ort.InferenceSession(
            model_path,
            providers=['CoreMLExecutionProvider',
                       'CPUExecutionProvider']
        )
        self.fallback_url = fallback_url
        self.confidence_threshold = 0.85

    def predict(self, features):
        input_name = self.session.get_inputs()[0].name
        output = self.session.run(None, {
            input_name: features.astype(np.float32)
        })[0]

        confidence = float(np.max(output))

        if confidence >= self.confidence_threshold:
            return {'prediction': int(np.argmax(output)),
                    'confidence': confidence,
                    'source': 'edge'}
        else:
            return self.fallback_to_cloud(features)

    async def fallback_to_cloud(self, features):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.fallback_url,
                json={'features': features.tolist()}
            ) as resp:
                return await resp.json()
```

## 雲端模型服務

雲端執行完整精度模型，處理邊緣無法確定的案例：

```python
from fastapi import FastAPI
import torch

app = FastAPI()
model = load_full_precision_model()

@app.post("/inference/fallback")
async def cloud_inference(request: dict):
    features = torch.tensor(request['features'])
    with torch.no_grad():
        output = model(features)

    return {
        'prediction': output.argmax().item(),
        'confidence': output.softmax(dim=0).max().item(),
        'source': 'cloud',
    }
```

## 模型分發與更新

邊緣裝置需要定期同步模型更新：

```python
class ModelDistribution:
    def __init__(self, edge_clients, registry):
        self.clients = edge_clients
        self.registry = registry

    async def roll_out(self, version, fraction=0.1):
        # 金絲雀發布
        sample = random.sample(
            self.clients,
            int(len(self.clients) * fraction)
        )

        for client in sample:
            await client.update_model(version)

        # 監控回退機制
        alert = await self.monitor_rollback(sample)
        if alert:
            for client in sample:
                await client.rollback()
            return

        # 全面發布
        await self.update_all(version)
```

## 延遲預算分配

| 層級 | 延遲預算 | 模型大小 | 更新頻率 |
|------|---------|---------|---------|
| 邊緣裝置 | < 10 ms | < 100 MB | 每日 |
| 邊緣閘道 | < 50 ms | < 1 GB | 每小時 |
| 雲端 | < 500 ms | 完整模型 | 即時 |

## 頻寬節省策略

邊緣-雲端協同的關鍵瓶頸是網路頻寬：

- **特徵壓縮**：只傳送 embedding 而非原始資料
- **差異更新**：傳送參數 diff 而非完整權重
- **推論快取**：相似請求在邊緣端快取

## 延伸閱讀

- [邊緣運算架構設計](https://www.google.com/search?q=edge+cloud+collaborative+inference+architecture)
- [ONNX Runtime 邊緣部署](https://www.google.com/search?q=ONNX+Runtime+edge+deployment+tutorial)
- [模型金絲雀發布策略](https://www.google.com/search?q=canary+model+deployment+ML)
