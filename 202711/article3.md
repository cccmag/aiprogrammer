# RLHF 與模型對齊技術

## 1. 引言

模型對齊（Alignment）是確保 AI 系統行為符合人類意圖和價值觀的技術領域。目前最主流的方法是 RLHF（Reinforcement Learning from Human Feedback），但這個領域正在快速演化。

## 2. RLHF 的核心流程

RLHF 分為三個階段：

**監督式微調（SFT）**：用高品質示範資料對預訓練模型微調，讓模型學會對話格式與人類偏好的風格。

**偏好模型訓練**：收集人類對模型輸出的偏好比較（A > B），訓練獎勵模型來預測人類偏好：

```python
class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base = base_model
        self.reward_head = nn.Linear(768, 1)
    def forward(self, input_ids):
        hidden = self.base(input_ids).last_hidden_state
        return self.reward_head(hidden[:, -1, :])
# 對比損失：偏好回應的獎勵更高
loss = -torch.log(sigmoid(reward_chosen - reward_rejected)).mean()
```

**強化學習微調（PPO）**：使用獎勵模型作為訊號，透過 PPO 演算法微調模型：

```python
from trl import PPOTrainer
ppo_trainer = PPOTrainer(
    model=model, reward_model=reward_model,
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64)
)
for query in train_queries:
    reward = reward_model(query, model.generate(query))
    ppo_trainer.step(query, response, reward)
```

## 3. RLHF 的侷限性

**Reward Hacking**：模型學會最大化獎勵分數而非真正符合人類偏好。例如，獎勵模型偏好長回應，模型就學會寫冗長的回覆。

**資料效率**：RLHF 需要大量人類標註，成本極高。OpenAI 估計標註一個偏好資料集需要數百萬美元。

**分布偏移**：PPO 訓練中模型生成的樣本分布與獎勵模型訓練時的分布不同，導致獎勵模型不準確。

## 4. 新興對齊方法

### DPO（Direct Preference Optimization）

DPO 跳過獎勵模型訓練，直接在偏好資料上優化策略。數學上更優雅，實務上更穩定。

```python
# DPO 損失函數
def dpo_loss(policy_logps, ref_logps, beta=0.1):
    policy_diff = policy_logps["chosen"] - policy_logps["rejected"]
    ref_diff = ref_logps["chosen"] - ref_logps["rejected"]
    logits = beta * (policy_diff - ref_diff)
    return -F.logsigmoid(logits).mean()
```

### Constitutional AI

Anthropic 的 Constitutional AI 使用一組原則（憲法）引導模型自我修正，減少人類回饋的需求。

### 弱到強泛化（Weak-to-Strong Generalization）

OpenAI 的 superalignment 研究方向，用小模型監督大模型對齊，探索超越人類監督能力的對齊方法。

## 5. 結語

RLHF 是目前模型對齊的標準方法，但 DPO、Constitutional AI 等新方法正在挑戰其主導地位。對齊不是一次性任務——隨著模型能力增強，對齊技術也必須持續進化。

---

## 延伸閱讀

- [RLHF 原始論文](https://www.google.com/search?q=RLHF+InstructGPT+paper)
- [DPO 論文：Direct Preference Optimization](https://www.google.com/search?q=DPO+preference+optimization)
- [Anthropic Constitutional AI](https://www.google.com/search?q=Constitutional+AI+Anthropic)
- [TRL 函式庫文件](https://www.google.com/search?q=HuggingFace+TRL+RLHF+training)
