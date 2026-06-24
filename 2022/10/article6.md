# Bradley-Terry 獎勵模型

## 1. 引言

Bradley-Terry 模型是 RLHF 中訓練獎勵模型的標準方法。它將人類的偏好判斷轉化為一個可訓練的獎勵函數。本文將深入探討 Bradley-Terry 模型的數學原理和實作細節。

## 2. Bradley-Terry 模型

Bradley-Terry 模型最初用於處理配對比較資料（如體育比賽的勝負）。在 RLHF 中，我們用它來建模人類對兩個回應的偏好。

### 模型定義

給定回應 y_1 和 y_2，人類偏好 y_1 勝過 y_2 的機率：

```
P(y_1 > y_2) = σ(r_θ(y_1) - r_θ(y_2))
```

其中：
- r_θ(y) 是獎勵模型對回應 y 的獎勵分數
- σ(x) = 1 / (1 + e^{-x}) 是 sigmoid 函數

### 直觀理解

當 r_θ(y_1) 遠大於 r_θ(y_2) 時，P(y_1 > y_2) → 1
當 r_θ(y_1) 遠小於 r_θ(y_2) 時，P(y_1 > y_2) → 0
當 r_θ(y_1) = r_θ(y_2) 時，P(y_1 > y_2) = 0.5（隨機猜測）

## 3. 損失函數

Bradley-Terry 模型的損失函數是負對數似然：

```
L(θ) = -E_{(y_w, y_l)}[ log σ(r_θ(y_w) - r_θ(y_l)) ]
```

其中 y_w 是勝出的回應（人類偏好），y_l 是失敗的回應。

### 梯度分析

對損失求梯度：

```
∇L(θ) = -E[ σ(r(y_l) - r(y_w)) * (∇r(y_w) - ∇r(y_l)) ]
```

當獎勵模型錯誤地給 y_l 高分時，σ(r(y_l) - r(y_w)) 較大，梯度會強烈懲罰這個錯誤。

## 4. 獎勵模型的架構

```python
class RewardModel:
    def __init__(self, base_model):
        self.base_model = base_model  # 預訓練語言模型
        self.reward_head = Linear(base_model.hidden_size, 1)

    def forward(self, input_ids, attention_mask):
        hidden = self.base_model(input_ids, attention_mask)
        # 取最後一個詞元的隱藏狀態
        last_hidden = hidden[:, -1, :]
        reward = self.reward_head(last_hidden)
        return reward.squeeze(-1)

    def compute_loss(self, chosen_rewards, rejected_rewards):
        # Bradley-Terry 損失
        logits = chosen_rewards - rejected_rewards
        loss = -log(sigmoid(logits)).mean()
        return loss
```

### 架構設計

- **基底模型**：使用預訓練語言模型提取回應的表示
- **獎勵頭**：將表示映射為標量獎勵分數
- **共享權重**：基底模型與原始語言模型共享大部分權重

## 5. 損失函數的變體

### 帶邊界的 Bradley-Terry

```
L(θ) = -E[ log σ(r(y_w) - r(y_l) - m) ]
```

m 是一個邊界，強迫獎勵分數至少相差 m。提高獎勵模型的區分能力。

### ListMLE 排名損失

對於排名清單（如 y_1 > y_2 > ... > y_k）：

```
L(θ) = -E[ log ∏ P(y_i > {y_j}_{j>i}) ]
```

這將配對比較擴展到完整排名。

## 6. 獎勵模型的評估

評估獎勵模型主要有以下指標：

- **準確率**：配對比較的預測準確率
- **一致性**：不同提示下的獎勵分數穩定性
- **泛化能力**：對未見過的提示的表現
- **校準度**：獎勵分數是否與人類偏好程度匹配

## 7. 結語

Bradley-Terry 模型是 RLHF 中獎勵模型訓練的核心。它的簡單性和有效性使其成為業界標準。理解這個模型是理解 RLHF 流程的關鍵一步。

## 延伸閱讀

- [Bradley-Terry 綜述](https://www.google.com/search?q=Bradley+Terry+model+statistical+tutorial)
- [獎勵模型訓練細節](https://www.google.com/search?q=reward+model+training+best+practices)
