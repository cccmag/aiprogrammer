# 語意分析與型別檢查

## 從結構到意義

語法分析確認了程式的結構（語法樹），但結構正確不代表程式有意義。語意分析（Semantic Analysis）負責檢查程式的語意正確性，是編譯器前端的最後一個階段。

語意分析的主要任務：
1. **型別檢查**：確認運算元的型別相容
2. **變數宣告檢查**：確認所有變數都已宣告
3. **範圍解析**：將變數使用連接到其宣告
4. **控制流檢查**：確認 break/continue 在迴圈內

## 型別系統

型別系統（Type System）是語意分析的核心。它定義了型別之間的關係和轉換規則。

### 靜態型別 vs 動態型別

- **靜態型別**：在編譯期檢查型別，如 C、Java、Rust
- **動態型別**：在執行期檢查型別，如 Python、JavaScript

### 強型別 vs 弱型別

- **強型別**：不允許隱式型別轉換，如 Rust、Haskell
- **弱型別**：允許隱式型別轉換，如 C（int 轉 float）

### 型別檢查的策略

**1. 推斷型別檢查**：編譯器自動推斷表達式的型別

```python
# 在簡單的型別系統中
# 3 + 4 → 推斷為 int
# x := 3 → x 的型別為 int
```

**2. 宣告型別檢查**：需要開發者明確宣告型別

```c
int x;   // 宣告型別
x = 42;  // 檢查賦值型別相容
```

**3. 結構化型別檢查**：檢查複合型別的結構匹配

## 符號表

符號表（Symbol Table）是編譯器儲存識別字資訊的資料結構。每個條目通常包含：

- 名稱（Name）
- 型別（Type）
- 範圍（Scope）
- 記憶體位置（Offset/Address）
- 其他屬性（常數、靜態等）

### 範圍管理

符號表需要支援巢狀範圍：

```python
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # 巢狀範圍堆疊
    
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        self.scopes.pop()
    
    def declare(self, name, typeinfo):
        self.scopes[-1][name] = typeinfo
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
```

## 語意分析實作

在我們的迷你編譯器中，語意分析在解析過程中自然完成。例如在處理賦值語句時，解析器確保等號左邊是識別字而非表達式。一個更完整的型別檢查實作如下：

```python
class TypeChecker:
    def check_assign(self, node):
        target_type = self.symbols.lookup(node.name)
        value_type = self.check_expr(node.value)
        if target_type != value_type:
            raise TypeError(
                f"Cannot assign {value_type} to {target_type}"
            )
    
    def check_binop(self, node):
        left_type = self.check_expr(node.left)
        right_type = self.check_expr(node.right)
        if left_type != right_type:
            raise TypeError(
                f"Type mismatch: {left_type} vs {right_type}"
            )
        return left_type
```

## 常見的語意錯誤

1. **未宣告的變數**：使用未宣告的識別字
2. **型別不匹配**：如將字串賦值給整數變數
3. **重複宣告**：在同一範圍內重複宣告相同名稱
4. **不可達程式碼**：return 之後的陳述式
5. **無效的運算子運算元**：如結構體套用算術運算

## 延伸閱讀

- [型別系統理論](https://www.google.com/search?q=type+system+programming+languages)
- [符號表實作](https://www.google.com/search?q=symbol+table+compiler+implementation)
- [語意分析教學](https://www.google.com/search?q=semantic+analysis+compiler+tutorial)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列之四。*
