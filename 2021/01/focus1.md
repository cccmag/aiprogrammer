# 大型語言模型的崛起

## GPT-3 的背景與架構

### 從 GPT-1 到 GPT-3 的演化

OpenAI 的 GPT（Generative Pre-trained Transformer）系列代表了一種新的自然語言處理範式：

- **GPT-1（2018）**：1.1 億參數，首次展示預訓練+微調的有效性
- **GPT-2（2019）**：15 億參數， 因擔心被濫用而延後發布
- **GPT-3（2020）**：1750 億參數，Few-shot learning 的突破

```
GPT-1 → GPT-2 → GPT-3
1億   → 15億  → 1750億
```

### GPT-3 的技術架構

GPT-3 採用標準的 Decoder-only Transformer 架構，但進行了若干優化：

```python
# GPT-3 的關鍵參數
{
    "layers": 96,
    "dimensions": 12288,
    "heads": 96,
    "context_length": 2048,
    "parameters": "175B"
}
```

### 與其他大型模型的比較

| 模型 | 參數量 | 發布時間 | 機構 |
|------|--------|----------|------|
| GPT-3 | 175B | 2020/05 | OpenAI |
| Turing NLG | 17B | 2020/02 | Microsoft |
| GPT-2 | 1.5B | 2019/02 | OpenAI |
| BERT-Large | 340M | 2018/10 | Google |

### 訓練資料

GPT-3 的訓練資料來自多個來源：

- **Common Crawl**：4100 億詞元（60%）
- **WebText2**：190 億詞元（22%）
- **Books1**：120 億詞元（8%）
- **Books2**：550 億詞元（8%）
- **Wikipedia**：30 億詞元（3%）

### 為何選擇 Decoder-only？

GPT-3 採用 Decoder-only（也稱為「 CausallmLM」）架構，而非 Encoder-Decoder 或 Encoder-only：

1. **簡單性**：只需處理單向注意力
2. **生成能力**：更適合文字生成任務
3. **擴展性**：更容易擴展到更大規模

---

## 延伸閱讀

- [GPT-3 原始論文](https://www.google.com/search?q=GPT-3+paper+175B+parameters)
- [Transformer 架構解析](https://www.google.com/search?q=transformer+architecture+decoder+only)
- [大型語言模型訓練成本](https://www.google.com/search?q=training+cost+GPT-3+4.6M+ dollars)