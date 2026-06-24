# 主題五：不可變性與資料結構

## 為什麼不可變性如此重要？

在命令式程式設計中，我們習慣了修改狀態：

```python
# 可變的方式
items = [1, 2, 3, 4, 5]
items.append(6)
items[0] = 10
# items 現在是 [10, 2, 3, 4, 5, 6]
```

這種方式直覺，但在並行環境中極為危險。當多個執行緒同時修改共享狀態時，會產生競爭條件（Race Condition）和資料競爭（Data Race）。

不可變性提供了一個優雅的解決方案：**如果資料永遠不變，就不需要鎖**。

## 函式式資料結構的原則

### 永不修改

函式式資料結構在創建後不可更改。任何「修改」操作都會返回一個新的資料結構。

```python
# Python 中的不可變列表（使用 tuple）
original = (1, 2, 3, 4, 5)
# 沒有 append 方法
# 沒有 __setitem__

# 需要修改時創建新 tuple
new = original + (6,)  # (1, 2, 3, 4, 5, 6)
```

### 結構共享

為了效率，函式式資料結構使用結構共享。當你「修改」一個不可變資料結構時，只需要複製路徑上的節點，其他節點可以共享。

```
原始結構 [1, 2, 3, 4, 5]:

    [*] -> [*] -> [*] -> [*] -> [*]
     1      2      3      4      5

新結構 [1, 2, 99, 4, 5]（修改第三個元素）:

    [*] -> [*] -> [*]
     1      2     99
           /         \
    [*] -> [*]    [*] -> [*]  (共享的其餘部分)
     3      4      4      5
```

## 持久化資料結構

**持久化（Persistent）**資料結構在修改時保留所有先前版本，並透過結構共享高效實現。

### Clojure 的持久化 Vector

Clojure 的 vector 是一個位向量索引樹（Bitmapped Vector Trie）：

```clojure
(def v1 [1 2 3 4 5])
(def v2 (assoc v1 2 99))

;; v1 仍然是 [1 2 3 4 5]
;; v2 是 [1 2 99 4 5]
;; 共享大部分節點
```

這種實現提供：
- **讀取**：O(log n)
- **更新**：O(log n)
- **不可變性**：完全保證
- **記憶體效率**：結構共享

### Haskell 的列表

Haskell 的列表是最簡單的函式式資料結構：

```haskell
-- 列表是不可變的
let original = [1, 2, 3, 4, 5]

-- 添加元素創建新列表
let added = 0 : original  -- [0, 1, 2, 3, 4, 5]

-- original 仍然是 [1, 2, 3, 4, 5]
```

列表的基本操作代價：

| 操作 | 時間複雜度 |
|------|-----------|
| head | O(1) |
| tail | O(1) |
| cons | O(1) |
| append | O(n) |
| index | O(n) |

## 不可變映射與集合

### Scala 的不可變集合

```scala
// 不可變 Map
val m1 = Map("a" -> 1, "b" -> 2, "c" -> 3)
val m2 = m1 + ("d" -> 4)    // 新增元素
val m3 = m2 - "a"           // 移除元素
val m4 = m3 updated ("b", 99)  // 更新元素

// 所有操作返回新 Map，原始 Map 不變
```

### Clojure 的不可變集合

```clojure
;; Map
(def m {:a 1 :b 2 :c 3})
(def m2 (assoc m :d 4))    ;; 新增
(def m3 (dissoc m :a))      ;; 移除

;; Set
(def s #{1 2 3 4 5})
(def s2 (conj s 6))         ;; 新增
(def s3 (disj s 3))         ;; 移除
```

## 設計模式：事件溯源

不可變性催生了一種稱為**事件溯源（Event Sourcing）**的設計模式：

```
應用程式不儲存當前狀態，而是儲存狀態變更的歷史。

狀態 = 初始狀態 + 所有事件

每次變更都是一個新事件，永不修改過去。
```

```python
# 事件溯源示例
class EventStore:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)

    def get_state(self):
        state = {}
        for event in self.events:
            state = apply_event(state, event)
        return state

# 事件是不可變的資料類
@dataclass(frozen=True)
class AccountCreated:
    account_id: str
    owner: str

@dataclass(frozen=True)
class Deposit:
    account_id: str
    amount: Decimal
```

## Copy-on-Write

**Copy-on-Write（COW）**是一種實現不可變資料結構的策略：

- 讀取：直接讀取，無需複製
- 寫入：先複製，寫入副本，原資料不變

Python 的 `frozendict` 或第三方庫如 `immutables` 提供了 COW 實現：

```python
from immutables import Map

m = Map({"a": 1, "b": 2})
m2 = m.set("c", 3)  # m 不變，m2 是新 Map
```

## React 與不可變性

前端框架 React 大量使用不可變性來最佳化渲染：

```javascript
// React 中，狀態更新應該是不可變的
// 錯誤的方式
this.state.items.push(newItem);

// 正確的方式
this.setState({
    items: [...this.state.items, newItem]
});
```

不可變性允許 React 使用浅比较（shallow compare）來判斷是否需要重新渲染，大幅提升效能。

## Redux 與純函式 Reducer

Redux 的核心是純函式 reducer：

```javascript
// Reducer 永遠返回新狀態，不修改原狀態
function reducer(state = initialState, action) {
    switch (action.type) {
        case 'ADD_ITEM':
            return {
                ...state,
                items: [...state.items, action.payload]
            };
        case 'REMOVE_ITEM':
            return {
                ...state,
                items: state.items.filter(item => item.id !== action.payload)
            };
        default:
            return state;
    }
}
```

## 小結

不可變性是函式式程式設計的基石。它簡化了並發處理、提升了程式可推斷性、使得除錯更加容易。

雖然不可變資料結構在修改時需要分配新記憶體，但現代實現透過結構共享和持久化技術，已經將成本降到可接受範圍。

下一篇文章中，我們將探討高階函式與閉包——函式作為一等公民的威力。