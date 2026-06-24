# 中間程式碼生成

## 從抽象到具體

經過前端分析後，編譯器擁有程式的結構化表示（AST）。但這個表示仍然太過抽象，不適合直接轉換為機器碼。中間程式碼生成（Intermediate Code Generation）的任務是將 AST 轉換為一種更接近機器碼、但平台無關的表示形式。

## 中間表示的形式

### 1. 三地址碼（Three-Address Code, TAC）

三地址碼是使用最廣泛的中間表示，每條指令最多包含三個地址（兩個運算元，一個結果）：

```
t1 = 4 * 2    # MUL t1, 4, 2
t2 = 3 + t1   # ADD t2, 3, t1
x  = t2       # STORE x, t2
```

常見的三地址碼指令包括：
- 算術指令：`ADD`, `SUB`, `MUL`, `DIV`
- 賦值指令：`STORE`, `LOAD`
- 控制流指令：`GOTO`, `IF_GOTO`
- 函式指令：`CALL`, `RETURN`

### 2. 靜態單賦值形式（SSA）

SSA（Static Single Assignment）是 TAC 的改良形式，要求每個變數只能被賦值一次。當變數在不同控制流路徑中被定義時，使用 Phi 函式合併：

```
entry:
  t1 = 4 * 2
  t2 = 3 + t1
  x  = t2
  if x > 0 goto L1 else goto L2
L1:
  y = x * 2
  goto L3
L2:
  y = x + 1
  goto L3
L3:
  z = phi(y1, y2)
```

SSA 簡化了許多最佳化演算法，因為每個變數只有一個定義點。

## AST 到三地址碼的轉換

從 AST 生成 TAC 的過程基本上是樹的走訪。以迷您編譯器為例：

```python
class CodeGen:
    def generate(self, ast):
        if ast.nodetype == 'BinOp':
            left_reg = self.generate(ast.left)
            right_reg = self.generate(ast.right)
            result = new_temp()
            self.emit(op_map[ast.op], result, left_reg, right_reg)
            return result
        elif ast.nodetype == 'Number':
            r = new_temp()
            self.emit('LOADI', r, ast.value)
            return r
```

## 控制流轉譯

控制流結構（if、while、for）需要特殊的處理：

```
if (x > 0) { y = 1; } else { y = 2; }

→

  if x <= 0 goto L1
  y = 1
  goto L2
L1:
  y = 2
L2:
  ...
```

## 中間表示的設計權衡

| 表示形式 | 抽象程度 | 最佳化效果 | 轉換難度 |
|---|---|---|---|
| AST | 高 | 較差 | 容易 |
| TAC | 中 | 良好 | 中等 |
| SSA | 中 | 極佳 | 較難 |
| 位元組碼 | 中偏低 | 中等 | 中等 |

## 本期實作

迷你編譯器的程式碼生成器使用類似三地址碼的形式。它遞迴走訪 AST，為每個子表達式產生暫存器，並發出具體的運算指令：

```
LOADI R0 3     # 載入常數 3 到 R0
LOADI R1 4     # 載入常數 4 到 R1
LOADI R2 2     # 載入常數 2 到 R2
MUL   R3 R1 R2 # R3 = R1 * R2
ADD   R4 R0 R3 # R4 = R0 + R3
STORE x R4     # 儲存 R4 到 x
```

## 延伸閱讀

- [三地址碼](https://www.google.com/search?q=three+address+code+compiler)
- [靜態單賦值 SSA](https://www.google.com/search?q=static+single+assignment+SSA+form)
- [中間表示設計](https://www.google.com/search?q=intermediate+representation+compiler+design)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列之五。*
