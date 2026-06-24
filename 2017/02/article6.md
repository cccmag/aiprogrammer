# AlphaGo 對決柯洁：世紀大戰

## 前言

2017 年 5 月，AlphaGo 與世界排名第一的柯洁九段在浙江烏鎮進行了三番棋對決。這是人工智慧圍棋領域最受關注的比賽，也是對深度強化學習技術的重要檢驗。

## 比賽背景

### 為什麼是柯洁？

柯洁是世界排名第一的圍棋棋手，當時保持對人類頂尖棋手的高勝率。選擇他作為對手，是為了測試 AlphaGo 的極限能力。

### 技術進步

相比 2016 年戰勝李世乭的版本，AlphaGo 經過了半年多的改進：

```
AlphaGo Fan (2015) → AlphaGo Lee (2016) → AlphaGo Master (2017) → AlphaGo Zero (2017年末)
```

## 比賽結果

```
2017 年 5 月 23-27 日：烏鎮
結果：AlphaGo 3:0 戰勝柯洁

第1局：AlphaGo 執白中盤勝
第2局：柯洁 執白中盤負
第3局：AlphaGo 執白中盤勝
```

### 比賽看點

1. **第一局的激烈**：柯洁發揮出色，一度讓 AlphaGo 陷入苦戰
2. **第二局的突破**：柯洁採用了激進的策略，但未能動搖 AlphaGo
3. **第三局的從容**：AlphaGo 展現了完美的形勢判斷

## AlphaGo 的技術進步

### 新的網路架構

```python
# 假設的改進方向
improvements = {
    "policy_network": "更深的神經網路",
    "value_network": "更精確的局面評估",
    "mcts": "更高效的蒙地卡羅樹搜索",
    "training": "更多的自我對弈數據"
}
```

### 深度強化學習的進步

AlphaGo 的成功展示了深度強化學習的強大能力：

1. **策略網路**：學習人類高手的下法
2. **價值網路**：評估當前局面的勝率
3. **蒙地卡羅樹搜索**：結合兩者選擇最佳行動
4. **自我對弈**：通過強化學習持續改進

## 對圍棋界的影響

### 職業棋手的反應

```
「我從來沒有看到過這樣的下法...這是來自另一個世界的下法。」
—— 柯洁，賽後採訪
```

### 圍棋理論的革新

AlphaGo 帶來了新的圍棋觀念：
- 新型开局變化
- 中盤作戰新思路
- 對死活的重新認識

## 結語

AlphaGo 對決柯洁的比賽標誌著深度強化學習的重大突破。雖然 AlphaGo 最終以 3:0 取勝，但柯洁在第一局的表現證明了人類頂尖棋手仍然能夠給 AI 帶來挑戰。

---

## 延伸閱讀

- [AlphaGo+柯洁+2017+烏鎮](https://www.google.com/search?q=AlphaGo+Ke+Jie+2017+Wuzhen)
- [DeepMind+AlphaGo+技術](https://www.google.com/search?q=DeepMind+AlphaGo+Ke+Jie+match)
- [深度強化學習+圍棋](https://www.google.com/search?q=deep+reinforcement+learning+Go+AlphaGo)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」文章系列之一。*