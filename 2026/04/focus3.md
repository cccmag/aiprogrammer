# 編譯器理論的黃金時代：詞法分析、語法分析與語義分析（1960s-1970s）

## 形式語言的理論基礎

1960 年代，編譯器設計從一門手工藝發展為一門系統化的科學。這在很大程度上歸功於 Noam Chomsky 的形式語言理論。

### Chomsky 層級

1956 年，語言學家 Noam Chomsky 提出了形式語言的四層級分類：

```
┌─────────────────────────────────────────────────────┐
│                 Chomsky 層級                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  類型 0：無限制文法（圖靈完備）                     │
│   └─ 可以表達任何可計算的語言                      │
│                                                     │
│  類型 1：上下文相關文法（Context-Sensitive）        │
│   └─ 比類型 0 嚴格，但仍有很強的表達力            │
│                                                     │
│  類型 2：上下文無關文法（Context-Free）             │
│   └─ 這是程式語言的基礎！                          │
│                                                     │
│  類型 3：正則文法（Regular）                       │
│   └─ 詞法分析的理論基礎                             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

編譯器中的兩個關鍵階段正好對應 Chomsky 層級的兩個層次：

- **詞法分析**：類型 3（正則文法）——識別 token
- **語法分析**：類型 2（上下文無關文法）——建立語法樹

## 詞法分析：正則表達式與有限自動機

### 詞法分析的角色

詞法分析器（Lexer）是編譯器的第一個階段，它的工作是將原始碼字串轉換為 Token 序列：

```
原始碼："x = 42 + y;"

  │
  ▼

詞法分析器 (Lexer)

  │
  ▼

Token 序列：
  ID("x") ASSIGN NUMBER(42) PLUS ID("y") SEMI
```

### 正則表達式

詞法分析的模式可以使用正則表達式描述：

```
// 常見的詞法模式
數字    : [0-9]+
識別符號 : [a-zA-Z_][a-zA-Z0-9_]*
空白    : [ \t\n]+（忽略）
運算子  : + | - | * | /
```

### 有限自動機

這些正則表達式可以轉換為確定性有限自動機（DFA）：

```
┌─────────────────────────────────────────────────────┐
│              數字識別的 DFA                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│         ┌────────────────────────┐                 │
│         │                        │                 │
│         ▼                        │                 │
│    ┌────────┐    digit    ┌────────────┐           │
│    │   q0   │───────────►│    q1      │───┐       │
│    │ (開始) │             │ (接受狀態)  │   │       │
│    └────────┘             └────────────┘   │       │
│         │                      │          digit    │
│         │  non-digit           │                  │
│         ▼                      ▼                  │
│    ┌────────┐            ┌────────┐               │
│    │  error │            │  error │               │
│    └────────┘            └────────┘               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Lex：詞法分析器生成器

1975 年，Mike Lesk 和 Eric Schmidt 開發了 Lex——一個自動生成詞法分析器的工具：

```lex
/* Lex 範例：簡單的算術運算式詞法分析 */
%{
#include "tokens.h"
%}

%%
[0-9]+        { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z_]\w*  { yylval.id = strdup(yytext); return IDENTIFIER; }
[ \t\n]       ;  /* 忽略空白 */
"+"           { return PLUS; }
"-"           { return MINUS; }
"*"           { return TIMES; }
"/"           { return DIVIDE; }
"("           { return LPAREN; }
")"           { return RPAREN; }
.             { fprintf(stderr, "非法字元: %s\n", yytext); }
%%

int yywrap() { return 1; }
```

## 語法分析：剖析樹的建立

### 上下文無關文法與剖析樹

語法分析器（Parser）的工作是根據文法規則建立剖析樹（Parse Tree）：

```
文法規則：
  expr ::= expr "+" term | term
  term ::= term "*" factor | factor
  factor ::= NUMBER | "(" expr ")"

輸入："2 + 3 * 4"

剖析樹：
      expr
      /|\
     / | \
   expr + term
    |      /|\
   term  / | \
    |  term * factor
  factor |     |
    |   factor NUMBER(4)
  NUMBER  |
    |   NUMBER(3)
  NUMBER(2)
```

### 自上而下剖析（LL 剖析）

LL（Left-to-right, Leftmost derivation）剖析從起始符號開始，逐步推導出輸入：

```python
# LL(1) 剖析器的虛擬碼
def parse_expr():
    # expr ::= term expr'
    parse_term()
    parse_expr_tail()

def parse_expr_tail():
    if current_token == '+':
        advance()       # 消費 '+'
        parse_term()    # 解析右側
        parse_expr_tail()  # 繼續遞迴
    # else: epsilon（空產生式）

def parse_term():
    # term ::= factor term'
    parse_factor()
    parse_term_tail()

def parse_term_tail():
    if current_token == '*':
        advance()
        parse_factor()
        parse_term_tail()

def parse_factor():
    # factor ::= NUMBER | "(" expr ")"
    if current_token == NUMBER:
        advance()
    elif current_token == '(':
        advance()
        parse_expr()
        expect(')')
    else:
        error("預期數字或左括號")
```

### 自下而上剖析（LR 剖析）

LR（Left-to-right, Rightmost derivation）剖析從輸入開始，逐步歸約為起始符號：

```
LR 剖析的移位-歸約過程：

步驟 | 堆疊內容         | 輸入剩餘          | 動作
─────┼──────────────────┼──────────────────┼────────
  1  |                  | 2 + 3 * 4 $      | 移位
  2  | 2               | + 3 * 4 $        | 歸約 factor
  3  | factor          | + 3 * 4 $        | 歸約 term
  4  | term            | + 3 * 4 $        | 歸約 expr
  5  | expr            | + 3 * 4 $        | 移位
  6  | expr +          | 3 * 4 $          | 移位
  7  | expr + 3        | * 4 $            | 歸約 factor
  8  | expr + factor   | * 4 $            | 歸約 term
  9  | expr + term     | * 4 $            | 移位
 10  | expr + term *   | 4 $              | 移位
 11  | expr + term * 4 | $                | 歸約 factor
 12  | expr + term * factor | $           | 歸約 term
 13  | expr + term     | $                | 歸約 expr
 14  | expr            | $                | 接受
```

### Yacc：語法分析器生成器

1975 年，Stephen Johnson 在貝爾實驗室開發了 Yacc（Yet Another Compiler-Compiler）：

```yacc
/* Yacc 範例：簡單計算器 */
%{
#include <stdio.h>
int yylex();
void yyerror(const char *s) { fprintf(stderr, "%s\n", s); }
%}

%token NUMBER
%left '+' '-'
%left '*' '/'

%%
input   : /* empty */
        | input line
        ;

line    : expr '\n'      { printf("= %d\n", $1); }
        ;

expr    : expr '+' expr  { $$ = $1 + $3; }
        | expr '-' expr  { $$ = $1 - $3; }
        | expr '*' expr  { $$ = $1 * $3; }
        | expr '/' expr  {
            if ($3 == 0) yyerror("除以零");
            else $$ = $1 / $3;
        }
        | NUMBER         { $$ = $1; }
        | '(' expr ')'   { $$ = $2; }
        ;
%%

int main() { return yyparse(); }
```

### LL vs LR 對比

| 特性 | LL 剖析 | LR 剖析 |
|------|---------|---------|
| 方向 | 自上而下 | 自下而上 |
| 複雜度 | 較簡單 | 較複雜 |
| 文法限制 | LL(1) | LR(1)/LALR(1) |
| 表達力 | 有限 | 更強 |
| 錯誤報告 | 較好 | 較差 |
| 代表工具 | ANTLR, recursive descent | Yacc, Bison |

## 語義分析：符號表與型別檢查

語法分析之後，編譯器需要進行語義分析——確保程式的意義是合理的。

### 符號表

符號表（Symbol Table）是編譯器用來追蹤變數和函式資訊的資料結構：

```python
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # 作用域堆疊
    
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        self.scopes.pop()
    
    def define(self, name, info):
        self.scopes[-1][name] = info
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_current(self, name):
        return self.scopes[-1].get(name)

# 使用範例
st = SymbolTable()
st.define('x', {'type': 'int', 'line': 42})
st.define('func', {'type': 'function', 'params': ['int', 'int']})
st.enter_scope()    # 進入函式體
st.define('y', {'type': 'int', 'line': 44})
print(st.lookup('x'))  # 找到外層的 x
st.exit_scope()     # 離開函式體
```

### 型別檢查

型別檢查器驗證運算元的型別是否相容：

```python
# 型別檢查範例
def type_check(ast, st):
    if isinstance(ast, Number):
        return 'int'
    if isinstance(ast, BinOp):
        left_type = type_check(ast.left, st)
        right_type = type_check(ast.right, st)
        
        if left_type != right_type:
            raise TypeError(f"型別不匹配: {left_type} vs {right_type}")
        
        if ast.op in ('+', '-', '*', '/'):
            if left_type != 'int' and left_type != 'float':
                raise TypeError(f"數值運算需要數值型別，得到 {left_type}")
            return left_type
        
        if ast.op in ('==', '!=', '<', '>', '<=', '>='):
            return 'bool'
    
    if isinstance(ast, Var):
        info = st.lookup(ast.name)
        if info is None:
            raise NameError(f"未定義的變數: {ast.name}")
        return info['type']
    
    if isinstance(ast, Assign):
        var_type = st.lookup(ast.name)['type']
        expr_type = type_check(ast.expr, st)
        if var_type != expr_type:
            raise TypeError(f"賦值型別不匹配: {var_type} = {expr_type}")
        return var_type
    
    raise RuntimeError(f"未知的 AST 節點: {type(ast)}")
```

## Dragon Book：編譯器教育的里程碑

1977 年，Alfred Aho、Ravi Sethi 和 Jeffrey Ullman 出版了《Compilers: Principles, Techniques, and Tools》——俗稱 Dragon Book（龍書）。

```
┌─────────────────────────────────────────────────────┐
│            Dragon Book 封面                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│    ╔═══════════════════════════════════════╗        │
│    ║                                      ║        │
│    ║   Compilers: Principles,             ║        │
│    ║   Techniques, and Tools             ║        │
│    ║                                      ║        │
│    ║   ┌─────────────────────┐           ║        │
│    ║   │   🐉 龍與騎士        │           ║        │
│    ║   └─────────────────────┘           ║        │
│    ║                                      ║        │
│    ║   Aho, Sethi, Ullman                ║        │
│    ╚═══════════════════════════════════════╝        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

龍書的貢獻在於：

1. **系統化**：將編譯器設計的各個階段組織為清晰的框架
2. **理論實踐結合**：將形式語言理論與工程實踐結合
3. **教育價值**：成為數代計算機學生的標準教材

龍書提出了一個完整的編譯器架構，至今仍被廣泛使用：

```
原始碼 → 詞法分析 → 語法分析 → 語義分析 → 中間碼生成 → 最佳化 → 目標碼生成 → 機器碼
         └────────── 前端 ──────────┘  └─── 中端 ───┘  └─── 後端 ───┘
```

## 結語

1960-1970 年代是編譯器理論的黃金時代。形式語言理論為編譯器提供了堅實的數學基礎；Lex 和 Yacc 等工具使得編譯器開發從手工藝變成了工程實踐；Dragon Book 則將這些知識系統化，教育了無數程式設計師。

下一篇文章將探討 1970-1990 年代的編譯器最佳化技術——從區域最佳化到全域最佳化的演進。

---

## 延伸閱讀

- [Chomsky 形式語言](https://www.google.com/search?q=Chomsky+formal+languages+theory)
- [Lex & Yacc 教學](https://www.google.com/search?q=Lex+Yacc+tutorial)
- [Dragon Book (Aho, Sethi, Ullman)](https://www.google.com/search?q=Dragon+Book+compilers+principles+techniques+tools)

---

*本篇文章為「AI 程式人雜誌 2026 年 4 月號」歷史回顧系列之三。*
