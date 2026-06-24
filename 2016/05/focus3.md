# 主題三：垃圾回收機制

## 為何需要垃圾回收？

手動記憶體管理容易出錯：
- 記憶體洩漏
- 懸空指標
- 雙重釋放

自動記憶體管理（垃圾回收）解決了這些問題。

## 引用計數

### 基本原理

每個物件維護一個引用計數，歸零時回收：

```python
# 概念示範
import sys

class RefCountedObject:
    def __init__(self, name):
        self.name = name
        self.refcount = 0

    def incref(self):
        self.refcount += 1

    def decref(self):
        self.refcount -= 1
        if self.refcount == 0:
            self.collect()

# Python 物件引用計數（可通過 sys.getrefcount 查看）
x = object()  # refcount = 2（x 和 getrefcount 的臨時引用）
y = x         # refcount = 3
del x         # refcount = 2
del y         # refcount = 1
```

### 優點

- 即時回收
- 簡單實現
- 可預測的延遲

### 缺點

- **無法處理循環引用**
- 每次引用變更需要更新計數
- 並發效能開銷

### Python 的循環垃圾收集器

Python 同時使用引用計數（主要）和循環垃圾收集器（備用）：

```python
import gc

# Python 的 GC 主要處理循環引用
# 當引用計數無法回收時觸發

# 手動觸發
gc.collect()

# 查看 GC 統計
print(gc.get_stats())

# 禁用/啟用 GC
gc.disable()
gc.enable()
```

## 標記-清除（Mark-and-Sweep）

### 演算法步驟

1. **標記階段**：從根集合出發，標記所有可達物件
2. **清除階段**：回收所有未標記的物件

```python
import gc

class GCObject:
    def __init__(self):
        self.refs = []

# 概念實現
class SimpleGC:
    def __init__(self):
        self.objects = []

    def allocate(self, size):
        obj = {'size': size, 'marked': False, 'data': None}
        self.objects.append(obj)
        return obj

    def mark_from_roots(self, roots):
        """從根集合標記所有可達物件"""
        stack = list(roots)
        while stack:
            obj = stack.pop()
            if not obj.get('marked'):
                obj['marked'] = True
                stack.extend(obj.get('refs', []))

    def sweep(self):
        """回收未標記的物件"""
        survivors = []
        for obj in self.objects:
            if obj['marked']:
                obj['marked'] = False
                survivors.append(obj)
            else:
                # 回收記憶體
                pass
        self.objects = survivors
```

### 優點

- 處理循環引用
- 併發效能較好

### 缺點

- 需要停止世界（Stop-the-World）
- 可能造成暫停

## 標記-壓縮（Mark-Compact）

在清除後移動存活物件，避免記憶體碎片：

```
清除前：
[占用][空閒][占用][空閒][占用]

清除後：
[占用][占用][占用][空閒][空閒]
```

## 複製收集（Copying GC）

將記憶體半分為 From 和 To 空間：

```
|---From---|---To---|
存活物件  空格

GC 時：
|---To---|---From---|
存活物件  空格
```

```python
# 複製收集概念
class CopyingGC:
    def __init__(self, size):
        self.from_space = [None] * size
        self.to_space = [None] * size
        self.from_top = 0
        self.to_top = 0

    def allocate(self, obj):
        if self.from_top >= len(self.from_space):
            self.collect()
        self.from_space[self.from_top] = obj
        self.from_top += 1
        return self.from_top - 1

    def collect(self):
        # 複製所有存活物件到 to_space
        self.to_top = 0
        for i in range(self.from_top):
            obj = self.from_space[i]
            if obj is not None:
                self.to_space[self.to_top] = obj
                self.to_top += 1

        # 交換空間
        self.from_space, self.to_space = self.to_space, self.from_space
        self.from_top = self.to_top
```

## 分代回收（Generational GC）

### 核心思想

大多數物件很快就會死亡（弱分代假設）：

```
年輕代（Minor GC）：大多數物件在此死亡
老年代（Major GC）：存活的物件會複製到這裡
```

### JVM 的分代結構

```
年轻代：
  Eden 区
  Survivor S0
  Survivor S1

老年代：
  Old Gen
```

```python
# 分代 GC 概念
class GenerationalGC:
    def __init__(self):
        self.generations = [
            {'size': 1000, 'objects': [], 'threshold': 100},
            {'size': 5000, 'objects': [], 'threshold': 50},
            {'size': 10000, 'objects': [], 'threshold': 10},
        ]

    def allocate(self, gen_idx, obj):
        gen = self.generations[gen_idx]
        if len(gen['objects']) >= gen['size']:
            self.promote(gen_idx)
        gen['objects'].append(obj)

    def promote(self, gen_idx):
        """將存活物件提升到下一代"""
        if gen_idx < len(self.generations) - 1:
            survivors = self.mark_and_sweep(gen_idx)
            for obj in survivors:
                self.allocate(gen_idx + 1, obj)
        else:
            # 老年代：完整 GC
            self.mark_and_sweep(gen_idx)
```

## 即時（JIT）與 GC

現代 JIT 編譯器會配合 GC 進行優化：

```java
// JIT 可能優化的模式
// 1. 標量替換：將物件欄位拆分為獨立變數
// 2. 棧上分配：將短期物件分配在棧上
// 3. 逃逸分析：判斷物件是否會跨執行緒
```

## 各語言的 GC 策略

| 語言 | GC 策略 |
|-----|-------|
| Java | 分代 + 標記-清除 |
| C# | 分代 + 標記-壓縮 |
| Go | 并行標記-清除 |
| Python | 引用計數 + 循環 GC |
| JavaScript | 分代 + 標記-清除 |
| Rust | 無 GC（所有權系統） |

## 調優 GC

### JVM GC 調優

```bash
# 常見 JVM GC 選項
java -XX:+UseG1GC -Xms512m -Xmx2g MyApp

# G1 GC 的目標暫停時間
java -XX:MaxGCPauseMillis=200 MyApp
```

### Python GC 調優

```python
import gc

# 設定閾值
gc.set_threshold(700, 10, 10)

# 禁用 GC
gc.disable()
```

## 小結

垃圾回收是現代程式語言的重要特徵。從引用計數到分代收集，各種演算法都有其適用場景。理解 GC 原理有助於寫出更高效的程式。