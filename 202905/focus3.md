# 人類偏好評估方法（2022-2029）

## 從 Elo 到人類反饋

### 前言

自動化指標無法捕捉「什麼是好的回答」——人類偏好評估因此成為 LLM 對齊的核心工具。

### Chatbot Arena：眾包偏好

LMSYS 的 Chatbot Arena 讓使用者對匿名模型輸出進行比較：

```python
# Elo 評分系統（簡化版）
class EloRating:
    def __init__(self, k=32):
        self.k = k
    def expected(self, ra, rb):
        return 1 / (1 + 10 ** ((rb - ra) / 400))
    def update(self, winner_elo, loser_elo):
        ew = self.expected(winner_elo, loser_elo)
        return winner_elo + self.k * (1 - ew), loser_elo + self.k * (0 - (1 - ew))
```

每場對戰相當於一次人類判斷，匯聚數十萬條比較後形成穩定排名。

### RLHF：從偏好到策略

人類反饋強化學習（RLHF）讓模型學會偏好：

```python
# RLHF 偏好模型訓練
def train_reward_model(preference_data):
    # preference_data: [(chosen, rejected), ...]
    model = RewardModel()
    for chosen, rejected in preference_data:
        r_chosen = model(chosen)
        r_rejected = model(rejected)
        loss = -torch.log(torch.sigmoid(r_chosen - r_rejected))
        loss.backward()
    return model
```

### 基於原則的評估

2024 年後，評估從「哪個更好？」轉向「是否符合原則？」：

```python
# 原則式評估
principles = {
    "有益": "回答是否對使用者有幫助？",
    "誠實": "回答是否準確且不誤導？",
    "無害": "回答是否可能造成傷害？",
}

def principle_eval(response):
    evaluations = {}
    for principle, criterion in principles.items():
        evaluations[principle] = judge_llm(
            f"根據以下標準評估回答：{criterion}\n\n回答：{response}"
        )
    return evaluations
```

### 人類 vs AI 審判員

2025 年後，AI 作為評審（LLM-as-a-Judge）越來越普遍：

```python
# AI Judge 與人類 Judge 的一致性
def judge_agreement(human_votes, ai_votes):
    from sklearn.metrics import cohen_kappa_score
    kappa = cohen_kappa_score(human_votes, ai_votes)
    if kappa > 0.8:
        print("AI Judge 可替代人類評分")
    else:
        print("需要人類介入")
```

### 小結

人類偏好評估從「相對比較」走向「原則對齊」，而 AI Judge 正在降低評估成本。

---

**下一步**：[對抗性測試與紅隊](focus4.md)

## 延伸閱讀

- [Chatbot Arena 介紹](https://www.google.com/search?q=Chatbot+Arena+LMSYS+Elo+rating)
- [RLHF 原理與實作](https://www.google.com/search?q=RLHF+reinforcement+learning+human+feedback)
- [LLM-as-a-Judge 研究](https://www.google.com/search?q=LLM+as+a+judge+evaluation+2024)
