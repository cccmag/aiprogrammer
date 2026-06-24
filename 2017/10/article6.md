# AlphaGo Zero 發布：從零學習的圍棋 AI

## 前言

2017 年 10 月，DeepMind 發布了 AlphaGo Zero，這是人工智慧領域的重大突破。不同於需要人類棋譜的 AlphaGo，AlphaGo Zero 從零開始，僅透過自我對弈學習，在 40 天內達到了超越所有先前版本的能力。

## AlphaGo Zero 的創新

### 從零開始

```
┌─────────────────────────────────────────────────────────┐
│         AlphaGo 版本對比                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  版本           訓練方式              實力水平          │
│  ───────────────────────────────────────────────────   │
│  AlphaGo Fan    人類棋譜 + 深度學習  業餘高手           │
│  AlphaGo Lee   人類棋譜              職業水平           │
│  AlphaGo Master 人類棋譜              世界冠軍           │
│  AlphaGo Zero  純自我對弈             超人類             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 技術架構

AlphaGo Zero 採用了創新的神經網路架構：

```python
# AlphaGo Zero 的核心思想
class AlphaZeroNetwork(nn.Module):
    def __init__(self):
        self.body = residual_blocks(40)  # 40 個殘差塊
        # 策略頭：輸出每個動作的機率
        self.policy_head = nn.Conv2d(256, 2, 1)
        # 價值頭：輸出局面評估
        self.value_head = nn.Conv2d(256, 1, 1)

    def forward(self, x):
        features = self.body(x)
        policy = self.policy_head(features)
        value = self.value_head(features)
        return policy, value
```

### 蒙特卡羅樹搜索 (MCTS)

```python
class MCTS:
    def search(self, position, network, simulations=1600):
        """
        AlphaGo Zero 的 MCTS 搜尋
        結合神經網路評估和快速模擬
        """
        for _ in range(simulations):
            self.simulate(position, network)

        # 返回最高訪問次數的動作
        return self.best_move()
```

## 為什麼重要？

### 1. 樣本效率

- AlphaGo Lee 使用了數百萬個人類棋譜
- AlphaGo Zero 完全不需要人類知識
- 這證明了即使沒有人類資料，AI 也能達到超人類水平

### 2. 泛化能力

- AlphaGo Zero 的方法可以推廣到其他領域
- 這個想法後來被應用於 AlphaZero
- 通用遊戲 AI 的先驅

### 3. 科學價值

- 展示了自我強化學習的潛力
- 為通用人工智慧研究提供新思路

## 對 AI 領域的影響

```python
# AlphaZero 的通用化
# 2017 年 12 月，DeepMind 發布了 AlphaZero
# 可以下圍棋、國際象棋、將棋

alphazero_results = {
    "圍棋": "超越 AlphaGo Zero",
    "象棋": "超越 Stockfish",
    "將棋": "超越 Elmo"
}
```

## 結語

AlphaGo Zero 的發布標誌著 AI 研究的一個重要里程碑。它不僅在圍棋領域達到了前所未有的水平，更重要的是展示了純粹自我學習的潛力。這種「從零開始」的學習範式對未來的 AI 研究產生了深遠影響。

---

**延伸閱讀**

- [AlphaGo Zero Paper](https://www.google.com/search?q=AlphaGo+Zero+Silver+2017)
- [DeepMind AlphaGo Page](https://www.google.com/search?q=DeepMind+AlphaGo)
- [Reinforcement Learning from Scratch](https://www.google.com/search?q=reinforcement+learning+from+scratch)

---

*本篇文章為「AI 程式人雜誌 2017 年 10 月號」AI 相關文章之一。*