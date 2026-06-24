# 分散式訓練與模型平行化 — 主題介紹

## 為何需要分散式訓練？

深度學習的發展趨勢是越大越好：更大的模型、更多的資料、更强的算力。然而，單卡的記憶體和算力有限。GPT-3 有 1750 億參數，訓練資料需要數 TB，單卡不可能完成。分散式訓練是突破這個限制的關鍵技術。

## 兩種主要的平行策略

根據分割方式，分散式訓練可分為資料平行（Data Parallelism）和模型平行（Model Parallelism）。資料平行中，每個運算單元有完整的模型副本，只分割輸入資料；適合資料量大、模型相對較小的場景。模型平行中，單一運算單元只持有模型的一部分；適合模型巨大、無法放入單卡的場景。實際應用中常組合兩者。

## 記憶體挑戰

模型訓練需要儲存參數、梯度、優化器狀態和中間活化值。對於大模型，優化器狀態佔用最多記憶體（Adam 需要保存兩階動量）。這催生了 ZeRO（零冗餘優化器）等記憶體優化技術。

## 通訊開銷

分散式訓練的一個關鍵瓶頸是節點間的通訊。梯度同步需要網路頻寬，節點越多、通訊越頻繁、性能瓶頸越明顯。梯度壓縮、計算和通訊重疊、張量分片等技術都是為了緩解這個問題。

## 本期導覽

[focus1](focus1.md) 介紹資料平行的基本原理。[focus2](focus2.md) 探討模型平行與管線平行。[focus3](focus3.md) 深入 ZeRO 的設計。[focus4](focus4.md) 解釋梯度 checkpointing。[focus5](focus5.md) 展示 PyTorch 分散式訓練實踐。[focus6](focus6.md) 討論張量平行。[focus7](focus7.md) 涵蓋混合精度訓練。十篇 [article](articles.md) 提供更深入的專題分析。

## 參考資源

- DeepSpeed GitHub：https://www.google.com/search?q=DeepSpeed+Microsoft+GitHub
- PyTorch Distributed：https://www.google.com/search?q=PyTorch+distributed+training+documentation