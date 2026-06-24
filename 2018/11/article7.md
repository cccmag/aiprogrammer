# BERT 與 GPT 的比較

## 背景回顧

2018 年 NLP 領域最重要的兩個模型：
- **GPT**（6 月）：OpenAI 發表，單向 Transformer
- **BERT**（10 月）：Google 發表，雙向 Transformer

兩者都採用預訓練 + 微調範式，但在架構與訓練方式上有重要區別。

## 架構比較

### GPT：單向 Transformer Decoder
- 採用 Transformer 的 Decoder 部分
- 每個位置只能看到之前的 token（左側上下文）
- 適合生成任務

### BERT：雙向 Transformer Encoder
- 採用 Transformer 的 Encoder 部分
- 每個位置可以看到所有 token（雙側上下文）
- 適合理解任務

## 預訓練目標比較

| 模型 | 預訓練任務 | 優勢 | 劣勢 |
|------|-----------|------|------|
| GPT | 傳統語言模型（单向） | 強大的生成能力 | 不能利用右側上下文 |
| BERT | Masked LM + NSP | 雙向理解 | 生成能力受限 |

## 注意力遮罩

### GPT 的因果遮罩
確保生成時只看見之前的 token：
```
[CLS] A B C [MASK] E
         ↓
只看見 A B C，預測 [MASK]
```

### BERT 的雙向注意力
沒有遮罩，所有位置都可以互相注意：
```
[CLS] A B C D E
    ↓
同時看見所有位置
```

## 適用場景

### BERT 擅長
- 文字分類
- 命名實體識別
- 問答系統
- 自然語言推理

### GPT 擅長
- 文字生成
- 對話系統
- 文本補全
- 創意寫作

## 效能比較

在 GLUE 基準測試上：
- BERT-base：78.7%
- GPT：72.5%
- BERT-large：80.5%

BERT 在理解任務上通常領先。

## 為何 BERT 在理解任務上更強？

雙向表示讓 BERT 能夠：
1. 同時利用左右上下文
2. 更好地理解句子級語義
3. 準確捕捉任務相關特徵

## 融合的可能性

研究者嘗試結合兩者：
- **GPT-2**：更大規模的 GPT，加強生成能力
- **XLNet**：排列語言模型，結合雙向與生成能力

## 實務選擇

選擇建議：
- **理解任務**：首選 BERT 或其變體
- **生成任務**：選擇 GPT 或語言模型
- **兩者都需要**：考虑 Encoder-Decoder 架構（如 T5）

## 參考資源

- https://www.google.com/search?q=BERT+vs+GPT+比較+單向+雙向+預訓練+任務+区别
- https://www.google.com/search?q=BERT+双向+Transformer+GPT+单向+Decoder+選擇+使用
- https://www.google.com/search?q=BERT+GPT+GLUE+benchmark+performance+comparison+2018