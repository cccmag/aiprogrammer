# 檢索式回覆選擇

## 問題定義

檢索式回覆選擇的目標是：給定對話歷史和一個候選回覆集合，選擇最合適的回覆。這個問題可以形式化為：

```
f(context, candidates) → best_response
```

## 經典檢索方法

### TF-IDF 向量化

TF-IDF（詞頻-逆文件頻率）將文本表示為稀疏向量。對於每一個詞 t 在文檔 d 中：

```
TF(t, d) = count(t, d) / |d|
IDF(t) = log(N / df(t))
TF-IDF(t, d) = TF(t, d) * IDF(t)
```

對話上下文和候選回覆都被轉換為 TF-IDF 向量，透過餘弦相似度計算匹配分數。

### BM25

BM25 是 TF-IDF 的改進版本，引入兩個重要調整：

1. **詞頻飽和**：一個詞在文檔中出現多次不會無限增加分數
2. **長度歸一化**：長文檔不會因其長度而獲得優勢

## 神經檢索方法

### Dual Encoder

Dual Encoder 使用兩個 BERT 編碼器分別編碼上下文和回覆：

```
h_context = BERT_encoder(context)
h_response = BERT_encoder(response)
score = cosine(h_context, h_response)
```

這種方法的優點是候選回覆的向量可以預先計算和索引，支援大規模檢索。

### Cross Encoder

Cross Encoder 將上下文和回覆拼接後輸入 BERT：

```
input = [CLS] context [SEP] response [SEP]
score = linear(BERT(input)[CLS])
```

雖然準確率更高，但 Cross Encoder 無法預先計算向量，檢索速度較慢。

## 兩階段架構

現代對話檢索系統通常採用兩階段架構：

1. **召回（Recall）**：使用 BM25 或 Dual Encoder 從數百萬候選中快速檢索 top-100
2. **排序（Re-rank）**：使用 Cross Encoder 對 top-100 進行精細排序

## 實務挑戰

檢索式系統在實際部署中面臨的主要挑戰包括：回覆庫的維護、新回覆的即時更新、長尾查詢的處理等。

## 延伸閱讀

- [Dual Encoder 對話匹配](https://www.google.com/search?q=dual+encoder+response+selection)
- [BERT 對話排序](https://www.google.com/search?q=BERT+response+selection+dialogue)
- [兩階段檢索排序系統](https://www.google.com/search?q=retrieval+ranking+dialogue+system)
