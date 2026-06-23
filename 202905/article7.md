# 持續評估管線設計

## 1. 為什麼需要持續評估

模型在生產環境中的表現會隨資料分布漂移而衰減。一次性評估不足以反映真實部署狀態，需要建立自動化持續評估管線。

## 2. 管線架構

持續評估管線包含：資料採集、及時評估、結果儲存與告警觸發四個核心環節。每個環節需設計容錯機制與監控指標。

```python
# 持續評估排程範例
import schedule
import time

eval_pipeline = EvaluationPipeline(
    model_endpoint="https://api.example.com/v1/chat",
    benchmark_tasks=["mmlu", "hellaswag"],
    alert_threshold={"mmlu": 0.05, "hellaswag": 0.03}
)

schedule.every(6).hours.do(eval_pipeline.run)
schedule.every().day.at("09:00").do(eval_pipeline.full_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 3. 回歸測試

每次模型更新應自動執行回歸測試套件，確保新版本未在已知任務上退化。回歸測試應包含核心能力基準與安全過濾器驗證。

## 4. 陰影評估

將新模型與生產模型的輸出同時記錄，進行離線比較評估。陰影評估不影響線上流量，可安全測試候選模型。

```python
class ShadowEval:
    def __init__(self, production, candidate):
        self.prod = production
        self.candidate = candidate
        self.results = []
    def evaluate(self, input_data):
        prod_out = self.prod(input_data)
        cand_out = self.candidate(input_data)
        self.results.append(compare(prod_out, cand_out))
```

## 5. 告警與儀表板

使用 Prometheus 儲存評估指標，Grafana 視覺化展示。設定分位數警報——如準確率低於過去的兩個標準差時自動通知。

## 6. 結語

持續評估管線是 AI 系統的監控系統。自動化、可觀測、可告警的評估架構能及早發現模型退化，保障生產環境的服務品質。

- https://www.google.com/search?q=LLM+continuous+evaluation+pipeline
- https://www.google.com/search?q=model+monitoring+drift+detection+AI
