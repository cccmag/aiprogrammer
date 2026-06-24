# 二元搜尋樹操作

## 插入操作

插入新節點時，從根節點開始比較。如果新值小於當前節點值則往左走，大於則往右走，直到找到空位。這個過程與搜尋非常相似。

```python
def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.val:
        root.left = insert(root.left, key)
    elif key > root.val:
        root.right = insert(root.right, key)
    return root
```

時間複雜度：平均 O(log n)，最差 O(n)。插入操作總是發生在葉節點位置。

## 搜尋操作

從根節點開始，不斷比較目標值與當前節點值。每一步的比較都能排除大約一半的子樹，這就是 BST 搜尋效率的來源。

```python
def search(root, key):
    if root is None or root.val == key:
        return root
    if key < root.val:
        return search(root.left, key)
    return search(root.right, key)
```

## 刪除操作

刪除節點是 BST 中最複雜的操作，分為三種情況：

1. **葉節點**：直接刪除，設為 None。
2. **一個子節點**：用該子節點取代被刪除的節點。
3. **兩個子節點**：找到中序後繼者（inorder successor，即右子樹中最小的節點），用它的值取代被刪除節點的值，然後遞迴刪除中序後繼者。

```python
def delete(root, key):
    if root is None:
        return root
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        temp = min_value_node(root.right)
        root.val = temp.val
        root.right = delete(root.right, temp.val)
    return root
```

## 遍歷與驗證

對 BST 進行中序走訪（inorder traversal）會得到排序結果。如果走訪結果不是嚴格遞增的，就代表樹的結構有問題。

## 延伸閱讀

- https://www.google.com/search?q=binary+search+tree+insert+delete+search+Python
- https://www.google.com/search?q=BST+deletion+inorder+successor+三種情況
- https://www.google.com/search?q=二元搜尋樹+插入+刪除+搜尋+時間複雜度
