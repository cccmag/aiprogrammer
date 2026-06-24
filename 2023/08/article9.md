# 暫存器分配

## 前言

暫存器分配（Register Allocation）是編譯器後端最關鍵的任務之一。現代處理器的暫存器數量有限（通常 16-32 個通用暫存器），而編譯器在中間表示中可能使用成千上萬的虛擬暫存器。如何將這些虛擬暫存器有效地映射到有限的實體暫存器，直接決定了生成程式碼的效能。

## 問題的定義

暫存器分配可以描述為：給定一組虛擬暫存器及其活躍區間（Live Range），找出一個映射關係 f，將虛擬暫存器分配到有限的實體暫存器，使得活躍區間重疊的虛擬暫存器分配到不同的實體暫存器。

## 圖著色演算法

### 1. 建構干擾圖

干擾圖（Interference Graph）的節點是虛擬暫存器，邊表示兩個暫存器的活躍區間重疊，不能共用同一實體暫存器。

```python
class InterferenceGraph:
    def __init__(self):
        self.nodes = {}  # virtual_reg → Node
    
    def add_interference(self, vreg1, vreg2):
        if vreg1 not in self.nodes:
            self.nodes[vreg1] = set()
        if vreg2 not in self.nodes:
            self.nodes[vreg2] = set()
        self.nodes[vreg1].add(vreg2)
        self.nodes[vreg2].add(vreg1)
```

### 2. 干擾檢測

根據活躍變數分析的結果建構干擾關係：

```python
def build_interference(cfg):
    graph = InterferenceGraph()
    
    for block in cfg:
        live = block.live_out.copy()
        for instr in reversed(block.instructions):
            if instr.defines:
                # 定義的變數與所有活躍變數干擾
                defined = instr.defines
                for v in live:
                    if v != defined:
                        graph.add_interference(defined, v)
                live.discard(defined)
            live.update(instr.uses)
    
    return graph
```

### 3. 著色

使用「簡化數」K（實體暫存器數量）來著色：

```python
def color_graph(graph, num_registers):
    stack = []
    nodes = {v: set(n) for v, n in graph.nodes.items()}
    
    # 簡化階段
    while nodes:
        # 找度數小於 K 的節點
        node = find_low_degree(nodes, num_registers)
        if node:
            stack.append(('color', node))
            # 移除節點並減少鄰居度數
            neighbors = nodes.pop(node)
            for n in neighbors:
                if n in nodes:
                    nodes[n].discard(node)
        else:
            # 需要溢出（Spill）
            node = heuristic_spill(nodes)
            stack.append(('spill', node))
            neighbors = nodes.pop(node)
            for n in neighbors:
                if n in nodes:
                    nodes[n].discard(node)
    
    # 分配階段
    colors = {}
    spilled = []
    while stack:
        action, node = stack.pop()
        if action == 'color':
            used = {colors[n] for n in graph.nodes[node] if n in colors}
            for c in range(num_registers):
                if c not in used:
                    colors[node] = c
                    break
        else:
            spilled.append(node)
    
    return colors, spilled
```

### 4. 溢出處理

溢出的虛擬暫存器需要儲存到記憶體：

```python
def handle_spill(spilled_regs, code):
    for vreg in spilled_regs:
        for i, instr in enumerate(code):
            if vreg in instr.uses:
                # 在使用前插入 LOAD 指令
                temp = new_virtual()
                code.insert(i, Instruction('LOAD', temp, f'spill_{vreg}'))
                # 替換原本的暫存器
                instr.replace_use(vreg, temp)
            if vreg in instr.defines:
                # 在定義後插入 STORE 指令
                temp = new_virtual()
                instr.replace_def(vreg, temp)
                code.insert(i+1, Instruction('STORE', f'spill_{vreg}', temp))
```

## 線性掃描演算法

線性掃描（Linear Scan）是一種更快的暫存器分配方法：

```python
def linear_scan(intervals, num_registers):
    """
    intervals: [(vreg, start, end), ...]
    """
    intervals.sort(key=lambda x: x[1])  # 按開始位置排序
    active = []
    allocation = {}
    free_regs = list(range(num_registers))
    
    for vreg, start, end in intervals:
        # 釋放已結束的暫存器
        active.sort(key=lambda x: x[2])
        while active and active[0][2] <= start:
            finished = active.pop(0)
            free_regs.append(allocation.pop(finished[0]))
        
        if free_regs:
            # 有空閒暫存器
            reg = free_regs.pop(0)
            allocation[vreg] = reg
            active.append((vreg, start, end))
        else:
            # 需要溢出
            spill_candidate = max(active, key=lambda x: x[2])
            if end > spill_candidate[2]:
                # 溢出最長的活躍區間
                allocation[spill_candidate[0]] = None  # 標記為溢出
                active.remove(spill_candidate)
                reg = allocation.pop(spill_candidate[0])
                allocation[vreg] = reg
                active.append((vreg, start, end))
            else:
                # 溢出現行暫存器
                allocation[vreg] = None
    
    return allocation
```

## 兩種演算法的比較

| 特性 | 圖著色 | 線性掃描 |
|---|---|---|
| 時間複雜度 | O(n²) 或更高 | O(n log n) |
| 分配品質 | 優良 | 良好 |
| 實作複雜度 | 高 | 中 |
| 適合場景 | 編譯時間不敏感 | JIT 編譯 |

## 結語

暫存器分配是編譯器後端最關鍵也最具挑戰性的部分。圖著色演算法雖然複雜但分配品質極佳，線性掃描則在編譯速度和分配品質間取得了良好平衡。理解這些演算法是開發高效編譯器的必備知識。

## 延伸閱讀

- [圖著色暫存器分配](https://www.google.com/search?q=graph+coloring+register+allocation+Chaitin)
- [線性掃描演算法](https://www.google.com/search?q=linear+scan+register+allocation+Poletto)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
