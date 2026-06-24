# 基本區塊與流程圖

## 前言

基本區塊（Basic Block）和流程圖（Control Flow Graph, CFG）是編譯器中端優化的基礎。透過將程式劃分為基本區塊並建構控制流關係，編譯器可以進行更精確的分析和更有效的最佳化。

## 基本區塊的定義

基本區塊是滿足以下條件的連續指令序列：

1. **單一入口**：只能從第一條指令進入
2. **單一出口**：只能從最後一條指令離開
3. **內部無分支**：區塊內沒有跳轉指令

### 範例

```
原始碼：
x := 3 + 4 * 2;
if x > 0 then
    y := x;
else
    y := 0;

基本區塊：
Block 1:
    LOADI R0 3
    LOADI R1 4
    LOADI R2 2
    MUL R3 R1 R2
    ADD R4 R0 R3
    STORE x R4
    IF x > 0 GOTO Block2
    GOTO Block3

Block 2:
    LOAD R5 x
    STORE y R5
    GOTO Block4

Block 3:
    LOADI R6 0
    STORE y R6

Block 4:
    ...
```

## 基本區塊的劃分

演算法：掃描指令序列，尋找前導指令（Leader）：

```python
def find_basic_blocks(instructions):
    # 步驟 1：找到所有前導指令
    leaders = set()
    leaders.add(0)  # 第一條指令
    
    for i, instr in enumerate(instructions):
        if instr.op in ('GOTO', 'IF_GOTO'):
            # 跳轉目標是前導指令
            leaders.add(instr.target)
            # 跳轉的下一条是前導指令
            if i + 1 < len(instructions):
                leaders.add(i + 1)
    
    # 步驟 2：劃分基本區塊
    blocks = []
    leaders = sorted(leaders)
    
    for i, start in enumerate(leaders):
        end = leaders[i + 1] if i + 1 < len(leaders) else len(instructions)
        blocks.append(instructions[start:end])
    
    return blocks
```

## 控制流程圖（CFG）

CFG 以基本區塊為節點，控制流邊為邊：

```
        [Block 1: Entry]
              |
              v
        [Block 2: cond]
         /           \
        v             v
   [Block 3]      [Block 4]
        \             /
         \           /
          v         v
        [Block 5: Exit]
```

### CFG 建構

```python
class CFGNode:
    def __init__(self, block, name):
        self.block = block
        self.name = name
        self.preds = []    # 前驅節點
        self.succs = []    # 後繼節點

def build_cfg(blocks):
    nodes = [CFGNode(block, f'B{i}') for i, block in enumerate(blocks)]
    
    for i, node in enumerate(nodes):
        last_instr = node.block[-1] if node.block else None
        
        if not last_instr:
            # 直落到下一個區塊
            if i + 1 < len(nodes):
                add_edge(node, nodes[i + 1])
        elif last_instr.op == 'GOTO':
            # 無條件跳轉
            target = find_block_by_label(nodes, last_instr.target)
            add_edge(node, target)
        elif last_instr.op == 'IF_GOTO':
            # 條件跳轉：真分支
            target = find_block_by_label(nodes, last_instr.target)
            add_edge(node, target)
            # 假分支：直落
            if i + 1 < len(nodes):
                add_edge(node, nodes[i + 1])
        else:
            # 非跳轉指令，直落
            if i + 1 < len(nodes):
                add_edge(node, nodes[i + 1])
    
    return nodes
```

## CFG 的應用

### 1. 活躍變數分析

```python
def liveness_analysis(cfg):
    changed = True
    while changed:
        changed = False
        for node in reversed(cfg):  # 反向走訪
            old_in = node.live_in.copy()
            
            node.live_out = set()
            for succ in node.succs:
                node.live_out |= succ.live_in
            
            node.live_in = (node.live_out - node.def_set) | node.use_set
            
            if node.live_in != old_in:
                changed = True
```

### 2. 可達性分析

確認哪些基本區塊可以從入口到達，哪些是死區塊：

```python
def reachable_blocks(cfg):
    visited = set()
    stack = [cfg[0]]  # 從入口開始
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(node.succs)
    
    return visited
```

### 3. 支配者分析

```python
def dominators(cfg):
    dom = {node: set(cfg) for node in cfg}
    dom[cfg[0]] = {cfg[0]}
    
    changed = True
    while changed:
        changed = False
        for node in cfg[1:]:
            new_dom = {node}
            if node.preds:
                intersect = set.intersection(
                    *(dom[p] for p in node.preds)
                )
                new_dom |= intersect
            if dom[node] != new_dom:
                dom[node] = new_dom
                changed = True
    
    return dom
```

## 結語

基本區塊和 CFG 是編譯器進行全域最佳化的基礎資料結構。從活躍變數分析到支配者樹，CFG 上的分析演算法構成了現代編譯器最佳化管線的核心。掌握這些概念是深入理解編譯器後端的第一步。

## 延伸閱讀

- [控制流分析](https://www.google.com/search?q=control+flow+analysis+compiler)
- [支配者樹理論](https://www.google.com/search?q=dominator+tree+compiler+optimization)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
