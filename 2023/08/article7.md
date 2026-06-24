# 三地址碼

## 前言

三地址碼（Three-Address Code, TAC）是編譯器中最常用的中間表示之一。它的指令形式簡單，每條指令最多包含三個運算元位址，接近機器碼的結構但保持平台無關性。本文深入探討三地址碼的設計與生成。

## TAC 指令格式

三地址碼的指令通常以四元組（Quadruple）表示：

```
(op, arg1, arg2, result)
```

例如：
```
(ADD, a, b, t1)     # t1 = a + b
(MUL, t1, c, t2)   # t2 = t1 * c
(STORE, t2, _, x)  # x = t2
```

## 常見指令類型

### 算術指令

```
ADD  result left right   # result = left + right
SUB  result left right   # result = left - right
MUL  result left right   # result = left * right
DIV  result left right   # result = left / right
```

### 載入與儲存

```
LOADI result value       # result = value (載入常數)
LOAD  result variable    # result = variable (載入變數)
STORE variable source    # variable = source (儲存變數)
```

### 控制流

```
GOTO label               # 無條件跳轉
IF_GOTO cond label       # 如果 cond 為真則跳轉
LABEL label              # 標記位置
```

### 函式操作

```
CALL result func args    # result = func(args)
RETURN value             # 返回 value
PARAM value              # 傳遞參數
```

## 從 AST 生成 TAC

生成 TAC 的過程本質上是 AST 的走訪，為每個節點產生對應的指令：

```python
class TACGen:
    def __init__(self):
        self.temps = 0
        self.code = []
    
    def new_temp(self):
        self.temps += 1
        return f't{self.temps}'
    
    def emit(self, op, arg1, arg2, result):
        self.code.append((op, arg1, arg2, result))
    
    def gen(self, node):
        method = f'gen_{node.nodetype}'
        return getattr(self, method)(node)
    
    def gen_Number(self, node):
        result = self.new_temp()
        self.emit('LOADI', node.value, None, result)
        return result
    
    def gen_Ident(self, node):
        result = self.new_temp()
        self.emit('LOAD', node.name, None, result)
        return result
    
    def gen_BinOp(self, node):
        left = self.gen(node.left)
        right = self.gen(node.right)
        result = self.new_temp()
        op_map = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
        self.emit(op_map[node.op], left, right, result)
        return result
    
    def gen_Assign(self, node):
        value = self.gen(node.value)
        self.emit('STORE', node.name, value, None)
```

## 控制流的轉譯

### if-else 轉譯

```
if (x > 0) {
    y = 1;
} else {
    y = 2;
}

→ TAC:
    IF_GOTO x > 0, L1
    GOTO L2
L1:
    y = 1
    GOTO L3
L2:
    y = 2
L3:
    ...
```

### while 迴圈轉譯

```
while (x > 0) {
    x = x - 1;
}

→ TAC:
L1:
    IF_GOTO x > 0, L2
    GOTO L3
L2:
    x = x - 1
    GOTO L1
L3:
    ...
```

## TAC 的優化

TAC 適合進行多種編譯器最佳化：

1. **常數折疊**：`t1 = 2 * 3` → `t1 = 6`
2. **複製傳播**：`t1 = x; t2 = t1 + 1` → `t2 = x + 1`
3. **死碼消除**：移除從未被使用的暫存器
4. **公共子表達式消除**：避免重複計算

## 三地址碼 vs 其他 IR

| IR | 抽象程度 | 適用最佳化 | 轉換成本 |
|---|---|---|---|
| AST | 高 | 結構化 | 低 |
| TAC | 中 | 線性 | 低 |
| SSA | 中 | 極高 | 中 |
| 機器碼 | 低 | 目標相關 | 高 |

## 結語

三地址碼是編譯器中端處理的理想中間表示。它足夠抽象以保持平台無關，同時足夠具體以支援高效的最佳化。理解 TAC 的生成是掌握編譯器後端的基礎。

## 延伸閱讀

- [三地址碼格式](https://www.google.com/search?q=three+address+code+intermediate+representation)
- [SSA 與 TAC 比較](https://www.google.com/search?q=SSA+vs+three+address+code)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
