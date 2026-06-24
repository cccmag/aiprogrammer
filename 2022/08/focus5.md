# 張量平行 TensorParallel

## 基本原理

張量平行在單一運算層內進行切割，不同於管線平行的按層切割。對於一個線性層 Y = XA，可以將權重矩陣 A 按列分割成 A1、A2，分別放在兩個 GPU 上，計算結果再透過 All-Reduce 合併。

## 行切割與列切割

**行切割**（Row-wise）：將權重矩陣沿行方向分割。每個 GPU 擁有完整的輸入，但只計算部分輸出。需要一次 All-Reduce 合併輸出。

**列切割**（Column-wise）：將權重矩陣沿列方向分割。每個 GPU 只看到部分輸入特徵，但計算完整的輸出。需要一次 All-Reduce 合併輸入。

## Transformer 中的應用

在 Transformer 模型中，張量平行通常同時應用於：
- Self-Attention 的 QKV 投影層
- FFN 的兩個線性層
- Embedding 層與輸出層

## Megatron-LM 實作

NVIDIA 的 Megatron-LM 是張量平行的代表性實作。其策略為：
- Attention 層：採用列切割 QKV，行切割輸出投影
- FFN 層：第一層行切割，第二層列切割
- 在每個 Transformer block 邊界進行一次 All-Reduce

## 通訊成本

張量平行需要在每次前向傳播中進行兩次 All-Reduce（一次在 Attention，一次在 FFN）。因為通訊發生在計算過程中，對高速互連（如 NVLink）有較高要求，通常只在單機內使用。

[搜尋 Tensor Parallelism Megatron](https://www.google.com/search?q=Megatron+tensor+parallelism)
[搜尋張量平行化Transformer](https://www.google.com/search?q=tensor+parallelism+Transformer)
