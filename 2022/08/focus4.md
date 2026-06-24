# 管線平行 PipelineParallel

## 基本原理

管線平行是模型平行的改良版本。核心概念是將輸入批次分割成更小的 micro-batch，然後依序送入管線。當 micro-batch 1 在 GPU2 進行運算時，micro-batch 2 可以同時在 GPU1 運算，micro-batch 3 在 GPU0 運算，實現多 GPU 並行。

## 管線排程策略

**Gpipe 排程**：先將所有 micro-batch 填滿管線（warm-up phase），然後進入穩定狀態，最後清空管線（cool-down phase）。簡單但仍有較多閒置時間。

**1F1B 排程**（One-Forward-One-Backward）：交錯執行前向與反向傳播，減少管線氣泡（pipeline bubble），提升 GPU 利用率。

**PipeDream 排程**：支援非對稱的管線排程，允許不同層有不同的計算時間。

## 管線氣泡分析

假設有 P 個 GPU、M 個 micro-batch，則管線氣泡比例約為 (P-1)/M。要降低氣泡，需要增加 micro-batch 數量。實際上通常選擇 m >> p 來達到接近線性加速。

## 梯度累積的關聯

管線平行與梯度累積自然結合：每個 micro-batch 計算梯度後不立即更新，而是累積 K 個 micro-batch 後才更新一次參數。這在管線平行中稱為累積步數。

## 主流實作

PyTorch 提供了 `torch.distributed.pipeline.sync.Pipe` 實作 Gpipe 風格的管線平行。FairScale 和 DeepSpeed 則提供了更進階的管線平行支援。

[搜尋 Pipeline Parallelism 深度學習](https://www.google.com/search?q=pipeline+parallelism+deep+learning)
[搜尋 Gpipe 管線平行](https://www.google.com/search?q=Gpipe+pipeline+parallelism)
