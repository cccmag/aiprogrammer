# All-Reduce 通訊原語

## 什麼是 All-Reduce

All-Reduce 是分散式運算中最核心的集體通訊操作。它從所有 worker 收集資料，進行某種 reduction 操作（通常是求和或平均），然後將結果分發回所有 worker。

## Ring All-Reduce

最經典的 All-Reduce 實作是 Ring All-Reduce。它將 GPU 排列成環狀，資料分割成多個 chunk，透過兩階段完成：

**Reduce-Scatter 階段**：每個 GPU 將自己的 chunk 發送給下一個 GPU，同時從上一個 GPU 接收 chunk，逐步累加結果。經過 N-1 步後，每個 GPU 擁有部分資料的完整歸約結果。

**All-Gather 階段**：每個 GPU 將累積結果廣播給下一個 GPU。經過 N-1 步後，所有 GPU 擁有完整資料。

## 通訊複雜度

Ring All-Reduce 的通訊量為 `2 * (N-1) * K / N`（K 為資料量），當 N 很大時接近 2K。優於簡單的 parameter server 架構（需要 2K * N）。

## 雙樹演算法

雖然 Ring 演算法在一般規模下表現良好，但在極大規模時延遲較高。雙樹（Double Binary Tree）演算法以 O(log N) 的步驟完成歸約，適合數百 GPU 以上的場景。

## 實際應用中的 All-Reduce

在 PyTorch DDP 中，每個反向傳播步驟結束後自動觸發一次梯度 All-Reduce。NCCL 的 `ncclAllReduce` 提供了 GPU 上的高效實作。透過梯度壓縮技術可進一步減少通訊量。

[搜尋 All-Reduce 演算法](https://www.google.com/search?q=All-Reduce+algorithm+distributed+training)
[搜尋 Ring All-Reduce 深度學習](https://www.google.com/search?q=Ring+All-Reduce+deep+learning)
