# CPU 微架構

## CPU 基本結構

```
┌─────────────────────────────────────────────────────┐
│                      CPU                             │
├─────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │  Fetch  │→ │  Decode │→ │  Issue  │             │
│  └────┬────┘  └────┬────┘  └────┬────┘             │
│       │            │            │                   │
│       └────────────┴────────────┘                   │
│                    ↓                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────┐  │
│  │   ALU   │  │   ALU   │  │  Load   │  │ Store │  │
│  │  (Exec) │  │  (Exec) │  │  Store  │  │ (Exec)│  │
│  └─────────┘  └─────────┘  └─────────┘  └───────┘  │
│                    ↓                                 │
│  ┌─────────────────────────────────────────┐        │
│  │            Register File                │        │
│  └─────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

## 管線化（Pipeline）

### 典型 x86 管線

```
Stage 1: Fetch (IF)
Stage 2: Decode (ID)
Stage 3: Execute (EX)
Stage 4: Memory (MEM)
Stage 5: Write Back (WB)
```

### 管線深度與效能

- 較深的管線：更高的時脈頻率
- 較淺的管線：更少的冒險（hazard）

## 微架構最佳化

### 超純量（Superscalar）

多個執行單元同時執行指令。

```
       ┌──→ ALU1 ─→
       │       ┌──→ ALU2 ─→ Register File
Fetch ─┼──→ ALU3 ─→           ↑
       │       └──→ Load ────┘
       └──→ Branch ─→ PC Update
```

### 亂序執行（Out-of-Order Execution）

```c++
// 這兩行可以並行執行
int a = b + c;  // 使用 ALUA
int d = e + f;  // 使用 ALUB

// 但這些必須順序執行
x = y + z;
w = x + 1;  // 依賴 x
```

## 快取層次

### 典型的快取配置

| 層次 | 大小 | 延遲 |
|-----|------|-----|
| L1 I-Cache | 32 KB | 4 週期 |
| L1 D-Cache | 32 KB | 4 週期 |
| L2 Cache | 256 KB | 12 週期 |
| L3 Cache | 8 MB | 30-40 週期 |

### 預取器

```c
// 硬體預取：自動偵測模式並預取
for (int i = 0; i < n; i += 2) {  // 2 為預取跨距
    process(data[i]);
}
```

## 分支預測

### 歷史表基礎

- **BTB**（分支目標緩冲區）：儲存跳躍位址
- **BHT**（分支歷史表）：追蹤分支模式
- **RAS**（返回位址堆疊）：函數返回位址

### 兩層分支預測

```
+---+---+---+---+---+---+---+---+
│   │   │   │   │   │   │   │   │
+---+---+---+---+---+---+---+---+
  0   0   0   1   1   1   1   0   ← Pattern History Table
```

## 指令延遲

| 指令類型 | 延遲 |
|---------|------|
| 整數加法 | 1 週期 |
| 整數乘法 | 3 週期 |
| 浮點加法 | 4 週期 |
| 浮點乘法 | 4-7 週期 |
| 除法 | 12-25 週期 |
| 記憶體載入 | 4 週期（命中 L1） |

## 微架構特定優化

### Intel Haswell / Skylake

- 2 個載入/儲存單元
- 4 個 ALU（但每週期只能發射 4 條指令）
- 2 個 FP 單元

### AMD Zen

- 4 個 ALU + 2 個 AGU
- 每週期可發射 5 條指令

## 效能監視器

### 使用 perf 監控

```bash
# 監控快取命中率
perf stat -e cache-references,cache-misses ./program

# 監控分支預測
perf stat -e branches,branch-misses ./program

# 監控管線停頓
perf stat -e cycles,stalled-cycles-frontend,stalled-cycles-backend ./program
```

## 參考資料

- [CPU 微架構](https://www.google.com/search?q=CPU+microarchitecture+tutorial)
- [指令延遲](https://www.google.com/search?q=instruction+latency+Intel+Haswell)