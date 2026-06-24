# 平行處理架構

## 前言

當單一核心的效能增長因為功耗和散熱限制而放緩時，平行處理成為持續提升計算效能的關鍵途徑。平行處理可以在不同層級實現：從指令層級到資料層級，再到任務層級。

## 平行處理的分類

Flynn 分類法根據指令流和資料流的數量將計算機架構分為四類：

| 分類 | 說明 | 範例 |
|------|------|------|
| SISD | 單指令流單資料流 | 傳統單核心 CPU |
| SIMD | 單指令流多資料流 | GPU、向量處理器 |
| MISD | 多指令流單資料流 | 容錯系統（罕見） |
| MIMD | 多指令流多資料流 | 多核心 CPU、叢集 |

## 指令層級平行（ILP）

### 超純量（Superscalar）

超純量處理器可以在每個時脈週期發射多條指令到多個執行單元：

```python
class SuperscalarCPU:
    def __init__(self, issue_width=4):
        self.issue_width = issue_width
        self.units = {
            'int_alu': 4,
            'fp_alu': 2,
            'load': 2,
            'store': 1,
        }

    def issue(self, instructions):
        issued = 0
        for inst in instructions:
            if issued >= self.issue_width:
                break
            if self.can_issue(inst):
                self.execute(inst)
                issued += 1
```

### VLIW（超長指令字）

VLIW 處理器將多個操作打包到一條長指令中，由編譯器負責排程：

```
一條 VLIW 指令 = [ALU_op | MEM_op | Branch_op | FP_op]
```

優點：硬體簡單（不需要動態排程）。缺點：依賴編譯器，程式碼體積大。

### 同時多執行緒（SMT / Hyper-Threading）

SMT 讓單一核心同時執行多個執行緒，利用原本會被浪費的管線資源：

```
傳統核心：   |t1|t1|  |t1|  |t1|t1|  |    ← 空白的管線氣泡
SMT 核心：   |t1|t2|t1|t2|t1|t1|t2|    ← 填充氣泡
```

## 執行緒層級平行（TLP）

### 多核心處理器

多核心處理器將多個 CPU 核心整合在單一晶片上，共享最後一級快取和記憶體控制器：

```
┌─────────────────────────┐
│  Core 0  Core 1         │
│  ┌───┐  ┌───┐           │
│  │L1 │  │L1 │           │
│  └───┘  └───┘           │
│  ┌─────────────────────┐ │
│  │      L2 快取        │ │
│  └─────────────────────┘ │
│  ┌─────────────────────┐ │
│  │   記憶體控制器       │ │
│  └─────────────────────┘ │
└─────────────────────────┘
```

### 快取一致性

在多核心系統中，多個核心可能快取同一份資料的不同副本。快取一致性協議（如 MESI）確保所有核心看到一致的資料：

```
MESI 狀態：
M (Modified): 快取行被修改，與主記憶體不一致
E (Exclusive): 只在目前核心的快取中，與主記憶體一致
S (Shared): 在多個核心的快取中，與主記憶體一致
I (Invalid): 快取行無效
```

## 資料層級平行（DLP）

### SIMD 指令

現代的 CPU 都支援 SIMD 指令集，可以在一個指令中同時處理多個資料：

```python
# SIMD 向量加法（一次處理 4 個 32 位元整數）
a = [1, 2, 3, 4]
b = [5, 6, 7, 8]
result = [a[i] + b[i] for i in range(4)]
```

x86 的 SSE/AVX 和 ARM 的 NEON/SVE 都是 SIMD 指令集的實例。

### 向量處理器

向量處理器（如 Cray 系列）專為科學計算設計，可以對整個陣列進行運算：

```
向量指令：VADD V1, V2, V3
等效於：for i in range(vector_length):
            V1[i] = V2[i] + V3[i]
```

## 任務層級平行

### 對稱多處理（SMP）

多個處理器共享同一記憶體匯流排和 I/O 子系統：

- **UMA（Uniform Memory Access）**：所有處理器存取記憶體的延遲相同
- **NUMA（Non-Uniform Memory Access）**：存取本地記憶體更快，存取遠端記憶體較慢

### 大規模平行處理（MPP）

數千個節點透過高速網路互連，每個節點有自己的記憶體（分散式記憶體）。

## 平行程式的挑戰

### Amdahl 定律

```
Speedup = 1 / ((1 - P) + P/N)
```

其中 P 是可平行化的比例，N 是處理器數量。即使 P = 0.95，使用 20 個處理器後加速比只有 10。

### 負載平衡

平行程式的效能受限於最慢的執行緒——所有執行緒必須同步等待最慢的同伴完成。

## 小結

平行處理是現代計算機架構的核心趨勢。從指令層級（超純量、管線）到資料層級（SIMD、向量處理）再到執行緒層級（多核心、SMT），不同層級的平行技術正在被整合到一個處理器中。

---

**下一步**：[現代計算機架構趨勢](focus7.md)

## 延伸閱讀

- [Flynn's Taxonomy](https://www.google.com/search?q=Flynn+taxonomy+parallel+computing)
- [Cache Coherence - MESI Protocol](https://www.google.com/search?q=MESI+cache+coherence+protocol)
- [SIMD vs MIMD](https://www.google.com/search?q=SIMD+vs+MIMD+architecture)
