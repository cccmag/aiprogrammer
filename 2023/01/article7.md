# 虛擬記憶體

## 1. 引言

虛擬記憶體（Virtual Memory）是計算機架構中另一項至關重要的技術。它讓每個程式擁有獨立的、連續的位址空間，而實際的資料可以分散在實體記憶體的各個位置，甚至被暫時移動到磁碟上。

## 2. 虛擬位址 vs 實體位址

### 2.1 為什麼需要虛擬記憶體

1. **隔離性**：程式 A 不能存取程式 B 的記憶體
2. **簡化程式設計**：每個程式看到連續的位址空間
3. **共享記憶體**：多個程式可以映射到同一實體頁面
4. **超額配置**：程式可以使用比實體記憶體更多的空間

```python
class VirtualMemory:
    def __init__(self, page_size=4096, num_pages=256):
        self.page_size = page_size
        self.page_table = [None] * num_pages
        self.physical_memory = {}  # 實體頁框 → 資料

    def virtual_to_physical(self, virtual_addr):
        vpn = virtual_addr // self.page_size
        offset = virtual_addr % self.page_size
        pfn = self.page_table[vpn]
        if pfn is None:
            raise PageFault()
        return pfn * self.page_size + offset
```

## 3. 分頁機制

### 3.1 頁面與頁框

- **頁面（Page）**：虛擬位址空間的分割單位
- **頁框（Page Frame）**：實體記憶體的分割單位
- 頁面和頁框通常大小相同（4KB 是常見選擇）

### 3.2 頁表結構

頁表（Page Table）是虛擬位址到實體位址的映射表：

```python
class PageTableEntry:
    def __init__(self):
        self.present = False   # 是否在實體記憶體中
        self.pfn = 0           # 實體頁框號碼
        self.dirty = False     # 是否被修改
        self.accessed = False  # 是否被存取
        self.rw = True         # 讀寫權限
        self.user = False      # 使用者模式存取權限
```

### 3.3 多層頁表

為了解決頁表過大的問題，現代處理器使用多層頁表：

```python
class TwoLevelPageTable:
    def __init__(self):
        self.level1 = [None] * 1024  # 第一級

    def translate(self, virtual_addr):
        # 假設虛擬位址 32 位元，頁面 4KB
        # 頁內偏移: bits 0-11 (12 bits)
        # 第二級索引: bits 12-21 (10 bits)
        # 第一級索引: bits 22-31 (10 bits)
        l1_idx = (virtual_addr >> 22) & 0x3FF
        l2_idx = (virtual_addr >> 12) & 0x3FF
        offset = virtual_addr & 0xFFF
        if self.level1[l1_idx] is None:
            return None  # Page Fault
        l2_table = self.level1[l1_idx]
        entry = l2_table[l2_idx]
        if not entry.present:
            return None
        return entry.pfn * 4096 + offset
```

## 4. TLB

### 4.1 TLB 的工作原理

TLB（Translation Lookaside Buffer）是頁表的快取，加速位址轉換：

```python
class TLB:
    def __init__(self, num_entries=64):
        self.entries = [None] * num_entries

    def lookup(self, vpn):
        for i, entry in enumerate(self.entries):
            if entry and entry['vpn'] == vpn:
                return entry['pfn']
        return None

    def update(self, vpn, pfn):
        idx = hash(vpn) % len(self.entries)
        self.entries[idx] = {'vpn': vpn, 'pfn': pfn}
```

### 4.2 TLB 失誤的處理

```
TLB Hit  : 直接取得實體位址（1-2 週期）
TLB Miss : 查詢頁表（數十到數百週期）
Page Fault: 從磁碟載入頁面（數百萬週期）
```

## 5. 頁面置換演算法

### 5.1 FIFO 頁面置換

先進先出，最簡單的置換演算法：

```python
def fifo_page_replacement(pages, num_frames):
    frames = []
    page_faults = 0
    for page in pages:
        if page in frames:
            continue
        if len(frames) < num_frames:
            frames.append(page)
        else:
            frames.pop(0)   # 移除最舊的
            frames.append(page)
        page_faults += 1
    return page_faults
```

### 5.2 LRU 頁面置換

理論上最優的可實作演算法：

```python
def lru_page_replacement(pages, num_frames):
    frames = []
    page_faults = 0
    for page in pages:
        if page in frames:
            frames.remove(page)  # 移到最後
            frames.append(page)
        else:
            if len(frames) >= num_frames:
                frames.pop(0)   # 移除最近最少使用的
            frames.append(page)
            page_faults += 1
    return page_faults
```

### 5.3 時鐘演算法（Clock Algorithm）

一個更有效率的 LRU 近似演算法，使用參考位元：

```python
class ClockAlgorithm:
    def __init__(self, num_frames=4):
        self.frames = [None] * num_frames
        self.ref_bits = [0] * num_frames
        self.hand = 0

    def access(self, page):
        if page in self.frames:
            idx = self.frames.index(page)
            self.ref_bits[idx] = 1
            return True  # Hit
        # Miss：使用時鐘指針尋找替換頁面
        while self.ref_bits[self.hand] == 1:
            self.ref_bits[self.hand] = 0  # 清除參考位元，給第二次機會
            self.hand = (self.hand + 1) % len(self.frames)
        self.frames[self.hand] = page
        self.ref_bits[self.hand] = 1
        self.hand = (self.hand + 1) % len(self.frames)
        return False
```

## 6. 虛擬記憶體的效能影響

### 6.1 有效存取時間

```
EAT = Hit Rate × TLB Hit Time + Miss Rate × TLB Miss Penalty
```

### 6.2 抖動（Thrashing）

當系統花費更多時間在頁面置換而非實際計算時，稱為抖動。這通常發生在實體記憶體不足時。

## 7. 結語

虛擬記憶體是現代作業系統的基石。它不僅提供了記憶體隔離和保護，還讓程式可以使用比實體記憶體更大的位址空間。理解虛擬記憶體的原理——頁表、TLB、頁面置換——對於系統程式設計師和效能工程師來說至關重要。

---

**下一步**：[RISC vs CISC](article8.md)

## 延伸閱讀

- [Virtual Memory Explained](https://www.google.com/search?q=virtual+memory+explained+computer+architecture)
- [Page Replacement Algorithms](https://www.google.com/search?q=page+replacement+algorithms+FIFO+LRU+clock)
- [TLB - Translation Lookaside Buffer](https://www.google.com/search?q=TLB+translation+lookaside+buffer+tutorial)
