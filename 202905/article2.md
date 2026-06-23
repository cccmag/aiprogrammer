# 人類偏好評估與 Chatbot Arena

## 1. 為什麼需要人類評估

自動化指標如 BLEU、ROUGE 難以捕捉生成品質的主觀面向。人類評估直接反映使用者體驗，尤其在開放式任務中不可或缺。

## 2. Chatbot Arena 運作原理

LMSYS Org 推出的 Chatbot Arena 採用匿名隨機配對比較。使用者與兩個模型對話後投票選出較佳者，透過 Elo 評分系統計算排名。

```python
def update_elo(winner_elo, loser_elo, k=32):
    expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_lose = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))
    return winner_elo + k * (1 - expected_win), loser_elo + k * (0 - expected_lose)
```

## 3. 評估維度設計

人類評估需定義明確維度：幫助性（Helpfulness）、真實性（Honesty）、無害性（Harmlessness）。每個維度有獨立的評分量尺，避免評分者將主觀偏好混入單一分數。

```python
criteria = {
    "helpfulness": "模型是否有效解決使用者問題？",
    "honesty": "模型是否正確表達不確定的資訊？",
    "harmlessness": "模型是否避免生成有害內容？"
}
```

## 4. 評分者間一致性

人類評估的最大挑戰是主觀差異。使用 Cohen's Kappa 或 Krippendorff's Alpha 衡量評分者間一致性，確保評估結果可靠。

## 5. 自動化替代方案

LLM-as-a-Judge 方法使用 GPT-4 等模型代替人類評分，成本低且可擴展。但存在位置偏差、冗長偏差等問題，需透過交換順序、校準等方式緩解。

## 6. 結語

人類偏好評估是模型對齊的核心環節。Chatbot Arena 開創了大規模社群驅動評估模式，而 LLM-as-a-Judge 則提供可擴展的替代方案。兩者相輔相成，構成完整的評估體系。

- https://www.google.com/search?q=Chatbot+Arena+LMSYS+Elo+rating
- https://www.google.com/search?q=LLM+as+a+judge+evaluation+method
