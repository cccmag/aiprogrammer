# 決策 AI 的未來（2023-2028）

## 從預測到決策

過去十年，AI 的核心能力是預測——分類、回歸、生成。但真實世界的問題需要的不是預測，而是決策。強化學習是從預測到決策的橋樑。

2023 年，DeepMind 發表了「決策 AI 生態系統」的概念框架：

```
預測 AI：   輸入 → 模型 → 預測結果
決策 AI：   觀測 → 模型 → 動作 → 環境變化 → 新觀測 → ...
```

這個區別至關重要。預測是靜態的，決策是動態的、序列的、因果的。

## 決策 Transformer（2023-2024）

2023 年，決策 Transformer（Decision Transformer）將 RL 重構為序列建模問題：

```python
class DecisionTransformer:
    def __init__(self, transformer_model):
        self.model = transformer_model

    def train_on_trajectories(self, trajectories):
        # 將軌跡編碼為 (回報目標, 狀態, 動作) 序列
        tokens = []
        for (returns, states, actions) in trajectories:
            tokens.append([returns, states, actions])

        # 使用自迴歸方式預測下一個動作
        loss = self.model.next_action_prediction(tokens)
        loss.backward()

    def act(self, target_return, state):
        # 給定目標回報和當前狀態，生成動作
        return self.model.generate(target_return, state)
```

決策 Transformer 的貢獻在於：它將 RL 的成功歸因於 Transformer 的序列建模能力，而非傳統的價值迭代。這啟發了後續大量「LLM + RL」的研究。

## 世界模型（2024-2026）

Yann LeCun 提出的「世界模型」（World Models）架構，主張決策 AI 的核心是在內部建立世界的因果模型：

```
世界模型架構：
  ┌───────┐    ┌─────────┐    ┌───────┐
  │ 感知器  │──→│ 世界模型  │──→│  規劃器  │
  └───────┘    └─────────┘    └───────┘
       │             │             │
       ▼             ▼             ▼
   原始數據    因果預測        行動序列
```

世界模型使 AI 能在行動之前在「想像力」中測試結果，大幅提高樣本效率。

### Genie（2024）

Google DeepMind 的 Genie 從網際網路影片中學習世界模型，無需任何動作標籤。這是「無監督 RL」的重要進展。

### Efficient World Models（2025-2026）

2025-2026 年，世界模型的研究重點是效率和可解釋性。基於狀態空間模型（SSM）和 Mamba 架構的世界模型在計算效率上顯著優於 Transformer 方案。

## LLM 與 RL 的深度融合（2025-2028）

### 推理能力強化

2025-2026 年，OpenAI 的 o1/o3 系列和 DeepSeek-R1 展示了 RL 在提升 LLM 推理能力上的驚人效果。RL 不僅讓模型學會了「如何思考」，還學會了「何時該深入思考」。

```
傳統 LLM：給定問題 → 立即生成答案
RL 增強的 LLM：給定問題 → 思考是否需要鏈條推理
              → 如果是：生成多步推理
              → 如果否：直接回答
              → 自我檢查 → 最終答案
```

### 工具使用與環境互動（2026-2027）

RL 使 LLM 學會使用工具——搜尋引擎、程式碼直譯器、計算器——在與環境的互動中完成複雜任務。

```python
# 概念：RL 訓練智能體使用工具
def tool_use_rl_loop(llm, environment, tools):
    for episode in range(10000):
        state = environment.reset()
        done = False
        trajectory = []

        while not done:
            action = llm.generate_action(state, tools)
            # 動作可以是：思考、調用工具、回答
            next_state, reward, done = environment.step(action)
            trajectory.append((state, action, reward, next_state))

        # RL 更新
        llm.update_from_rewards(trajectory)
```

## 2028 年關鍵趨勢

### 統一決策模型

2028 年最重要的趨勢是「統一決策模型」：一個模型處理多種決策任務，從文字對話到機器人控制：

| 任務類型 | 傳統方案 | 統一方案 |
|---------|---------|---------|
| 自然語言 | GPT-like | 同一模型 |
| 遊戲控制 | DQN/SAC | 同一模型 |
| 機器人操作 | 專用策略 | 同一模型 |
| 自動駕駛 | 模塊化 | 同一模型 |
| 商業決策 | 啟發式 | 同一模型 |

### 安全與對齊

2028 年的決策 AI 安全框架包括：

- **可逆性保證**：決策必須是可逆的或具有安全回退
- **對抗性魯棒性**：在對抗環境中保持穩定
- **價值一致性**：決策與人類價值觀一致
- **可解釋決策**：AI 必須能解釋為何做出特定決策

### AGI 之路

決策 AI 被認為是通往 AGI 的關鍵路徑。Yann LeCun 和 Richard Sutton 都認為，真正的智慧必須包含在複雜世界中做出序列決策的能力。

Sutton 的「苦澀教訓」（The Bitter Lesson）強調：建立在搜尋和學習之上的通用方法最終會超越人類設計的特定方案。RL 正是這種通用方法的典範。

## 結語

從 1956 年的 Bellman Equation 到 2028 年的統一決策模型，強化學習走過了七十多年的歷程。它從心理學的一個分支，成長為 AI 的核心支柱之一。

未來的決策 AI 將不僅僅是做出選擇——它將理解選擇的後果，規劃長期的路徑，並與人類的價值觀保持一致。這或許是 AGI 到來前最後的旅程。

## 延伸閱讀

- [Decision Transformer 論文](https://www.google.com/search?q=Decision+Transformer+Reinforcement+Learning+via+Sequence+Modeling)
- [Sutton Bitter Lesson](https://www.google.com/search?q=Sutton+The+Bitter+Lesson)
- [World Models 論文](https://www.google.com/search?q=World+Models+Ha+Schmidhuber+2018)
- [Genie 世界模型](https://www.google.com/search?q=Genie+Generative+Interactive+Environments+DeepMind+2024)

*本篇文章為「AI 程式人雜誌 2028 年 5 月號」強化學習系列之一。*
