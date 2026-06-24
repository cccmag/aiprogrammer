# 附加：程式語言實作範例

## 程式碼範例說明

本期的主題是程式語言理論與實現，我們特別準備了記憶體管理、垃圾回收、和簡單虛擬機的範例程式。

## 目錄結構

```
_code/
├── memory/
│   ├── simple_alloc.py      # 簡單記憶體分配器
│   ├── reference_count.py    # 引用計數實現
│   └── gc_simulation.py     # GC 模擬
├── vm/
│   ├── stack_vm.py          # 簡單棧式虛擬機
│   └── bytecode_gen.py      # 位元組碼生成
├── threading/
│   ├── mutex_demo.py        # 互斥鎖示例
│   └── producer_consumer.py # 生產者消費者問題
└── test.sh                  # 測試腳本
```

## 記憶體管理範例

### 簡單記憶體分配器

```python
# simple_alloc.py - 簡化的記憶體分配器
# 概念類似 malloc 的簡化實現

class SimpleAllocator:
    def __init__(self, size=1024):
        self.memory = bytearray(size)
        self.allocated = [False] * size
        self.size = size

    def allocate(self, n):
        """找到第一個足夠大的連續空間"""
        # 簡單的首次適配
        start = 0
        count = 0
        for i in range(self.size):
            if not self.allocated[i]:
                count += 1
                if count >= n:
                    # 找到足夠空間
                    for j in range(start, i + 1):
                        self.allocated[j] = True
                    return start
            else:
                start = i + 1
                count = 0
        return -1  # 記憶體不足

    def free(self, addr, n):
        """釋放記憶體"""
        for i in range(addr, addr + n):
            self.allocated[i] = False

    def dump(self):
        """顯示記憶體狀態"""
        for i in range(self.size):
            status = "X" if self.allocated[i] else "_"
            if i % 64 == 0:
                print(f"\n{i:04d}: ", end="")
            print(status, end="")
        print()
```

### 引用計數實現

```python
# reference_count.py - 引用計數 GC

class RefCountedObject:
    def __init__(self, name):
        self.name = name
        self.refcount = 0
        print(f"Created {name}")

    def add_ref(self):
        self.refcount += 1
        return self

    def release(self):
        self.refcount -= 1
        if self.refcount <= 0:
            print(f"GC: Collecting {self.name}")
            return True
        return False

class RefCountGC:
    def __init__(self):
        self.objects = {}

    def new_object(self, name):
        obj = RefCountedObject(name)
        self.objects[name] = obj
        return obj.add_ref()

    def reference(self, obj):
        return obj.add_ref()

    def release(self, obj):
        if obj.release():
            del self.objects[obj.name]
```

### GC 模擬

```python
# gc_simulation.py - 標記-清除 GC 模擬

class GCObject:
    def __init__(self, name, refs=None):
        self.name = name
        self.refs = refs or []
        self.marked = False

class MarkSweepGC:
    def __init__(self):
        self.heap = []
        self.roots = []

    def allocate(self, name, refs=None):
        obj = GCObject(name, refs)
        self.heap.append(obj)
        return obj

    def add_root(self, obj):
        self.roots.append(obj)

    def mark(self):
        """標記所有可達物件"""
        stack = list(self.roots)
        while stack:
            obj = stack.pop()
            if not obj.marked:
                obj.marked = True
                stack.extend(obj.refs)

    def sweep(self):
        """回收未標記的物件"""
        collected = []
        survivors = []
        for obj in self.heap:
            if obj.marked:
                obj.marked = False
                survivors.append(obj)
            else:
                collected.append(obj)
        self.heap = survivors
        return collected

    def collect(self):
        print("Starting GC...")
        self.mark()
        collected = self.sweep()
        print(f"Collected {len(collected)} objects")
        return collected
```

## 虛擬機範例

### 簡單棧式虛擬機

```python
# stack_vm.py - 簡單的棧式虛擬機

class StackVM:
    def __init__(self):
        self.stack = []
        self.locals = {}
        self.ip = 0  # 指令指標

    def execute(self, bytecode):
        """執行位元組碼"""
        ops = {
            'ICONST': lambda v: self.stack.append(v),
            'IADD': lambda: self._binop(lambda a, b: a + b),
            'ISUB': lambda: self._binop(lambda a, b: a - b),
            'IMUL': lambda: self._binop(lambda a, b: a * b),
            'ILT': lambda: self._compare(lambda a, b: a < b),
            'BR': lambda dest: self.__dict__.update({'ip': dest - 1}),
            'BRT': lambda dest: self._branch_true(dest),
            'BRF': lambda dest: self._branch_false(dest),
            'LOAD': lambda idx: self.stack.append(self.locals.get(idx, 0)),
            'STORE': lambda idx: self.locals.update({idx: self.stack.pop()}),
            'HALT': lambda: None,
        }

        self.ip = 0
        while self.ip < len(bytecode):
            op, *args = bytecode[self.ip]
            if op == 'HALT':
                break
            ops[op](*args) if args else ops[op]()
            self.ip += 1

        return self.stack[-1] if self.stack else None

    def _binop(self, op):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(op(a, b))

    def _compare(self, op):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if op(a, b) else 0)

    def _branch_true(self, dest):
        if self.stack.pop():
            self.ip = dest - 1

    def _branch_false(self, dest):
        if not self.stack.pop():
            self.ip = dest - 1
```

### 位元組碼生成

```python
# bytecode_gen.py - 簡單的位元組碼生成器

class BytecodeGen:
    def __init__(self):
        self.bytecode = []
        self.labels = {}

    def emit(self, op, *args):
        self.bytecode.append((op, *args))
        return len(self.bytecode) - 1

    def iconst(self, value):
        return self.emit('ICONST', value)

    def iadd(self):
        return self.emit('IADD')

    def isub(self):
        return self.emit('ISUB')

    def imul(self):
        return self.emit('IMUL')

    def ilt(self):
        return self.emit('ILT')

    def br(self, label):
        return self.emit('BR', label)

    def brt(self, label):
        return self.emit('BRT', label)

    def brf(self, label):
        return self.emit('BRF', label)

    def label(self, name):
        self.labels[name] = len(self.bytecode)

    def load(self, idx):
        return self.emit('LOAD', idx)

    def store(self, idx):
        return self.emit('STORE', idx)

    def halt(self):
        return self.emit('HALT')

# 示例：生成計算 10! 的位元組碼
def gen_factorial():
    gen = BytecodeGen()

    gen.iconst(1)       # 結果初始化為 1
    gen.store(0)        # 存入 local[0]
    gen.iconst(1)       # i = 1
    gen.store(1)        # 存入 local[1]

    gen.label('loop')
    gen.load(1)         # 載入 i
    gen.iconst(10)      # 載入 10
    gen.ilt()           # i < 10 ?
    gen.brf('end')      # 若 false，跳到 end
    gen.load(0)         # 載入 result
    gen.load(1)         # 載入 i
    gen.imul()          # result * i
    gen.store(0)        # 存回 result
    gen.load(1)         # 載入 i
    gen.iconst(1)       # 載入 1
    gen.iadd()          # i + 1
    gen.store(1)        # 存回 i
    gen.br('loop')      # 跳回 loop

    gen.label('end')
    gen.load(0)         # 載入 result
    gen.halt()          # 結束

    return gen.bytecode
```

## 並發範例

### 互斥鎖示例

```python
# mutex_demo.py - 互斥鎖實現和使用

import threading

class SimpleMutex:
    def __init__(self):
        self.locked = False
        self.thread = None

    def acquire(self):
        thread = threading.current_thread()
        while self.locked and self.thread != thread:
            # 忙等待（實際應該用條件變數）
            pass
        self.locked = True
        self.thread = thread

    def release(self):
        self.locked = False
        self.thread = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *args):
        self.release()
```

### 生產者消費者問題

```python
# producer_consumer.py - 經典的同步問題

import threading
import time
import random

class Buffer:
    def __init__(self, size=10):
        self.size = size
        self.buffer = []
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def produce(self, item):
        with self.not_full:
            while len(self.buffer) >= self.size:
                self.not_full.wait()
            self.buffer.append(item)
            print(f"Produced: {item}")
            self.not_empty.notify()

    def consume(self):
        with self.not_empty:
            while not self.buffer:
                self.not_empty.wait()
            item = self.buffer.pop(0)
            print(f"Consumed: {item}")
            self.not_full.notify()
            return item

def producer(buffer, count):
    for i in range(count):
        time.sleep(random.random())
        buffer.produce(i)

def consumer(buffer, count):
    for _ in range(count):
        time.sleep(random.random())
        buffer.consume()
```

## 執行測試

請參考 `test.sh` 來執行各範例。

```bash
# 執行所有測試
cd _code
./test.sh

# 執行單一範例
python3 memory/simple_alloc.py
python3 vm/stack_vm.py
```

## 延伸閱讀

- [Google 搜尋：garbage collection algorithms](https://www.google.com/search?q=garbage+collection+algorithms)
- [Google 搜尋：JIT compiler implementation](https://www.google.com/search?q=JIT+compiler+implementation)
- [Google 搜尋：stack virtual machine implementation](https://www.google.com/search?q=stack+virtual+machine+implementation)