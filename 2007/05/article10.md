# Computer Go：AI 的遊戲挑戰

## 前言

圍棋被認為是 AI 領域最困難的遊戲之一，因為其巨大的搜索空間。

## 圍棋程式的挑戰

```
圍棋 vs 象棋：
───────────────────────────
象棋    評估節點數 ~10^44   可用 alpha-beta 修剪
圍棋    評估節點數 ~10^170  難以評估局面
```

## MCTS 的興起

2007 年，Monte Carlo Tree Search 開始被應用於圍棋：

```python
# MCTS 基本概念
def monte_carlo_tree_search(root):
    for _ in range(iterations):
        node = select(root)
        result = simulate(node)
        backpropagate(node, result)
    return best_child(root)
```

## 結語

AlphaGo 在 2016 年的成功標誌著 Computer Go 問題的解決。

---

## 延伸閱讀

- [computer+go+AI+2007](https://www.google.com/search?q=computer+go+AI+2007)

---