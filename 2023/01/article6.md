# 快取記憶體策略

## 1. 引言

快取記憶體（Cache Memory）是計算機架構中最重要的效能最佳化技術之一。它利用局部性原理，在 CPU 和主記憶體之間放置一個小而快的記憶體，顯著降低平均記憶體存取時間。

本文將深入探討快取的映射方式、替換策略和寫入策略，並透過 Python 模擬比較不同策略的效能。

## 2. 快取的基本原理

### 2.1 快取命中與失誤

```python
class CacheLine:
    def __init__(self):
        self.valid = False
        self.tag = 0
        self.data = 0
        self.dirty = False
```

- **Hit**：需要的資料在快取中，直接讀取
- **Miss**：需要的資料不在快取中，從下一級記憶體載入

### 2.2 位址分割

```
記憶體位址 = Tag | Index | Block Offset
```

- **Block Offset**：定位快取行內的哪個位元組
- **Index**：定位快取中的哪一組
- **Tag**：比對是否為目標資料

## 3. 映射方式

### 3.1 直接映射

每個記憶體塊只能映射到快取的唯一位置：

```python
class DirectMappedCache:
    def __init__(self, num_lines=16):
        self.lines = [CacheLine() for _ in range(num_lines)]

    def access(self, address):
        idx = (address // self.block_size) % self.num_lines
        tag = address // (self.block_size * self.num_lines)
        line = self.lines[idx]
        if line.valid and line.tag == tag:
            return True  # Hit
        # Miss：載入新資料
        line.valid = True
        line.tag = tag
        return False
```

**優點**：簡單、快速、成本低。**缺點**：衝突失誤率高。

### 3.2 全關聯映射

任何記憶體塊可以放在快取的任何位置：

```python
class FullyAssociativeCache:
    def __init__(self, num_lines=16):
        self.lines = [CacheLine() for _ in range(num_lines)]

    def access(self, address):
        tag = address // self.block_size
        for line in self.lines:
            if line.valid and line.tag == tag:
                return True  # Hit
        # Miss：需要替換
        idx = self.find_victim()
        self.lines[idx].valid = True
        self.lines[idx].tag = tag
        return False
```

**優點**：衝突失誤最低。**缺點**：比對所有快取行，硬體成本高。

### 3.3 組關聯映射

最務實的方案，將快取分為多組，每組包含多個快取行：

```python
class SetAssociativeCache:
    def __init__(self, num_sets=8, associativity=4):
        self.sets = [[CacheLine() for _ in range(associativity)] for _ in range(num_sets)]

    def access(self, address):
        idx = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)
        for line in self.sets[idx]:
            if line.valid and line.tag == tag:
                return True
        return False
```

## 4. 替換策略

### 4.1 LRU（Least Recently Used）

LRU 替換最近最少使用的快取行，是理論上最優的替換策略：

```python
class LRUCache:
    def __init__(self, num_lines=16):
        self.lines = [None] * num_lines
        self.ages = [0] * num_lines

    def access(self, address):
        tag = address // self.block_size
        for i, line in enumerate(self.lines):
            if line == tag:
                self.ages[i] = 0  # 最近使用
                self.increment_ages(i)
                return True
        # Miss
        victim = self.ages.index(max(self.ages))
        self.lines[victim] = tag
        self.ages[victim] = 0
        self.increment_ages(victim)
        return False

    def increment_ages(self, exclude):
        for i in range(len(self.ages)):
            if i != exclude:
                self.ages[i] += 1
```

### 4.2 FIFO

先進先出策略，實作簡單但效能不如 LRU。

### 4.3 隨機替換

最簡單的策略，在某些場景下效能意外地好：

```python
import random
def random_replacement(cache_lines, new_line):
    idx = random.randrange(len(cache_lines))
    cache_lines[idx] = new_line
```

### 4.4 策略比較

| 策略 | 命中率 | 硬體成本 | 實作複雜度 |
|------|--------|---------|-----------|
| LRU | 高 | 高 | 高 |
| FIFO | 中 | 中 | 中 |
| 隨機 | 中 | 低 | 低 |

## 5. 寫入策略

### 5.1 Write-through

資料同時寫入快取和主記憶體：

```python
def write_through(cache, address, data):
    cache.write(address, data)
    memory.write(address, data)  # 同步寫入主記憶體
```

**優點**：快取和主記憶體始終一致，硬體簡單。**缺點**：每次寫入都需要存取主記憶體。

### 5.2 Write-back

只寫入快取，標記為髒（dirty），在替換時才寫回主記憶體：

```python
class WriteBackCache:
    def write(self, address, data):
        tag = address // self.block_size
        idx = self.index(address)
        self.lines[idx].data = data
        self.lines[idx].tag = tag
        self.lines[idx].dirty = True  # 標記為髒

    def evict(self, idx):
        if self.lines[idx].dirty:
            memory.write(self.lines[idx].tag * self.block_size, self.lines[idx].data)
```

**優點**：減少主記憶體寫入次數。**缺點**：硬體更複雜，需要髒位元。

## 6. 快取效能模擬

```python
def cache_simulation():
    configs = [
        ("Direct-mapped, 16 lines", DirectMappedCache(16)),
        ("2-way, 8 sets", SetAssociativeCache(8, 2)),
        ("Fully associative, LRU", LRUCache(16)),
    ]
    addresses = [0, 64, 128, 0, 64, 192, 256, 0, 64, 128]
    for name, cache in configs:
        hits = sum(1 for a in addresses if cache.access(a))
        print(f"{name}: {hits}/{len(addresses)} hits")
```

## 7. 結語

快取的效能取決於多個因素的權衡：映射方式決定了硬體成本和衝突失誤率的平衡，替換策略影響快取的有效利用率，寫入策略則在效能和一致性之間取捨。

對程式設計師而言，理解快取有助於寫出快取友好的程式碼：順序存取陣列（利用空間局部性）、重用資料（利用時間局部性）、避免隨機存取模式。

---

**下一步**：[虛擬記憶體](article7.md)

## 延伸閱讀

- [Cache Memory - Mapping, Replacement, Writing](https://www.google.com/search?q=cache+memory+mapping+replacement+write+policy)
- [LRU vs Random Cache Replacement](https://www.google.com/search?q=LRU+vs+random+cache+replacement+performance)
- [Write-through vs Write-back Cache](https://www.google.com/search?q=write+through+vs+write+back+cache)
