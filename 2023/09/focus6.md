# 控制流程與 Continuation

## 程式的執行順序

### 控制流程的抽象

控制流程決定了程式的執行順序。從基本的順序執行、條件分支和迴圈，到進階的例外處理、協程和非同步——控制流程抽象是程式語言演化的重要維度。

### Continuation 的概念

**Continuation** 是「剩下的計算」——在某個時間點之後要繼續執行什麼。每個程式點都隱含了一個 continuation：

```python
# 在 + 之前，continuation = 列印結果並結束
result = 1 + 2
print(result)
```

Continuation 可以被視為「計算的未來」——將 continuation 明確化可以實現非區域性的控制流轉移。

### CPS（Continuation-Passing Style）

CPS 是 continuation 的顯式表示：每個函數都接受一個額外的參數（continuation），並在計算完成後呼叫它：

```python
# 直接風格
def add(a, b): return a + b

# CPS 風格
def add_cps(a, b, cont): cont(a + b)

# 使用
add_cps(3, 4, lambda r: print(r))  # 7
```

### Call/CC（Call with Current Continuation）

Scheme 語言的 `call/cc` 是 continuation 的經典展現——它捕捉當前的 continuation 作為一個可呼叫的物件：

```python
# Scheme 偽代碼表示
# (call/cc (lambda (k) (k 42)))  → 42
# k 是當前的 continuation，呼叫 k 會跳轉回 call/cc 的位置
```

`call/cc` 可以用來實作：
- **非區域性跳轉**：類似 goto
- **例外處理**：捕捉 continuation 作為錯誤處理器
- **協程**：透過儲存和恢復 continuation
- **回溯搜尋**：失敗時恢復到先前的狀態

### 從 continuation 到現代程式設計

Continuation 雖然在主流語言中不常見，但其思想影響深遠：

**例外處理**：`try/catch` 可視為受限的 continuation——`throw` 跳轉到 `catch` 定義的 continuation。

```python
try:
    result = risky_operation()
except Exception as e:
    # 這裡是 continuation（錯誤路徑）
    handle_error(e)
```

**協程與 async/await**：協程可視為可暫停的 continuation，`await` 暫停當前計算並儲存 continuation。

**Generator**：`yield` 儲存當前的 continuation，下次迭代時恢復。

### 控制流程的操作語意

控制流程的操作語意可以用 continuation 的形式化描述：

```
⟨E[call/cc f], ρ, κ⟩ → ⟨E[f v], ρ, κ'⟩
其中 v = λx. ⟨E[x], ρ, κ⟩ 且 κ' 被儲存在 v 中
```

### 延伸閱讀

- [Continuation 解釋](https://www.google.com/search?q=continuation+programming+concept)
- [CPS 轉換](https://www.google.com/search?q=continuation+passing+style)
- [call/cc 教學](https://www.google.com/search?q=call+with+current+continuation)

---

**下一篇**：[程式語意學](focus7.md)
