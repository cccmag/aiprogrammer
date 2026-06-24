# 強化學習的實際應用進展

## 2021 年亮點

強化學習（RL）在 2021 年繼續從遊戲走向實際應用。

## DeepMind 的 MuZero

MuZero 能夠在未知環境中自學，達到超人表現：
- 學習多個 Atari 遊戲
- 在圍棋、象棋上超越人類冠軍
- 無需事先了解遊戲規則

## AlphaFold2 的 RL 元素

AlphaFold2 使用了強化學習思想進行結構優化，展示了 RL 在科學發現中的潛力。

## 機器人控制

2021 年 RL 在機器人控制方面取得實際進展：
- 工廠自動化
- 物流倉儲
- 醫療輔助

## RLHF：人類回饋的強化學習

讓人類對模型輸出排序，用於訓練獎勵模型：

```python
# 獎勵模型
def reward_model(response):
    human_rating = get_human_rating(response)
    return human_rating
```

這是 InstructGPT 等模型的關鍵技術。

## 挑戰

-樣本效率低
- 獎勵函式設計困難
- 安全性考量

## 結論

強化學習正在走出實驗室，在實際應用中展現價值，但仍有很長的路要走。