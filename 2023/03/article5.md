# AVL 樹旋轉

## 平衡因子與旋轉時機

AVL 樹的每個節點都記錄其子樹高度，平衡因子（Balance Factor, BF）= 左子樹高度 - 右子樹高度。當 |BF| > 1 時，需要執行旋轉操作來恢復平衡。

有四種不平衡情形，對應四種旋轉：

## 1. LL（左左）— 右旋

新節點插入在左子樹的左側，導致左子樹比右子樹高 2。解決方式是對不平衡節點執行右旋。

```
    10             5
   /              / \
  5       →      3   10
 /
3
```

## 2. RR（右右）— 左旋

新節點插入在右子樹的右側，導致右子樹比左子樹高 2。解決方式是對不平衡節點執行左旋。

```
  10               15
    \             /  \
     15    →     10   20
       \
        20
```

## 3. LR（左右）— 左右雙旋

新節點插入在左子樹的右側。先對左子樹執行左旋（變成 LL 情形），再對不平衡節點執行右旋。

```
    10             10              7
   /              /              / \
  5       →      7        →    5   10
   \            /
    7          5
```

## 4. RL（右左）— 右左雙旋

新節點插入在右子樹的左側。先對右子樹執行右旋（變成 RR 情形），再對不平衡節點執行左旋。

```
  10               10                15
    \                \              /  \
     20     →        15       →   10   20
    /                  \
   15                   20
```

## Python 實作

`_code/ds_theory.py` 中的 AVL 類別實作了完整的四種旋轉。`_insert` 方法在每次插入後更新節點高度、檢查平衡因子，並根據四種情形選擇對應的旋轉。關鍵程式碼如下：

```python
b = self._bf(n)
if b > 1 and key < n.left.key:       # LL
    return self._rr(n)
if b < -1 and key > n.right.key:     # RR
    return self._rl(n)
if b > 1 and key > n.left.key:       # LR
    n.left = self._rl(n.left)
    return self._rr(n)
if b < -1 and key < n.right.key:     # RL
    n.right = self._rr(n.right)
    return self._rl(n)
```

## 延伸閱讀

- https://www.google.com/search?q=AVL+tree+rotation+LL+RR+LR+RL+圖解
- https://www.google.com/search?q=AVL+tree+insertion+rotation+step+by+step
- https://www.google.com/search?q=AVL+平衡樹+旋轉+Python+實作+範例
