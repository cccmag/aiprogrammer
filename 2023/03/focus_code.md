# 本月程式碼說明

本月的程式碼集中在 `_code/ds_theory.py`，這是一個完整的 Python 腳本，內含四種經典資料結構的實作：二元搜尋樹（BST）、AVL 平衡樹、圖走訪（BFS/DFS）與雜湊表。每種資料結構都提供清晰的 API 與完整的操作，適合學習與參考。

## 二元搜尋樹（BST）

`BST` 類別實作了二元搜尋樹的核心操作：插入（insert）、搜尋（search）與中序走訪（inorder）。中序走訪會傳回排序結果，可用來驗證樹的正確性。

```python
bst = BST()
for k in [5, 3, 7, 2, 4, 8]:
    bst.insert(k)
print(bst.inorder())  # [2, 3, 4, 5, 7, 8]
print(bst.search(4))  # <BSTNode object>
print(bst.search(9))  # None
```

## AVL 平衡樹

`AVL` 類別示範了 AVL 樹的完整實作，包含右旋（_rr）、左旋（_rl）、左右雙旋與右左雙旋。每次插入後自動檢查平衡因子的絕對值是否超過 1，必要時執行對應的旋轉來維持樹的平衡。

```python
avl = AVL()
for k in [10, 20, 30, 40, 50, 25]:
    avl.insert(k)
print(avl.inorder())  # [10, 20, 25, 30, 40, 50]
```

## 圖走訪（BFS / DFS）

`Graph` 類別以鄰接串列（adjacency list）儲存無向圖，並提供廣度優先（bfs）與深度優先（dfs）兩種走訪方法。

```python
g = Graph()
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(2, 4)
print(g.bfs(1))  # [1, 2, 3, 4]
print(g.dfs(1))  # [1, 2, 4, 3]
```

## 雜湊表

`HashTable` 類別使用鏈結法（chaining）處理碰撞，每個陣列位置維護一個串列來儲存多個鍵值對。實作了 insert、get 與 remove 三種基本操作。

```python
ht = HashTable()
ht.insert("name", "Alice")
ht.insert("age", 30)
print(ht.get("name"))   # "Alice"
ht.remove("age")
print(ht.get("age"))    # None
```

## 執行方式

```bash
cd _code
python3 ds_theory.py
```

或直接執行測試腳本：`cd _code && bash test.sh`。執行後會依序展示 BST 中序走訪、AVL 平衡結果、圖的 BFS/DFS 走訪順序以及雜湊表的基本操作，完整驗證每個資料結構的正確性。
