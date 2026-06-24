# 程式實作：年度回顧報告產生器

## 簡介

本實作產生 2029 年度 AI 技術回顧報告，整合四年里程碑數據和趨勢分析。完整程式碼在 `_code/annual_report_2029.py`。

## 核心元件

### 1. 年度摘要資料

```python
YEARLY_DATA = [
    YearSummary(2026, ["GPT-5", "AutoGen 1.0"], {"market_b": 200}),
    YearSummary(2027, ["Multi-agent boom"], {"market_b": 500}),
    YearSummary(2028, ["Agent economy"], {"market_b": 1000}),
    YearSummary(2029, ["Agent economy $100B"], {"market_b": 2000}),
]
```

### 2. 趨勢計算

```python
calculator = TrendCalculator()
growth = calculator.calculate_growth(YEARLY_DATA, "market_b")
```

### 3. 亮點提取

```python
extractor = HighlightExtractor()
highlights = extractor.extract_milestones(YEARLY_DATA)
```

### 4. 報告生成

```python
report = ReportGenerator()
report.generate(YEARLY_DATA, "annual_report_2029.md")
```

## 執行方式

```bash
cd _code
python3 annual_report_2029.py
```

## 延伸練習

1. **加入更多指標**：開源貢獻數、論文發表數
2. **視覺化圖表**：用 matplotlib 繪製趨勢線
3. **預測 2030**：基於歷史數據預測來年
4. **自訂主題**：針對特定領域分析（如 Agent、安全）
5. **比較分析**：與前四年的預測進行比對
