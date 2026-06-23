# 程式實作：AI 技術趨勢分析工具

## 簡介

本實作從零建構一個 AI 技術趨勢分析工具，展示如何收集、分析、可視化技術趨勢資料，並產生年度報告。完整程式碼在 `_code/trend_analyzer.py`。

## 核心元件

### 1. 趨勢資料模型

結構化儲存趨勢分析所需的資料：

```python
data = TrendDataPoint(
    keyword="multi-agent",
    month="2027-08",
    mentions=342,
    sentiment=0.75,
    source="simulated"
)
```

### 2. 成長率與情緒分析

計算各技術的成長軌跡：

```python
analyses = analyze_trends(data)
for a in analyses:
    print(f"{a.keyword}: {a.growth_rate:.2f}x, sentiment {a.avg_sentiment:+.2f}")
```

### 3. 熱門話題檢測

識別最近 3 個月成長顯著的技術：

```python
hot = find_hot_topics(data, threshold=1.5)
```

### 4. 報告自動生成

產生結構化的年度趨勢報告：

```python
report = generate_report(analyses, hot)
```

## 執行方式

```bash
cd _code
python3 trend_analyzer.py
```

## 延伸練習

1. **串接真實資料源**：從 arXiv、Twitter、GitHub API 獲取真實資料
2. **加入時間序列預測**：用 ARIMA 或 Prophet 預測下一年趨勢
3. **互動儀表板**：用 Plotly Dash 或 Streamlit 建立可視化儀表板
4. **情緒細化分析**：按地區、語言、領域分別分析技術情緒
