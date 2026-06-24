# DeepMind 的 AlphaZero 與 MuZero

## 前言

AlphaZero 和 MuZero 是 DeepMind 開發的通用棋類遊戲 AI，展示了從零學習的強大能力。

## AlphaZero

```python
"""
AlphaZero 特點：
────────────────────────────────

1. 從零學習
   └── 不使用人類遊戲記錄
   └── 完全通過自我對弈學習

2. 通用演算法
   └── 同一套程式適用於多種遊戲
   └── 圍棋、象棋、將棋

3. 神經網路 + MCTS
   └── Policy Network 預測下一步
   └── Value Network 預測勝率
```

## MuZero

```
MuZero 創新：
────────────────────────────────

在未知環境動力學的情況下學習規劃

應用場景：
-  Atari 遊戲（無需遊戲規則）
- 機器人控制
- 資源调度
```

## 延伸閱讀

- [AlphaZero 論文](https://www.google.com/search?q=AlphaZero+Science+2018+paper)
- [MuZero 論文](https://www.google.com/search?q=MuZero+Nature+2020+paper)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」文章集錦之一。*