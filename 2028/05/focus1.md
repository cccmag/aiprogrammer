# 強化學習基礎與演進（1956-2028）

## 從行為心理學到馬可夫決策過程

強化學習（Reinforcement Learning, RL）的根源可以追溯到 1950 年代的行為心理學。B.F. Skinner 的操作制約理論（Operant Conditioning）指出：當一個行為帶來正向回饋時，這個行為被強化的機率增加；反之則減少。這種「嘗試—錯誤—學習」的循環，正是 RL 的核心思想。

1956 年，Richard Bellman 提出了動態規劃理論，引入了著名的 Bellman Equation：

```
V(s) = maxₐ [ R(s,a) + γ Σₛ' P(s'|s,a) V(s') ]
```

其中 V(s) 是狀態 s 的價值，R(s,a) 是即時獎勵，γ 是折扣因子，P(s'|s,a) 是狀態轉移機率。這個方程式為後續所有 RL 演算法提供了理論基礎。

## 馬可夫決策過程

RL 的數學模型是馬可夫決策過程（Markov Decision Process, MDP），由五元組 (S, A, P, R, γ) 定義：

- **S**：狀態集合
- **A**：動作集合
- **P(s'|s,a)**：狀態轉移機率
- **R(s,a)**：獎勵函數
- **γ ∈ [0,1]**：折扣因子

MDP 的關鍵假設是「馬可夫性質」：下一個狀態只取決於當前狀態和動作，與歷史無關。

```
P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, ...) = P(s_{t+1} | s_t, a_t)
```

## 動態規劃與值迭代（1956-1980）

Bellman 的動態規劃方法包含兩個核心過程：

**策略評估（Policy Evaluation）：**
```
V_{k+1}(s) = Σₐ π(a|s) [ R(s,a) + γ Σₛ' P(s'|s,a) V_k(s') ]
```

**策略迭代（Policy Iteration）：**
```
π'(s) = argmaxₐ [ R(s,a) + γ Σₛ' P(s'|s,a) V(s') ]
```

這種方法需要完整知道環境模型（P 和 R），在現實問題中往往不可行。

## 無模型強化學習（1988-2013）

1988 年，Chris Watkins 在其博士論文中提出了 Q-Learning，這是第一個無模型的 RL 演算法。Q-Learning 不需要環境模型，通過與環境互動來學習：

```
Q(s,a) ← Q(s,a) + α [ R(s,a) + γ maxₐ' Q(s',a') - Q(s,a) ]
```

其中 α 是學習率。這個更新規則稱為「時間差分學習」（Temporal Difference Learning, TD Learning）。

Sutton 和 Barto 在 1998 年出版了《Reinforcement Learning: An Introduction》，這本書至今仍是 RL 領域的聖經。

## 深度強化學習的革命（2013-2018）

2013 年，DeepMind 發表了 DQN（Deep Q-Network），用深度神經網路取代 Q 值表格，在 Atari 遊戲上超越人類水準。這是深度強化學習（Deep RL）的起點。

2016 年，AlphaGo 擊敗了李世石，震驚世界。AlphaGo 結合了策略網路、價值網路和蒙地卡羅樹搜索（MCTS）：

```
AlphaGo 架構：
  ┌─────────────┐
  │   棋盤狀態   │
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │  策略網路   │ → 建議落子機率
  ├─────────────┤
  │  價值網路   │ → 評估局面勝率
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │  MCTS 搜索  │ → 綜合決策
  └─────────────┘
```

## 從 AlphaGo 到 ChatGPT（2017-2028）

2017 年，AlphaZero 展示了完全自對弈的 RL 方法，不需要人類棋譜。2021 年，RLHF（Reinforcement Learning from Human Feedback）被成功應用於 GPT 模型的訓練，結合了人類偏好和強化學習。

2024 年後，RL 與大型語言模型的結合更加深入。GRPO（Group Relative Policy Optimization）和 RLOO（Reinforcement Learning from Online Outputs）等方法大幅提升了 LLM 的推理能力。

2026-2028 年，決策基礎模型（Decision Foundation Model）成為熱門方向：一個模型在多種決策任務上預訓練，能零樣本遷移到新任務。

## 演算法演進時間線

| 年份 | 里程碑 | 意義 |
|------|--------|------|
| 1956 | Bellman Equation | RL 的數學基礎 |
| 1988 | Q-Learning | 第一個無模型 RL |
| 1992 | TD-Gammon | 第一個世界級 RL 應用 |
| 2013 | DQN | 深度 RL 誕生 |
| 2016 | AlphaGo | 擊敗人類頂尖棋手 |
| 2017 | AlphaZero | 純自對弈學習 |
| 2018 | SAC, TD3 | 穩定深度 RL 演算法 |
| 2021 | RLHF | 人類偏好引入 RL |
| 2025 | GRPO | 高效 LLM 後訓練 |
| 2028 | Decision FM | 通用決策基礎模型 |

## 延伸閱讀

- [Sutton & Barto Reinforcement Learning](https://www.google.com/search?q=Sutton+Barto+Reinforcement+Learning+An+Introduction)
- [DeepMind DQN Atari](https://www.google.com/search?q=DeepMind+DQN+Playing+Atari+with+Deep+Reinforcement+Learning)
- [AlphaGo 論文](https://www.google.com/search?q=AlphaGo+Mastering+the+game+of+Go+with+deep+neural+networks)
- [RLHF 原始論文](https://www.google.com/search?q=RLHF+Training+language+models+to+follow+instructions)

*本篇文章為「AI 程式人雜誌 2028 年 5 月號」強化學習系列之一。*
