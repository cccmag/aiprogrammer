# 儀表板設計原則

## 前言

好的儀表板讓團隊在 10 秒內判斷系統健康狀態。本文從資訊層級、視覺選擇與互動設計探討 AI 監控儀表板的設計原則。

---

## 一、資訊層級

| 層級 | 內容 | 更新頻率 |
|------|------|---------|
| L1 摘要 | 健康分數、警報數 | 即時 |
| L2 趨勢 | 關鍵指標時間序列 | 每分鐘 |
| L3 細節 | 各模型個別表現 | 按需 |

---

## 二、核心 KPI 選擇

```python
class DashboardKPI:
    def __init__(self):
        self.kpis = {
            "overall_health": {"visualization": "gauge", "threshold": 0.8},
            "avg_latency_p99": {"visualization": "timeseries", "threshold": 1000},
            "drift_count": {"visualization": "stat", "threshold": 3},
            "prediction_volume": {"visualization": "timeseries"},
            "error_rate": {"visualization": "timeseries", "threshold": 0.01},
        }
```

---

## 三、視覺化選擇

| 資料類型 | 推薦圖表 | 用途 |
|---------|---------|------|
| 單一數值 | 儀錶圖 (Gauge) | 健康分數 |
| 時間序列 | 折線圖 (Line) | 延遲趨勢 |
| 分布 | 箱形圖 (Box) | 特徵漂移 |
| 比較 | 長條圖 (Bar) | 版本對比 |

---

## 四、互動設計

```python
class InteractiveDashboard:
    def __init__(self, data_source):
        self.data = data_source

    def drill_down(self, model_name, metric, time_range):
        details = self.data.query(f"model == '{model_name}'")
        correlations = self.data.find_correlated_features(metric, threshold=0.6)
        return {"detail_chart": details, "suggested_causes": correlations}
```

---

## 五、版面佈局原則

```
┌──────────────────────────────────┐
│  Header: 健康分數 [████░░] 0.82  │
├────────┬─────────────────────────┤
│ 側欄   │ 延遲 │ 準確率 │ QPS    │
│ 模型清單│ 漂移特徵列表            │
│ 時間範圍│ 最近警報                │
└────────┴─────────────────────────┘
```

1. 最重要的指標在上方
2. 從左到右閱讀
3. 色彩一致性（綠/黃/紅）
4. 避免滾動

---

## 六、快速原型：Streamlit

```python
import streamlit as st
st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)
col1.metric("健康分數", "0.87", delta="-0.03")
col2.metric("P99 延遲", "342ms", delta="+12ms")
col3.metric("錯誤率", "0.8%", delta="+0.2%")
```

---

## 結語

設計時不斷問：「這個圖表能讓我看見什麼新資訊？」如果答案是否定的，就移除它。

---

## 參考資料

- https://www.google.com/search?q=dashboard+design+principles+monitoring
- https://www.google.com/search?q=Grafana+ML+model+monitoring
- https://www.google.com/search?q=cognitive+load+dashboard+design
