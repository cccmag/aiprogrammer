# 模型監控指標與儀表板

## 從準確率到 P99 延遲（2021-2028）

### 前言

監控 AI 模型與監控傳統服務最大的不同在於：你需要同時監控**模型品質指標**和**系統效能指標**。一個模型可能準確率很高但延遲過高，或者準確率正常但信心度持續下降。

### 關鍵指標分類

**1. 業務指標（Business Metrics）**
- 預測轉換率、推薦點擊率、內容留存率
- 這些指標直接反映模型對業務的影響

**2. 模型品質指標（Model Quality）**
- 分類：準確率、精確率、召回率、F1、AUC-ROC
- 迴歸：MAE、RMSE、R²
- 生成式：BLEU、ROUGE、困惑度
- 當 ground truth 延遲到達時，需要代理指標（Proxy Metrics）

**3. 營運指標（Operational Metrics）**
- 延遲：P50/P95/P99 推論時間
- 輸送量：每秒請求數（RPS）
- 錯誤率：推論失敗、模型載入失敗、輸入驗證失敗
- 資源利用率：GPU 使用率、VRAM、推理引擎佇列長度

**4. 資料品質指標（Data Quality）**
- 新鮮度（Data Freshness）
- 完整性（Missing Value 比例）
- 一致性（Schema 是否符合預期）

### 儀表板設計原則

好的監控儀表板遵循「金字塔」結構：

```
┌─────────────────────────┐
│     SLA / 業務摘要      │  ← 高層一眼看懂
├─────────────────────────┤
│  模型品質趨勢（4h-7d）  │  ← 中期分析
├─────────────────────────┤
│  營運指標即時面板       │  ← 除錯入口
├─────────────────────────┤
│  個別請求追蹤查詢       │  ← 深層診斷
└─────────────────────────┘
```

### 延遲監控的陷阱

使用平均延遲是常見的錯誤。一個推論請求可能花 10 秒，其他 99 個請求花 100ms，平均值是 ~200ms，但第 99 個使用者體驗極差。**永遠監控 P95/P99 而非平均值**。

```python
import numpy as np

latencies = [0.1, 0.12, 0.09, 0.11, 10.0]
p99 = np.percentile(latencies, 99)
mean = np.mean(latencies)
print(f"Mean={mean:.2f}s, P99={p99:.2f}s")
```

### 儀表板工具演進

| 時期 | 工具 | 特點 |
|------|------|------|
| 2021 | Grafana + Prometheus | 基礎指標聚合 |
| 2023 | Grafana + ML Plugin | 增加模型指標 |
| 2025 | Evidently Dashboard | 專注資料漂移視覺化 |
| 2027 | 自訂 React 儀表板 | 內建因果分析 |

### SLO 與錯誤預算

將模型監控與服務等級目標（SLO）綁定：
- **SLO：99.9% 的推論請求 P95 < 500ms**
- **SLO：每日模型漂移檢測次數 < 3 次**
- 超出 SLO 即消耗錯誤預算，到達閾值後停止模型部署

### 小結

選擇正確的指標比建置華麗的儀表板更重要。從業務目標反推出模型指標，再從模型指標反推出營運指標——這就是可觀測性設計的「由外而內」原則。

---

**下一步**：[資料漂移與概念漂移檢測](focus3.md)

## 延伸閱讀

- [Grafana ML Dashboard](https://www.google.com/search?q=Grafana+ML+monitoring+dashboard)
- [Evidently AI Metrics](https://www.google.com/search?q=Evidently+AI+model+metrics)
- [SLO for ML Systems](https://www.google.com/search?q=SLO+for+machine+learning+systems)
