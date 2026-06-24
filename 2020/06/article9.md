# 從 BERT 到 GPT-3 的演進

## 時間線

| 年份 | 模型 | 參數量 | 重要創新 |
|------|------|--------|---------|
| 2017 | Transformer | N/A | 注意力機制 |
| 2018 | GPT-1 | 1.1 億 | 預訓練 + 微調 |
| 2018 | BERT | 3.4 億 | 雙向注意力 |
| 2019 | GPT-2 | 15 億 | 完全開放 |
| 2020 | T5 | 110 億 | Text-to-Text 統一框架 |
| 2020 | GPT-3 | 1750 億 | Few-shot Learning |

## 架構演進

### 從 GPT-1 到 GPT-2

- 規模擴大 10 倍以上
- 訓練資料從 BookCorpus 到 WebText
- 單向注意力的改進

### 從 GPT-2 到 GPT-3

- 規模擴大 117 倍
- 情境學習能力湧現
- Sparse Transformer 元素

## 訓練目標演進

```python
# GPT-1/2: Next token prediction
# 輸入: [A, B, C] → 預測: D

# BERT: Masked Language Model
# 輸入: [A, B, [MASK], D] → 預測: C

# T5: Span corruption
# 輸入: [A, B, [MASK], D, E] → 預測: [C, start]
```

## 遷移學習範式演進

| 階段 | 方法 | 特點 |
|------|------|------|
| 早期 | 從頭訓練 | 需要大量資料 |
| 2018-2019 | 預訓練 + 微調 | BERT 系列 |
| 2020+ | In-context Learning | GPT-3 |

## 預訓練任務比較

BERT 的創新：掩碼語言模型（MLM）+ 下一句預測（NSP）
GPT 系列：下一個 token 預測

兩種方法各有優勢，催生了不同的應用場景。

## 規模與能力關係

研究顯示，隨著規模增加：
1. 語言建模能力平滑提升
2. 湧現能力在特定規模閾值突然出現
3. Few-shot 能力顯著增強

## 未來方向

- 更大的模型（GPT-4傳聞）
- 多模態整合
- 更高效的架構
- 結合符號 AI

## 參考資源

- https://www.google.com/search?q=BERT+GPT+evolution+timeline+transformer+language+model+history+2018-2020
- https://www.google.com/search?q=pretrained+language+model+development+ELMo+BERT+GPT+T5+comparison
- https://www.google.com/search?q=GPT-3+emergence+in-context+learning+scale+breakthrough+analysis