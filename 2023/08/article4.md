# 抽象語法樹 AST

## 前言

抽象語法樹（Abstract Syntax Tree, AST）是編譯器內部表示程式結構的核心資料結構。與具體語法樹（Parse Tree）不同，AST 省略了僅用於語法分析的輔助節點，專注於程式語義的本質結構。

## AST vs Parse Tree

```
輸入：3 + 4 * 2

Parse Tree:
    expr
   / |  \
 expr +  term
  |      / | \
 term   term * factor
  |       |     |
 factor  factor 2
  |        |
  3        4

AST:
  BinOp(+)
   /    \
Number(3) BinOp(*)
           /    \
      Number(4) Number(2)
```

Parse Tree 包含所有語法資訊（如非終結符展開的層次），而 AST 只保留運算子和運算元。

## AST 節點設計

一個好的 AST 節點設計應該易於建構、走訪和擴充：

```python
class AST:
    def __init__(self, nodetype, **attrs):
        self.nodetype = nodetype
        self.__dict__.update(attrs)
    
    def __repr__(self):
        attrs = {k:v for k,v in self.__dict__.items() if k!='nodetype'}
        parts = [f'{k}={v!r}' for k,v in attrs.items()]
        return f'{self.nodetype}({", ".join(parts)})'
```

使用這種設計，我們可以動態建構任意節點：

```python
num = AST('Number', value=42)
ident = AST('Ident', name='x')
binop = AST('BinOp', op='+', left=num, right=ident)
assign = AST('Assign', name='y', value=binop)
```

## AST 走訪策略

### 遞迴走訪

最簡單的走訪方式是遞迴函式：

```python
def visit(node, depth=0):
    prefix = '  ' * depth
    print(f'{prefix}{node.nodetype}')
    
    if node.nodetype == 'Program':
        for stmt in node.stmts:
            visit(stmt, depth + 1)
    elif node.nodetype == 'Assign':
        print(f'{prefix}  name = {node.name}')
        visit(node.value, depth + 2)
    elif node.nodetype == 'BinOp':
        print(f'{prefix}  op = {node.op}')
        visit(node.left, depth + 2)
        visit(node.right, depth + 2)
    elif node.nodetype == 'Number':
        print(f'{prefix}  value = {node.value}')
    elif node.nodetype == 'Ident':
        print(f'{prefix}  name = {node.name}')
```

### 訪問者模式（Visitor Pattern）

更結構化的走訪方式是 Visitor 模式：

```python
class ASTVisitor:
    def visit(self, node, *args):
        method = f'visit_{node.nodetype}'
        if hasattr(self, method):
            return getattr(self, method)(node, *args)
        raise NotImplementedError(f'No visitor for {node.nodetype}')

class CodeGenerator(ASTVisitor):
    def visit_Program(self, node):
        for stmt in node.stmts:
            self.visit(stmt)
    
    def visit_Number(self, node):
        reg = new_temp()
        emit(f'LOADI {reg} {node.value}')
        return reg
    
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = new_temp()
        emit(f'{op_map[node.op]} {result} {left} {right}')
        return result
```

## AST 的建構時機

AST 通常在語法分析過程中建構。遞迴下降解析器在解析的同時產生 AST 節點：

```python
def parse_expr(self):
    left = self.parse_term()
    while self.peek() in ('+', '-'):
        op = self.consume()
        right = self.parse_term()
        left = AST('BinOp', op=op, left=left, right=right)
    return left
```

## AST 的其他用途

AST 不僅用於編譯，還廣泛應用於：

1. **Linter**：靜態分析程式碼風格和潛在錯誤
2. **Formatter**：重新格式化原始碼（如 Prettier、Black）
3. **Refactoring**：自動重構工具
4. **Code Generation**：從模板生成程式碼
5. **Transpilation**：語言到語言的轉換（TypeScript → JavaScript）

## 結語

AST 是編譯器最核心的資料結構。一個好的 AST 設計讓後續的最佳化和程式碼生成變得簡單。建議初學者從簡單的二元樹結構開始，逐步加入更多節點型別。

## 延伸閱讀

- [AST 走訪](https://www.google.com/search?q=abstract+syntax+tree+traversal+visitor+pattern)
- [AST 格式](https://www.google.com/search?q=AST+abstract+syntax+tree+JSON+format)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
