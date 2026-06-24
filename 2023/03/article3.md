# 二元樹走訪：前、中、後序

## 走訪的種類

二元樹走訪（Binary Tree Traversal）分為深度優先（Depth-First Search, DFS）與廣度優先（Breadth-First Search, BFS）兩大類。深度優先包含前序（Pre-order）、中序（In-order）、後序（Post-order）三種。走訪順序的不同會影響處理節點的時機，選擇正確的走訪方式對解決特定問題至關重要。

## 前序走訪（Pre-order）

順序：根節點 → 左子樹 → 右子樹。在進入左右子樹之前先處理根節點。

**遞迴實作**：
```python
def preorder(node):
    if node:
        print(node.val)       # 先處理根節點
        preorder(node.left)   # 再走左子樹
        preorder(node.right)  # 最後走右子樹
```

前序走訪在複製整棵樹、輸出樹的結構或序列化二元樹時非常有用。前序走訪的第一個節點就是樹的根節點。

## 中序走訪（In-order）

順序：左子樹 → 根節點 → 右子樹。對二元搜尋樹（BST）進行中序走訪，會得到升序排列的結果，這是驗證 BST 正確性的標準方法。

```python
def inorder(node):
    if node:
        inorder(node.left)    # 先走左子樹
        print(node.val)       # 再處理根節點
        inorder(node.right)   # 最後走右子樹
```

中序走訪在運算式中也很有用，對表示式樹進行中序走訪可以得到中序表示法 (infix notation)。

## 後序走訪（Post-order）

順序：左子樹 → 右子樹 → 根節點。先處理子節點再處理父節點。

```python
def postorder(node):
    if node:
        postorder(node.left)   # 先走左子樹
        postorder(node.right)  # 再走右子樹
        print(node.val)        # 最後處理根節點
```

後序走訪常用於刪除整棵樹（先刪除子節點）、計算表示式樹的結果以及計算樹的高度。

## 迭代實作

遞迴實作雖然簡潔，但在樹很深時可能導致堆疊溢位（stack overflow）。迭代實作使用顯式的堆疊來模擬遞迴過程：

- **前序迭代**：先 push 右子節點再 push 左子節點，確保左子樹先被走訪。
- **中序迭代**：一直往左走到最底，過程中 push 入堆疊，pop 時處理該節點，再往右走。
- **後序迭代**：最複雜，可用雙堆疊法或 visited 標記。

## 延伸閱讀

- https://www.google.com/search?q=binary+tree+traversal+preorder+inorder+postorder+範例+圖解
- https://www.google.com/search?q=二元樹走訪+前序+中序+後序+遞迴+迭代+Python+實作
- https://www.google.com/search?q=tree+DFS+traversal+iterative+vs+recursive+stack+overflow
