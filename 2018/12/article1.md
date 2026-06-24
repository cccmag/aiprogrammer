# GPT 與語言模型

## GPT 發表背景

2018 年 6 月，OpenAI 發表「Improving Language Understanding by Generative Pre-Training」論文，提出 GPT 模型。這是首個成功的大型 Transformer 預訓練語言模型。

## 核心架構

GPT 使用單向 Transformer Decoder：
- 12 層 Transformer
- 768 隱藏維度
- 12 注意力頭
- 約 1.1 億參數

## 預訓練目標

GPT 採用傳統的語言模型目標：
```
L = - Σ log P(w_i | w_1, ..., w_{i-1})
```

這是從左到右的单向預測，只能利用左側上下文。

## 無監督預訓練

GPT 在大規模語料上進行預訓練：
- BooksCorpus：包含超過 7,000 本書籍
- 書籍文本適合學習長距離依賴
- 文本未標注，可以大規模收集

## 監督式微調

預訓練完成後，在特定任務上微調：
```
L_task = - Σ log P(label | features)
```

微調時加入任務特定輸出層，整個網路共同訓練。

## 實驗結果

GPT 在多項任務上取得领先成绩：
- 文字蘊含：82.1% 準確率
- 問答：87.4% 準確率
- 常識推理：63% 準確率
- 語義相似度：78% 準確率

## GPT 的貢獻

1. 驗證了大型預訓練模型的有效性
2. 展示了 Transformer 在語言模型上的優異表現
3. 開啟了大模型時代

## GPT 與 BERT 的比較

| 特性 | GPT | BERT |
|------|-----|------|
| 架構 | 單向 Transformer | 雙向 Transformer |
| 預訓練 | 語言模型 | MLM + NSP |
| 優勢 | 生成能力強 | 理解能力強 |
| 發表時間 | 6 月 | 10 月 |

## 參考資源

- https://www.google.com/search?q=GPT+OpenAI+預訓練語言模型+2018+原理+詳解
- https://www.google.com/search?q=GPT+BERT+比較+單向+雙向+預訓練+区别
- https://www.google.com/search?q=generative+pre-training+GPT+language+model+paper+OpenAI+2018