# 任務型對話與狀態追蹤

## 什麼是任務型對話

任務型對話系統旨在幫助使用者完成特定任務，如訂餐、預約掛號、查詢航班。與開放域聊天不同，任務型對話有明確的目標和結構化的對話流程。

## 對話狀態定義

對話狀態（Dialog State）是任務型對話系統的核心資料結構，它記錄了對話過程中提取的所有關鍵資訊。狀態通常表示為一組槽位（Slots）：

```
{
  "intent": "book_flight",
  "slots": {
    "departure": "台北",
    "destination": "東京",
    "date": "2022-12-01",
    "passengers": 2
  }
}
```

## Slot Filling 技術

Slot Filling（槽位填充）是從使用者輸入中提取特定資訊的過程。主要方法包括：

- **基於規則**：使用正則表達式或 CRF 抽取實體
- **基於序列標註**：使用 BiLSTM-CRF 或 BERT 進行命名實體識別
- **基於機器閱讀理解**：將槽位作為問題，從對話中尋找答案

## 信念狀態追蹤

信念狀態（Belief State）追蹤是對話狀態追蹤（DST）的核心任務。它維護一個關於使用者意圖的機率分佈，而非單一的確定性狀態：

```
P(intent="book_flight" | history) = 0.95
P(intent="check_status" | history) = 0.05
```

### DST 方法演進

- **2015-2017**：基於 RNN 的生成式 DST
- **2018-2020**：基於 BERT 的跨注意力 DST
- **2021-2022**：基於預訓練語言模型的一站式 DST

## 對話策略學習

對話策略（Dialog Policy）決定系統下一步的操作。策略可以是基於規則的狀態機，也可以是透過強化學習訓練的策略網路。

## 實例：餐廳預約系統

```
使用者：我想訂明天晚上的餐廳
系統：請問幾位用餐？
使用者：兩位，晚上七點
系統：好的，預約明天晚上七點兩位，請問您的姓名？
```

## 延伸閱讀

- [對話狀態追蹤基準](https://www.google.com/search?q=Dialog+State+Tracking+Challenge+DSTC)
- [Slot Filling 技術](https://www.google.com/search?q=slot+filling+dialogue+system)
- [強化學習對話策略](https://www.google.com/search?q=reinforcement+learning+for+dialog+policy)
