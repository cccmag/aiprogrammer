# 因果 AI 的未來與挑戰（2023-2028）

## 當前瓶頸

### 因果發現的不穩定性

從有限數據中恢復真實 DAG 是 NP-hard 問題。即使 NOTEARS 等連續方法也對超參數敏感，在小樣本下容易過擬合。

### 隱藏混淆變數

現實中總存在未觀測的混淆變數。代理學習（Proxy Learning）與敏感度分析是應對策略，但尚無普適解法。

### 可擴展性

現有因果方法在百萬級特徵與樣本下的表現遠不如深度學習。因果深度學習需要更高效的架構。

## 前沿方向

### 因果強化學習（2023-2028）

將因果結構整合進 RL 的狀態表徵，讓智能體理解動作的真正後果，而非僅學習表面相關。DeepMind 的 Causal RL 在 Minecraft 導航任務中超越傳統方法。

### 基礎模型中的因果

大型語言模型是否具備因果推理能力？2025 年的研究顯示 LLM 在某些因果任務上表現良好，但容易受提示的虛假相關干擾。因果微調（Causal Fine-tuning）成為新方向。

### 因果世界模型

Yann LeCun 的「世界模型」本質上是因果模型——理解動作如何改變世界狀態。到 2028 年，因果世界模型被視為通用人工智慧的關鍵組件。

## 結語

因果 AI 從統計學的邊疆發展為 AI 的核心支柱。從 Pearl 的結構方程到 LLM 的因果推理，這場從「相關到因果」的旅程才剛開始。

參考：[搜尋 Causal Reinforcement Learning](https://www.google.com/search?q=Causal+Reinforcement+Learning) | [搜尋 Causal World Model](https://www.google.com/search?q=Causal+World+Model+AI)
