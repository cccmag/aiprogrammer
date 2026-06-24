# 本期焦點

## 強化學習基礎

### 引言

強化學習（Reinforcement Learning，RL）是機器學習的三大分支之一，與監督學習和無監督學習並列。不同於監督學習從標註資料中學習，強化學習的智能體（Agent）通過與環境互動，從經驗中學習如何做出一系列決策。

從 AlphaGo 擊敗世界冠軍，到自動駕駛的決策系統，強化學習已經在許多領域展現出驚人的能力。本期，我們將深入探討強化學習的核心理論和演算法，包括馬可夫決策過程、Q-learning、Policy Gradient，以及如何將深度學習與強化學習結合。

---

## 大綱

* [程式：Q-learning 與 Policy Gradient 實作](focus_code.md)
   - 經典 Q-learning 实现
   - Policy Gradient 基本方法
   - CartPole 環境範例

1. [強化學習概述：從經驗中學習的 AI](focus1.md)
   - 強化學習的基本框架
   - Agent 與環境的互動
   - 探索與利用的平衡

2. [馬可夫決策過程：MDP 與價值函數](focus2.md)
   - 狀態、動作、獎勵
   - 價值函數與 Q 函數
   - 折扣因子與最優策略

3. [Q-learning 與深度 Q 網路：基於價值的強化學習](focus3.md)
   - Q-learning 演算法
   - DQN 與經驗回放
   - 目標網路與雙DQN

4. [Policy Gradient 方法：基於策略的強化學習](focus4.md)
   - REINFORCE 演算法
   - 策略梯度定理
   - 方差 reduction

5. [Actor-Critic 架構：結合價值與策略](focus5.md)
   - Actor-Critic 基本原理
   - A2C 與 A3C
   - PPO 和其他進階方法

6. [AlphaGo 與圍棋 AI：深度強化學習的勝利](focus6.md)
   - AlphaGo 的技術架構
   - Monte Carlo Tree Search
   - AlphaGo Zero 與 AlphaZero

7. [未來展望：強化學習的發展方向](focus7.md)
   - 多智慧體強化學習
   - 強化學習與大型語言模型
   - 產業應用前景

---

## 濃縮回顧

### 強化學習的基本框架

強化學習的核心是智能體（Agent）與環境（Environment）的互動：

**智能體**：
- 觀察環境狀態
- 選擇並執行動作
- 根據獎勵學習策略

**環境**：
- 根據動作轉移到新狀態
- 提供獎勵信號
- 定義任務目標

### 馬可夫決策過程（MDP）

MDP 是強化學習的數學框架：

- **狀態空間 S**：所有可能的狀態
- **動作空間 A**：所有可能的動作
- **轉移機率 P**：P(s'|s,a)
- **獎勵函數 R**：R(s,a,s')
- **折扣因子 γ**：0 ≤ γ < 1

### 經典演算法

**Q-learning**：
- 學習動作-價值函數 Q(s,a)
- 使用 Bellman 方程更新
- 離策略（off-policy）學習

**Policy Gradient**：
- 直接優化策略函數 π(a|s)
- 使用梯度上升更新
- 在策略（on-policy）學習

**Actor-Critic**：
- 結合價值和策略方法
- Actor 學習策略
- Critic 估計價值

### AlphaGo 的啟示

2016 年 AlphaGo 擊敗李世石，展示了深度強化學習的潛力：
- 使用 CNN 評估棋局
- Monte Carlo Tree Search 規劃
- 深度學習與傳統方法的結合

---

## 結論與展望

強化學習是通往通用人工智慧的重要一步。通過與環境互動學習，智能體可以不斷提升其決策能力。然而，挑戰依然存在：
- 樣本效率低
- 訓練不穩定
- 安全性問題

未來，我們期待看到強化學習在更多領域展現其威力。

---

## 延伸閱讀

- [強化學習概述](focus1.md)
- [馬可夫決策過程](focus2.md)
- [Q-learning 與 DQN](focus3.md)
- [Policy Gradient 方法](focus4.md)
- [Actor-Critic 架構](focus5.md)
- [AlphaGo 與圍棋 AI](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。感謝閱讀《AI 程式人雜誌》2021 年 9 月號。*