# 儲存系統與 I/O

## 前言

計算機的價值不僅在於計算能力，更在於與外部世界的互動能力。I/O（輸入/輸出）系統負責在 CPU、記憶體和外部裝置之間傳輸資料。儲存系統則是 I/O 中最重要的組成部分——它提供了資料的持久化儲存。

## I/O 控制方式

### 程式化 I/O（Programmed I/O）

CPU 直接控制 I/O 操作，透過輪詢（Polling）檢查裝置狀態：

```python
def programmed_io():
    while not device_ready():
        pass  # 輪詢等待
    data = read_device()
    return data
```

優點：簡單易實作。缺點：CPU 在等待 I/O 時被佔用，無法執行其他工作。

### 中斷驅動 I/O（Interrupt-driven I/O）

裝置完成操作後透過中斷通知 CPU：

1. CPU 發起 I/O 請求後繼續執行其他工作
2. 裝置完成操作後發送中斷信號
3. CPU 暫停目前程式，執行中斷服務常式（ISR）
4. ISR 處理完 I/O 後恢復原程式

優點：CPU 與 I/O 裝置可以並行工作。缺點：每個 I/O 操作都需要中斷，大量 I/O 時開銷很大。

### DMA（直接記憶體存取）

DMA 控制器可以在不經 CPU 參與的情況下，直接在 I/O 裝置和記憶體之間傳輸資料：

1. CPU 設定 DMA 控制器（來源位址、目標位址、傳輸大小）
2. DMA 控制器接管匯流排，執行資料傳輸
3. 傳輸完成後 DMA 控制器發送中斷通知 CPU

```python
class DMAController:
    def transfer(self, src, dst, size):
        for i in range(size):
            memory[dst + i] = device[src + i]
        self.interrupt_cpu()
```

優點：CPU 完全解放，適合大量資料傳輸。

## 儲存裝置

### 機械硬碟（HDD）

HDD 使用磁性碟片和移動式讀寫頭來儲存資料：

- **搜尋時間（Seek Time）**：讀寫頭移動到目標磁軌的時間（~5-15ms）
- **旋轉延遲（Rotational Latency）**：碟片旋轉到目標磁區的時間
- **傳輸時間**：資料從碟片讀取到快取的時間

```
HDD 存取時間 ≈ 搜尋時間 + 旋轉延遲 + 傳輸時間
```

### 固態硬碟（SSD）

SSD 使用 NAND Flash 快閃記憶體：

- **隨機讀取**：~10-100μs（比 HDD 快 100-1000 倍）
- **寫入限制**：每個儲存單元有有限的寫入次數（P/E cycles）
- **寫入放大**：Flash 需要先擦除再寫入，導致實際寫入量大於邏輯寫入量

### NVMe vs SATA

| 特性 | SATA SSD | NVMe SSD |
|------|----------|----------|
| 介面頻寬 | 6 Gbps (SATA III) | 4-16 GB/s (PCIe 4.0) |
| 隨機讀取 IOPS | ~100K | ~1M |
| 延遲 | ~100μs | ~10μs |
| 佇列深度 | 32 (AHCI) | 65536 (NVMe) |

## RAID 技術

RAID（Redundant Array of Independent Disks）透過多個硬碟組合成一個邏輯單元，提升效能或可靠性：

| 等級 | 描述 | 最小磁碟數 | 容錯能力 |
|------|------|-----------|---------|
| RAID 0 | 條帶化（Striping） | 2 | 無 |
| RAID 1 | 鏡像（Mirroring） | 2 | 1 顆 |
| RAID 5 | 條帶 + 分散奇偶校驗 | 3 | 1 顆 |
| RAID 6 | 條帶 + 雙奇偶校驗 | 4 | 2 顆 |
| RAID 10 | RAID 1+0 組合 | 4 | 每組 1 顆 |

## I/O 效能指標

### IOPS（每秒 I/O 操作數）

IOPS 是衡量儲存系統效能的重要指標，特別是在隨機存取場景中：

```
IOPS = 1 / (存取延遲)
```

例如：SSD 延遲 100μs → 10,000 IOPS；HDD 延遲 10ms → 100 IOPS

### 吞吐量（Throughput）

吞吐量表示單位時間內傳輸的資料量：

```
吞吐量 = IOPS × 每次 I/O 大小
```

## 小結

I/O 系統的設計目標是最大化 CPU 與外部裝置之間的資料傳輸效率。從程式化 I/O 到中斷驅動再到 DMA，每一個進階都讓 CPU 更專注於計算任務。在儲存方面，從 HDD 到 SSD 再到 NVMe，儲存技術的進步正在持續改變計算機的效能瓶頸。

---

**下一步**：[平行處理架構](focus6.md)

## 延伸閱讀

- [DMA Controller Explained](https://www.google.com/search?q=DMA+controller+explained)
- [NVMe vs SATA vs M.2](https://www.google.com/search?q=NVMe+vs+SATA+vs+M.2+comparison)
- [RAID Levels Explained](https://www.google.com/search?q=RAID+levels+explained+tutorial)
