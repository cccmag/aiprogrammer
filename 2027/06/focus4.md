# 微調策略：SFT 與 RLHF（2020-2026）

## 監督式微調（SFT）

SFT 是將預訓練模型適應到特定任務的最直接方法。需要收集任務專屬的（輸入, 輸出）配對資料。

### SFT 資料格式

```python
# 指令微調資料範例 (JSONL)
{
    "instruction": "解釋什麼是注意力機制",
    "input": "",
    "output": "注意力機制是 Transformer 的核心..."
}

{
    "instruction": "將以下句子翻譯成英文",
    "input": "深度學習改變了世界",
    "output": "Deep learning changed the world."
}

{
    "instruction": "總結以下文章的關鍵論點",
    "input": "大型語言模型的研究近年取得巨大進展...",
    "output": "本文指出 LLM 在推理能力和...\n關鍵論點：1. ... 2. ..."
}
```

### 指令微調的最佳實踐

2024-2026 年的實務經驗總結：

| 策略 | 說明 | 效果 |
|------|------|------|
| **資料品質 >> 數量** | 幾千條手工撰寫的資料勝過百萬條自動生成 | 顯著 |
| **多樣性優先** | 涵蓋多種任務型態而非單一任務 | 通用性提升 |
| **格式一致性** | 統一的回覆格式與結構 | 可預測性 |
| **負面樣本** | 包含拒絕回答不適當問題的範例 | 安全性提升 |

## RLHF：強化學習來自人類反饋

RLHF（2020 由 OpenAI 提出）讓模型學習人類偏好，而不僅僅是模仿訓練資料。

### 三階段流程

```
Phase 1: SFT — 在示範資料上微調
Phase 2: Reward Model — 訓練獎勵模型預測人類偏好
Phase 3: PPO — 使用獎勵模型透過 PPO 最佳化策略
```

### Reward Model 訓練

```python
# Reward Model 的核心：比較兩筆回覆
def compute_reward_loss(reward_model, x, y_win, y_lose):
    r_win = reward_model(x, y_win)    # 好的回覆
    r_lose = reward_model(x, y_lose)  # 差的回覆
    # 讓獎勵模型學會偏好好的回覆
    loss = -log(sigmoid(r_win - r_lose))
    return loss
```

### PPO 訓練

PPO 使用獎勵模型評分來更新 LLM 的權重，同時透過 KL 懲罰項防止偏離原始模型太遠：

```
PPO 損失 = -E[r(x,y)] + β × KL(π_θ || π_ref)

第一項最大化獎勵
第二項防止模型「駭入」獎勵模型
β 控制探索-利用權衡
```

## DPO：直接偏好最佳化

2023 年斯坦福團隊提出 DPO，證明無需顯式的獎勵模型和 PPO：

```python
def dpo_loss(policy_logits, ref_logits, y_win, y_lose):
    # 直接比較偏好配對的 log-probability
    win_prob = log_prob(policy_logits, y_win) - log_prob(ref_logits, y_win)
    lose_prob = log_prob(policy_logits, y_lose) - log_prob(ref_logits, y_lose)
    loss = -log(sigmoid(win_prob - lose_prob))
    return loss
```

```
傳統 RLHF  vs  DPO：
─────────────────────────────
RLHF: SFT → Train RM → PPO (3 階段，複雜)
      需要同時載入 4 個模型 (policy, ref, reward, value)

DPO:  SFT → DPO (2 階段，簡單)
      只需要 2 個模型 (policy, ref)
```

截至 2026 年，DPO 及其變體（KTO、ORPO、SimPO）已成為偏好最佳化的首選方法。RLHF 的 PPO 由於訓練不穩定性，僅在超大規模（>100B 參數）仍被少數團隊使用。

---

## 延伸閱讀

- [RLHF 原始論文](https://www.google.com/search?q=Training+language+models+to+follow+instructions+with+human+feedback)
- [DPO 論文](https://www.google.com/search?q=Direct+Preference+Optimization+DPO+language+model)
- [Instruction Tuning 最佳實踐](https://www.google.com/search?q=instruction+tuning+best+practices+LIMA+data)
- [Llama 2 微調報告](https://www.google.com/search?q=Llama+2+open+foundation+fine-tuned+language+models)

---

*AI 程式人雜誌 2026 年 7 月號 — 大型語言模型實戰*
