# RL 在機器人學中的應用（2017-2028）

## 為什麼機器人需要強化學習？

傳統機器人控制依賴精確的物理模型和手工設計的控制規則。但現實世界充滿不確定性：摩擦力變化、零件磨損、物體形狀不同、光照條件改變。強化學習讓機器人能透過試錯學習適應這些變化。

機器人 RL 的核心困難：

```
物理世界挑戰：
  1. 樣本效率低：一次跌倒就是真的跌倒
  2. 安全約束：不能隨便試錯
  3. 真實性差距：模擬器和真實世界的差異
  4. 連續動作：高維度的關節控制
```

## Sim-to-Real 遷移（2017-2020）

由於機器人真實數據收集成本高，RL 在模擬器中訓練後遷移到真實世界成為主流方法。

### Domain Randomization

OpenAI 在 2017 年展示了 Domain Randomization：在模擬器中隨機化視覺參數（顏色、紋理、光照），使模型在真實世界中也能泛化：

```python
import random

def randomize_scene(scene):
    # 隨機化物理參數
    scene.friction = random.uniform(0.2, 1.0)
    scene.mass = random.uniform(0.5, 2.0)
    scene.gravity = random.uniform(8.0, 11.0)

    # 隨機化視覺參數
    scene.light_color = random.choice(['white', 'yellow', 'red'])
    scene.texture = random.choice(['wood', 'metal', 'plastic', 'rubber'])
    scene.background = random.choice(['white', 'gray', 'random'])

    return scene
```

2018 年，OpenAI 的 Dactyl 機器人手使用 Domain Randomization 學會了解決魔術方塊，這個成果登上了 Nature 封面。

### 模擬器技術演進

| 年份 | 模擬器 | 特點 |
|------|--------|------|
| 2017 | MuJoCo | 快速物理模擬 |
| 2018 | PyBullet | 開源替代方案 |
| 2020 | Isaac Gym | GPU 加速、大規模並行 |
| 2022 | Brax | JAX 生態、可微分物理 |
| 2024 | Genesis | 即時光線追蹤物理 |
| 2026 | MuJoCo-X | 基於 JAX 的 GPU 加速版本 |

## 無模型 RL 在機器人中的應用（2021-2024）

### 獎勵函數設計

機器人 RL 最困難的部分是獎勵函數設計。稀疏獎勵（只有成功或失敗）難以學習；密集獎勵需要大量手動調整。

**Successor Features（2021）**：將獎勵分解為多個任務相關的特徵，實現一次性訓練多個任務。

**Hindsight Experience Replay（HER, 2018）**：即使沒有達到目標，也將實際達到的狀態視為目標來學習：

```python
class HER:
    def replay(self, trajectory, goal):
        for t in range(len(trajectory)):
            s, a, r, s_next = trajectory[t]
            # 原始經驗：未達目標
            self.buffer.push(s, a, r, s_next, done=False)

            # 後見之明：假設目標是實際到達的位置
            achieved_goal = s_next['achieved']
            fake_reward = 1 if achieved_goal == trajectory['desired_goal'] else 0
            self.buffer.push(s, a, fake_reward, s_next, done=(fake_reward == 1))
```

### 基於模型的 RL（2022-2024）

學習一個環境模型，然後在模型中規劃或訓練策略：

```
真實世界 ──┬── 收集數據 → 學習模型 ──→ 模型預測
           │                              │
           └── ←── 執行策略 ←── 在模型中訓練 ←─┘
```

Dreamer（2020-2023）系列演算法展示了基於模型的 RL 在機器人任務中的有效性，使用潛在動力學模型進行想像軌跡的訓練。

## 2024-2028：基礎模型與機器人 RL

### RT-2 與具身智能（2023）

Google 的 RT-2（Robotic Transformer 2）將網路規模的視覺語言知識遷移到機器人控制。這不是傳統的 RL，而是「模仿學習 + 大規模預訓練」：

```
RT-2 輸入：相機圖像 + 自然語言指令
RT-2 輸出：機械臂的離散動作 token
訓練數據：網路上的圖文資料 + 機器人示範
```

### 決策基礎模型（2025-2028）

最新的趨勢是用 RL 訓練通用的「機器人大腦」：

- **Octo（2024）**：在 800 萬次機器人示範上訓練的擴散策略模型
- **π0（2025）**：Physical Intelligence 發表的通用機器人操作模型
- **GR-2（2026）**：大規模視頻預訓練後進行 RL 微調

### 仿真到真實的無縫橋樑（2026-2028）

2028 年的技術突破是「可微分物理引擎」和「神經渲染」的結合，使模擬與真實的差距幾乎為零：

```python
# 概念：統一模擬-真實訓練
def train_in_unified_env(robot_policy):
    while True:
        # 1. 在可微分模擬器中訓練
        sim_loss = train_in_differentiable_sim(robot_policy)

        # 2. 使用真實感渲染進行域隨機化
        sim_loss += photorealistic_domain_randomization(robot_policy)

        # 3. 線上適應：少數真實樣本校正
        real_loss = few_shot_real_world_adapt(robot_policy, n_samples=5)

        # 4. 更新策略
        total_loss = sim_loss + 0.1 * real_loss
        total_loss.backward()
        robot_policy.step()
```

## 延伸閱讀

- [OpenAI Dactyl 機器人手](https://www.google.com/search?q=OpenAI+Dactyl+Solving+Rubik%27s+Cube+with+a+Robot+Hand)
- [RT-2 論文](https://www.google.com/search?q=RT-2+Vision-Language-Action+Model+Transferring+Web+Knowledge+to+Robotic+Control)
- [Dreamer 系列](https://www.google.com/search?q=Dreamer+Reinforcement+Learning+with+World+Models)

*本篇文章為「AI 程式人雜誌 2028 年 5 月號」強化學習系列之一。*
