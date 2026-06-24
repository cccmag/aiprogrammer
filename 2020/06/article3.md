# GPT-3 vs BERT 比較

## 架構差異

| 特性 | GPT-3 | BERT |
|------|-------|------|
| 架構 | Transformer 解碼器 | Transformer 編碼器 |
| 注意力 | 單向（只看前文） | 雙向（看全文） |
| 訓練目標 | 下一個 token 預測 | 掩碼語言模型 + NSP |
| 參數量 | 1750 億 | 3.4 億（base）/ 11 億（large）|

## 訓練目標差異

```python
# GPT-3 訓練：預測下一個 token
# 輸入：[A, B, C] → 預測 D

# BERT 訓練：預測被遮蓋的 token
# 輸入：[A, B, [MASK], D] → 預測 C
```

## 任務適配方式

### GPT-3：透過 Prompt

```python
prompt = """Classify the sentiment:
Text: This movie is great!
Sentiment: positive

Text: Terrible experience.
Sentiment: negative

Text: It's okay.
Sentiment:"""

# 不需要微調，直接預測
```

### BERT：需要微調

```python
from transformers import BertForSequenceClassification

model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
# 需要標註資料進行微調
```

## 各任務表現

| 任務類型 | GPT-3 優勢 | BERT 優勢 |
|---------|-----------|-----------|
| 生成任務 | ✓✓✓ 強大 | ✗ 不適合 |
| 分類任務 | ✓ 尚可 | ✓✓✓ 強大 |
| 問答任務 | ✓✓ 良好 | ✓✓ 良好 |
| 翻譯 | ✓✓ 良好 | ✗ 需特別訓練 |
| 文字相似度 | ✓ 尚可 | ✓✓✓ 強大 |

## 資源需求

```python
# BERT：可在單個 GPU 上運行
# GPT-3：需要透過 API 訪問

# 記憶體需求
bert_base = "340MB"      # 權重大小
gpt3_api = "無本地需求"    # 透過 API
```

## 生成 vs 理解

GPT-3 專精於生成流暢的文字，特別適合需要創造性輸出的任務。

BERT 專精於理解文字的語義，特別適合分類、序列標注等理解任務。

## 實際選擇建議

| 場景 | 推薦 |
|------|------|
| 文字分類 | BERT |
| 文字生成 | GPT-3 |
| 問答系統 | 兩者皆可 |
| 情感分析 | BERT |
| 創意寫作 | GPT-3 |
| 翻譯 | GPT-3 |

## 混合使用

有時可以結合兩者的優勢：

```python
# 使用 BERT 進行分類
importance_score = bert_classifier(text)

# 使用 GPT-3 根據分類結果生成
response = openai.Completion.create(
    prompt=f"Write about {topic} with {tone} tone"
)
```

## 參考資源

- https://www.google.com/search?q=GPT-3+vs+ BERT+comparison+language+model+architecture+differences+2020
- https://www.google.com/search?q=BERT+GPT-3+when+to+use+which+task+performance+comparison
- https://www.google.com/search?q=GPT-3+BERT+fine-tuning+vs+few-shot+approach+comparison