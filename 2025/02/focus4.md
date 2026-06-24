# 鏈結串列與樹

## 鏈結串列（Linked List）

鏈結串列由節點（Node）組成，每個節點包含資料和指向下一個節點的指標。與陣列不同，鏈結串列不要求連續記憶體空間。

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 建立鏈結串列 1 -> 2 -> 3
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
```

### 特性對比

| 操作 | 陣列 | 單向鏈結串列 |
|------|------|-------------|
| 索引存取 | O(1) | O(n) |
| 頭部插入 | O(n) | O(1) |
| 頭部刪除 | O(n) | O(1) |
| 任意位置插入 | O(n) | O(n) |

## 樹（Tree）

樹是一種非線性結構，由節點和邊組成。最常見的是二元樹（Binary Tree），每個節點最多有兩個子節點。

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
```

### 二元搜尋樹（BST）

二元搜尋樹的規則：
- 左子樹所有節點值 < 根節點值
- 右子樹所有節點值 > 根節點值
- 左右子樹也分別是 BST

```python
def search_bst(root, val):
    if not root or root.val == val:
        return root
    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)
```

## 參考資源

- https://www.google.com/search?q=linked+list+data+structure
- https://www.google.com/search?q=binary+search+tree+tutorial
- https://www.google.com/search?q=Python+linked+list+implementation

## 小結

鏈結串列提供靈活的動態記憶體配置，樹結構則能高效組織層次資料。兩者都是進階資料結構的基礎。
