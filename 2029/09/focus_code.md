# 程式實作：科學分析工具包

## 簡介

本實作建構一個科學文獻分析工具，支援論文檢索、摘要提取和趨勢分析。完整程式碼在 `_code/sci_analyzer.py`。

## 核心元件

### 1. 論文檢索

```python
retriever = PaperRetriever()
papers = retriever.search("quantum machine learning")
```

### 2. 摘要提取

```python
extractor = AbstractExtractor()
summary = extractor.extract_key_sentences(paper.abstract, top_k=3)
```

### 3. 趨勢分析

```python
analyzer = TrendAnalyzer()
trends = analyzer.detect_trends(all_papers, "quantum")
```

### 4. 生成報告

```python
report = analyzer.generate_report(papers, trends)
```

## 執行方式

```bash
cd _code
python3 sci_analyzer.py
```

## 延伸練習

1. **串接真實 API**：用 Semantic Scholar API 檢索論文
2. **圖譜構建**：建立論文引用網路
3. **文字生成摘要**：用 LLM 生成摘要
4. **時間序列分析**：追蹤關鍵詞熱度變化
5. **可視化儀表板**：互動式科學趨勢展示
