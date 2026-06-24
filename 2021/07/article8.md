# GPT-3 與 Few-shot Learning

GPT-3 展示了大型語言模型的驚人能力。本文介紹其核心特性。

## 1. GPT-3 簡介

GPT-3 有 1750 億參數，是 2020 年最大的語言模型。其核心突破是強大的 Few-shot Learning 能力。

## 2. Few-shot Learning

傳統機器學習需要大量標註資料。Few-shot Learning 只需少量範例：

```python
prompt = """翻譯為英文：

範例：
中文：我愛機器學習
英文：I love machine learning

範例：
中文：今天天氣很好
英文：
"""
```

## 3. Prompt Engineering

設計有效的 prompt 是使用 GPT-3 的關鍵：
- 清晰的任務描述
-適量的範例
- 明確的輸出格式

## 4. 限制

- 幻覺問題
- 計算成本高
- 可能包含偏見

## 5. 結論

GPT-3 開啟了大型語言模型的新時代，Few-shot Learning 改變了我們對 AI 的期待。

---

## 延伸閱讀

- [GPT-3 論文](https://www.google.com/search?q=GPT-3+language+models+are+few-shot+learners+paper)
- [OpenAI API 文檔](https://www.google.com/search?q=OpenAI+GPT-3+API+documentation)