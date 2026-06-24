# 對話狀態追蹤 DST

## 核心任務

對話狀態追蹤（Dialog State Tracking, DST）是任務型對話系統的核心組件。DST 的任務是在每一輪對話結束後，根據對話歷史更新當前的對話狀態。

## 對話狀態表示

對話狀態通常包含：

```
{
  "active_intent": "book_restaurant",
  "slots": {
    "party_size": {"value": "2", "confidence": 1.0},
    "date": {"value": "today", "confidence": 0.9},
    "time": {"value": "19:00", "confidence": 0.8}
  }
}
```

## DST 方法演進

### 基於規則的 DST

最簡單的方法使用狀態機和手寫規則。例如，當使用者提到「人數」時，觸發填寫 party_size 槽位。

### 生成式 DST

2015 年後，基於 RNN 的生成式模型成為主流。模型的輸出是每個槽位的值分佈：

```
P(slot=value | dialogue_history)
```

### BERT 時代的 DST

2019 年後，BERT 成為 DST 的基礎架構。TRADE（Transferable Dialogue State Generator）模型使用 Copy Mechanism 從對話歷史中複製槽位值。

### 開放詞彙 DST

傳統 DST 需要預先定義所有可能的槽位值，這限制了系統的可擴展性。開放詞彙（Open-Vocabulary）DST 如 SOM-DST 可以處理訓練時未見過的槽位值。

## DST 挑戰

### 對話歷史依賴

使用者可能在第五輪才提供第一輪問題的答案，模型需要正確地回填槽位。

### 值共指

使用者可能在對話中用代詞指代之前提到的值，模型需要解決共指問題。

### 不確定性管理

使用者的表述可能模糊不清，模型需要維護多種可能的狀態假設。

## DST 評估

DST 的標準評估指標是 Joint Goal Accuracy（JGA）：

```
JGA = 1/N * Σ I(pred_slots == true_slots)
```

只有所有槽位的預測都完全正確時，這一輪才計為正確。

## 延伸閱讀

- [DSTC 挑戰賽](https://www.google.com/search?q=Dialog+State+Tracking+Challenge+DSTC)
- [TRADE 模型](https://www.google.com/search?q=TRADE+dialog+state+tracking)
- [SOM-DST 開放詞彙](https://www.google.com/search?q=SOM-DST+open+vocabulary+dialog+state+tracking)
