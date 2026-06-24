# 記憶體階層

## 前言

記憶體階層（Memory Hierarchy）是計算機架構中最重要的概念之一。它利用「局部性原理」（Principle of Locality）來平衡速度、容量和成本之間的取捨——讓記憶體系統看起來既快又大又便宜。

## 記憶體階層的結構

### 金字塔模型

```
                  ┌──────┐
                  │暫存器 │  速度：最快（~0.3ns）
                  │ 1 KB │  容量：最小
               ┌──┴──────┴──┐
               │  L1 快取    │  速度：~1ns
               │ 32-64 KB   │
            ┌──┴──────────┴──┐
            │   L2 快取      │  速度：~3-10ns
            │  256-512 KB   │
         ┌──┴──────────────┴──┐
         │    L3 快取         │  速度：~10-40ns
         │   2-32 MB         │
      ┌──┴──────────────────┴──┐
      │     主記憶體（DRAM）    │  速度：~50-100ns
      │       8-512 GB        │
   ┌──┴──────────────────────┴──┐
   │     SSD/NVMe 固態硬碟      │  速度：~10-100μs
   │       256 GB-2 TB        │
┌──┴──────────────────────────┴──┐
│      HDD 機械硬碟              │  速度：~5-15ms
│        1-20 TB                │  容量：最大
└──────────────────────────────┘
```

### 局部性原理

快取能夠有效工作的理論基礎是局部性原理：

1. **時間局部性（Temporal Locality）**：最近存取的資料很可能在短期內再次被存取（如迴圈變數）
2. **空間局部性（Spatial Locality）**：存取某個位址附近的資料很可能也會被存取（如陣列遍歷）

## 快取記憶體

### 快取的基本結構

快取由多個「快取行」（Cache Line）組成，每個快取行儲存一個「塊」（Block）。快取使用「標籤」（Tag）來標識資料的記憶體位址。

### 快取映射方式

**1. 直接映射（Direct-mapped）**

```
記憶體位址 = 標籤(Tag) | 索引(Index) | 偏移(Offset)
```

每個記憶體塊只能映射到快取中的一個特定位置。簡單但衝突率較高。

**2. 全關聯映射（Fully Associative）**

任何記憶體塊可以放在快取的任何位置。靈活性最高但硬體成本也最高。

**3. 組關聯映射（Set-associative）**

```
n-way 組關聯：快取分為若干組，每組有 n 個快取行
```

現在處理器通常使用 8-way 或 16-way 組關聯映射。

### 快取替換策略

當快取已滿且需要載入新資料時，必須決定替換哪個快取行：

- **LRU（Least Recently Used）**：替換最近最少使用的行
- **FIFO**：替換最早載入的行
- **隨機替換**：簡單但效能適中
- **LFU（Least Frequently Used）**：替換使用頻率最低的行

### 寫入策略

- **Write-through**：資料同時寫入快取和主記憶體
- **Write-back**：只寫入快取，標記為「髒」（dirty），在替換時才寫回主記憶體

## 主記憶體

### DRAM 組織

主記憶體使用 DRAM（動態隨機存取記憶體），每個位元由一個電容和一個電晶體組成。DRAM 需要定期刷新（refresh）以維持資料。

### 記憶體頻寬計算

```
記憶體頻寬 = 時脈頻率 × 資料寬度 × 傳輸次數/週期
```

例如 DDR4-3200：`3200 MHz × 64 bits / 8 × 1 = 25.6 GB/s`

## 虛擬記憶體

虛擬記憶體是記憶體階層的重要延伸，它讓每個程式擁有獨立的位址空間：

- **頁（Page）**：虛擬記憶體的基本單位（通常 4KB）
- **頁表（Page Table）**：將虛擬位址映射到實體位址
- **TLB（Translation Lookaside Buffer）**：頁表的快取，加速位址轉換

## 效能分析

### 平均記憶體存取時間

```
AMAT = Hit Time + Miss Rate × Miss Penalty
```

其中 Miss Penalty 是從下一級記憶體讀取資料所需的時間。

### 範例計算

```
L1 快取：Hit Time = 1ns, Miss Rate = 5%
L2 快取：Hit Time = 10ns, Miss Rate = 20%
主記憶體：Hit Time = 100ns

AMAT = 1 + 0.05 × (10 + 0.2 × 100) = 1 + 0.05 × 30 = 2.5 ns
```

如果沒有快取：AMAT = 100ns。快取將存取時間從 100ns 降低到 2.5ns，加速 40 倍。

## 小結

記憶體階層是計算機架構中速度與容量的妥協藝術。快取的效能關鍵在於局部性原理的利用——程式撰寫時注意資料存取模式，可以大幅提升快取命中率。

---

**下一步**：[儲存系統與 I/O](focus5.md)

## 延伸閱讀

- [Memory Hierarchy Design](https://www.google.com/search?q=memory+hierarchy+design+computer+architecture)
- [Cache Memory Principles](https://www.google.com/search?q=cache+memory+principles+tutorial)
- [DDR5 vs DDR4 Memory](https://www.google.com/search?q=DDR5+vs+DDR4+memory+comparison)
