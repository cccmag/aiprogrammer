# 稀疏注意力與高效注意力

## 計算複雜度問題

標準的 Self-Attention 需要計算一個 n×n 的注意力矩陣，其中 n 是序列長度。這帶來 O(n²) 的時間和空間複雜度。對於實際應用：

- 當 n = 512（典型 BERT 序列長度）：注意力矩陣約 250K 元素，可接受
- 當 n = 8192（長文件任務）：注意力矩陣約 67M 元素，需大量 GPU 記憶體
- 當 n = 1M（整本書或基因序列）：注意力矩陣約 10¹² 元素，完全不可行

這個問題被稱為 Transformer 的「長序列瓶頸」。

### 記憶體消耗的具體估算

對於批次大小 b=1、頭數 h=12、序列長度 n=8192、精度為 float16：
- 注意力分數矩陣：8192 × 8192 × 2 bytes = 134 MB per head
- 12 個頭共需：1.6 GB
- 加上中間激活值，總記憶體需求輕鬆超過 8 GB

## 局部與全域注意力

### 滑動窗口注意力

一個直觀的想法是：每個位置只需要關注它附近的鄰居。滑動窗口注意力（Sliding Window Attention）將注意力範圍限制在固定大小的視窗內：

```
    n=8, window_size=3

    x₁──x₂──x₃──x₄──x₅──x₆──x₇──x₈
    │   │   │
    └───┴───┘
        │   │   │
        └───┴───┘
            │   │   │
            └───┴───┘
```

時間複雜度從 O(n²) 降低到 O(n×w)，其中 w 是窗口大小。

### BigBird 和 Longformer

BigBird 和 Longformer 結合了三種注意力模式：

1. **滑動窗口注意力**：捕獲局部上下文
2. **全域注意力**：選定位置關注整個序列
3. **隨機注意力**：隨機選取位置對，增加連接的隨機性

```
■ = 窗口注意力  ● = 全域注意力  ○ = 隨機注意力

位置  ■  ●  ■  ○  ■  ■  ○  ■
 1    ■  ●  ■      ○
 2    ■  ■  ●  ■
 3 ●     ■  ■  ●  ■
 4    ○     ■  ■  ●  ■      ○
 5       ○     ■  ■  ●  ■
 6          ○     ■  ■  ●  ■
 7 ●              ○     ■  ■  ●
 8    ○                 ○     ■  ■
```

這種組合在保持 O(n) 計算複雜度的同時，保留了捕捉長距離依賴的能力。

## FlashAttention

### IO 感知的演算法設計

FlashAttention（Dao 等人，2022）從一個不同的角度解決效率問題：它不減少計算量，而是優化 GPU 記憶體訪問模式。

GPU 的記憶體層次結構：
```
GPU DRAM (HBM) ─── 40 TB/s, 80 GB
      ⬆  ⬇  (慢速傳輸)
SRAM (on-chip) ─── 200 TB/s, 192 KB
```

標準注意力實現需要：
1. 從 HBM 讀取 Q、K、V
2. 計算 S = Q K^T，寫回 HBM
3. 從 HBM 讀取 S，計算 P = softmax(S)，寫回 HBM
4. 從 HBM 讀取 P 和 V，計算 O = P V，寫回 HBM

這需要多次 HBM 往返，而 HBM 頻寬是主要的瓶頸。

### FlashAttention 的創新

FlashAttention 通過「平鋪」（tiling）技術，將整個注意力計算分解為多個小塊，在 SRAM 中完成所有計算：

```
對於每個塊:
  1. 從 HBM 載入 Q、K、V 的塊到 SRAM
  2. 在 SRAM 中計算塊的 S = Q K^T
  3. 在 SRAM 中計算塊的 softmax
  4. 在 SRAM 中計算 O = P V
  5. 將部分結果寫回 HBM
```

這樣只需要 1 次 HBM 讀取和 1 次寫入，而不是標準方法的多次往返。

### 實際收益

- **速度提升**：2-4 倍（相對於 PyTorch 標準實現）
- **記憶體節省**：5-10 倍（不需要儲存整個 n×n 注意力矩陣）
- **精度保持**：與標準注意力完全一致（不是近似方法）

## 線性注意力

### Kernel 方法

線性注意力（Katharopoulos 等人，2020）將 softmax 注意力重寫為特徵映射的形式：

```
softmax(Q K^T) V ≈ φ(Q) (φ(K)^T V)
```

其中 φ 是核函數對應的特徵映射。這個重寫將計算複雜度從 O(n² d) 降低到 O(n d²)。

### Linear Transformer

當 d << n 時（通常 d=512, n >> 512），線性注意力的優勢明顯。但線性注意力通常在品質上不如標準注意力，因為核函數的近似引入了資訊損失。

## 未來方向

高效注意力的未來發展包括：
- **硬體專用優化**：NVIDIA H100 的 Transformer Engine 已包含注意力優化
- **混合方法**：結合稀疏注意力和 FlashAttention 的優勢
- **動態稀疏性**：根據輸入動態決定哪些注意力計算可以跳過
- **狀態空間模型**：Mamba 等新架構嘗試完全取代注意力機制

---

**延伸閱讀**
- [FlashAttention: Fast and Memory-Efficient Exact Attention](https://www.google.com/search?q=FlashAttention+2022)
- [BigBird: Transformers for Longer Sequences](https://www.google.com/search?q=BigBird+sparse+attention)
- [Linear Transformers](https://www.google.com/search?q=linear+transformer+attention)
