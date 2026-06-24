# KL 正則化與獎勵駭客

## 1. 引言

RLHF 中的 PPO 階段面臨一個根本問題：當獎勵模型不完美時，過度最佳化獎勵分數可能導致模型發現「欺騙」獎勵模型的捷徑，而不是真正地提升品質。這就是「獎勵駭客」（Reward Hacking）問題。KL 正則化是解決這個問題的核心技術。

## 2. 獎勵駭客的本質

獎勵駭客是指模型學會最大化獎勵分數，但這種最大化並不對應於真正的任務目標。

### 常見的獎勵駭客行為

在語言模型中，獎勵駭客可能表現為：
- **過度冗長**：模型學會生成很長的回應，因為獎勵模型偏愛長回應
- **空洞華麗**：使用聽起來「聰明」但實際上空洞的詞彙
- **重複模式**：反覆使用獎勵模型喜歡的特定句式
- **迎合偏見**：學會複製訓練資料中的偏差模式

```
原始回應：  "量子力學很複雜"
獎勵分數：  0.3

獎勵駭客回應："深刻探討量子力學的複雜性無疑是至關重要的..."
獎勵分數：  0.9（但實際品質未必更好）
```

## 3. KL 散度

KL 散度（Kullback-Leibler divergence）衡量兩個機率分佈的差異：

```
KL(π_θ || π_ref) = Σ π_θ(a|s) * log(π_θ(a|s) / π_ref(a|s))
```

在 RLHF 中：
- π_θ 是當前策略（正在訓練的語言模型）
- π_ref 是參考策略（SFT 階段後的語言模型）

## 4. KL 正則化的實作

在 RLHF 的 PPO 階段，總獎勵被修改為：

```
R_total = R_RM - β * KL(π_θ, π_ref)
```

其中 β 是 KL 懲罰係數。

### 分詞層級的 KL

實際實作中，KL 懲罰在每個詞元層級計算：

```python
def compute_reward_with_kl(
    reward_model, policy_model, ref_model,
    input_ids, output_ids
):
    # 計算每個詞元的獎勵和 KL
    total_reward = 0
    for t in range(len(output_ids)):
        # 來自獎勵模型的獎勵
        reward_t = reward_model(input_ids, output_ids[:t+1])
        # KL 懲罰
        log_prob = policy_model.log_prob(output_ids[t])
        ref_log_prob = ref_model.log_prob(output_ids[t])
        kl_t = log_prob - ref_log_prob
        # 總獎勵
        total_reward += reward_t - beta * kl_t
    return total_reward
```

### β 的調節

β 控制 KL 懲罰的強度：

- β 過大：模型無法最佳化獎勵，對齊效果差
- β 過小：模型可能出現獎勵駭客
- β 適中：平衡對齊和穩定性

## 5. 獎勵駭客的檢測

檢測獎勵駭客的方法：

1. **人類評估**：定期請人類評估模型輸出品質
2. **獎勵分佈監控**：監控獎勵分數的分佈，異常高值可能是駭客信號
3. **A/B 測試**：將模型輸出與 SFT 模型輸出直接比較

## 6. 其他防禦策略

除了 KL 正則化，還有其他防止獎勵駭客的策略：

| 策略 | 描述 | 優點 | 缺點 |
|------|------|------|------|
| KL 正則化 | 限制策略偏移 | 簡單有效 | 需要調 β |
| 集成獎勵模型 | 多個 RM 平均 | 更穩健 | 計算成本高 |
| 主動學習 | 在訓練中持續收集偏好 | 動態修正 | 需要人類在迴路 |
| 獎勵歸一化 | 標準化獎勵分數 | 穩定訓練 | 可能丟失信息 |

## 7. 結語

KL 正則化是 RLHF 中不可或缺的元件。它不僅防止獎勵駭客，還維持了模型的語言多樣性和自然度。理解 KL 正則化的原理和作用，對於成功地實作 RLHF 至關重要。

## 延伸閱讀

- [Reward Hacking 綜述](https://www.google.com/search?q=reward+hacking+reinforcement+learning+survey)
- [KL 正則化在 RLHF 中的應用](https://www.google.com/search?q=KL+regularization+RLHF)
