# 人類偏好評估與 Chatbot Arena

## 為什麼需要人類偏好評估？

自動化基準雖然方便，但無法捕捉人類對輸出品質的真實感受。Chatbot Arena 由 LMSYS 組織發起，透過匿名對戰方式收集人類偏好，目前已成為評估聊天機器人最重要平台之一。

## Chatbot Arena 運作機制

使用者對兩個匿名模型提問，投票選出較佳回答。透過 Bradley-Terry 模型計算 Elo 分數排名。

```python
import numpy as np
import pandas as pd

# 模擬 Elo 評分計算
class EloCalculator:
    def __init__(self, k=32):
        self.k = k
        self.ratings = {}

    def expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update(self, model_a, model_b, winner):
        if model_a not in self.ratings:
            self.ratings[model_a] = 1000
        if model_b not in self.ratings:
            self.ratings[model_b] = 1000

        ea = self.expected_score(self.ratings[model_a],
                                 self.ratings[model_b])
        eb = 1 - ea

        if winner == "A":
            sa, sb = 1, 0
        elif winner == "B":
            sa, sb = 0, 1
        else:
            sa, sb = 0.5, 0.5

        self.ratings[model_a] += self.k * (sa - ea)
        self.ratings[model_b] += self.k * (sb - eb)

elo = EloCalculator()
elo.update("GPT-4", "Claude-3", "A")
elo.update("GPT-4", "Gemini", "A")
elo.update("Claude-3", "Gemini", "A")
print(elo.ratings)
```

## 分析偏好資料

```python
import matplotlib.pyplot as plt

# 繪製勝率矩陣
def plot_win_matrix(win_rates, models):
    plt.figure(figsize=(8, 6))
    plt.imshow(win_rates, cmap="RdYlGn", vmin=0, vmax=1)
    plt.xticks(range(len(models)), models, rotation=45)
    plt.yticks(range(len(models)), models)
    plt.colorbar(label="Win Rate")
    plt.title("模型對戰勝率矩陣")
    plt.tight_layout()
    plt.show()
```

## 偏好評估的挑戰

- **成本高昂**：需要大量人類標註員
- **偏差問題**：標註員偏好可能不一致
- **時間變化**：使用者偏好隨時間改變

## 結語

Google 搜尋「Chatbot Arena Leaderboard」可查看即時排名。人類偏好評估與自動化基準相輔相成，共同構建完整的模型評估體系。
