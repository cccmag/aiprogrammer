# 自監督學習與對比學習

## 為何需要自監督學習？

標籤資料的獲取成本高昂。自監督學習通過設計代理任務，讓模型從未標注資料中學習表示。

## 對比學習原理

對比學習的核心是讓相似樣本在表示空間中接近，不相似樣本遠離：

```python
def contrastive_loss(query, positive, negatives, temperature=0.5):
    query = l2_normalize(query)
    positive = l2_normalize(positive)
    negatives = l2_normalize(negatives)

    pos_sim = dot(query, positive) / temperature
    neg_sim = dot(query, negatives) / temperature

    logits = concat([pos_sim, neg_sim])
    labels = zeros(len(logits))
    return cross_entropy(logits, labels)
```

## 2021 年的重要進展

### SimCLR v2

Google 發布 SimCLR v2，結合更大的模型和蒸餾技術，進一步提升效能。

### BYOL 和 Barlow Twins

這些方法不需要負樣本，簡化了訓練過程。

### MAE（Masked Autoencoder）

何愷明等提出的 MAE 採用類似 BERT 的遮罩策略，極大提升了影象表示學習的效率。

## 應用場景

- 醫學影像表示學習
- 自然語言處理的預訓練
- 語音處理

## 結論

自監督學習減少了對標註資料的依賴，是 AI 走向通用智慧的重要步驟。