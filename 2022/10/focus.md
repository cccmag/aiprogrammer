# 本期焦點

## RLHF 與人類反饋：從強化學習到對齊

### 引言

2022 年是強化學習從人類反饋（RLHF）走向主流的一年。從 InstructGPT 到即將問世的 ChatGPT，RLHF 已經成為大型語言模型對齊人類價值觀的核心技術。本期將深入探討 RLHF 的各個面向——從強化學習的基礎理論，到策略梯度與 PPO 演算法，再到人類偏好資料的收集與獎勵模型的訓練。

RLHF 的核心思想很直觀：與其讓 AI 模型自行摸索任務目標，不如讓它從人類反饋中學習。人類提供的不再是「正確答案」，而是「偏好排序」——哪個輸出更好、哪個更安全、哪個更符合人類意圖。這種學習方式讓模型能夠處理那些難以用形式化目標定義的任務。

### 大綱

- [程式：RLHF 完整流程模擬](focus_code.md)
  - 虛擬環境、策略網路、獎勵模型、PPO 更新、KL 懲罰

1. [強化學習基礎：Agent、環境、獎勵](focus1.md)
   - MDP 框架、策略、值函數、優勢函數

2. [策略梯度與 PPO](focus2.md)
   - 策略梯度定理、重要性採樣、PPO 截斷

3. [人類反饋的收集與標註](focus3.md)
   - 偏好資料集、標註工具、品質控制

4. [獎勵模型訓練](focus4.md)
   - Bradley-Terry 模型、pairwise loss、排名聚合

5. [PPO 與 RLHF 流程](focus5.md)
   - 完整管線：SFT → 獎勵模型 → PPO

6. [對齊問題與憲法 AI](focus6.md)
   - 價值對齊、AI 安全、憲法 AI

7. [RLHF 的挑戰與替代方案](focus7.md)
   - 獎勵駭客、分佈偏移、DPO、SLiC

### 從監督學習到人類反饋

傳統的監督學習使用「正確答案」訓練模型。但在許多真實場景中，「正確答案」並不存在——我們只知道哪個答案相對更好。這就是 RLHF 的出發點：用偏好取代標籤。

```
監督學習：輸入 → 正確答案
RLHF：     輸入 → 候選 A > 候選 B（人類偏好）
```

這種轉變不僅改變了訓練方式，也改變了我們對 AI 系統的期望——從「正確」到「有用且安全」。

### RLHF 的三階段流程

```
Phase 1: 監督微調（SFT）
  收集人類示範資料 → 微調預訓練模型

Phase 2: 獎勵模型訓練
  收集人類偏好資料 → 訓練獎勵模型

Phase 3: PPO 強化學習
  使用獎勵模型 → 強化學習最佳化策略
```

### 濃縮回顧

強化學習的歷史可以追溯到 1950 年代的動態規劃，但 RLHF 的誕生是近年的事情：

- **2017**：OpenAI 發表 RLHF 先驅論文，將強化學習應用於摘要任務
- **2020**：OpenAI 發表 InstructGPT 的前期工作，使用人類反饋微調 GPT
- **2022**：InstructGPT 論文正式發表，ChatGPT 誕生，RLHF 成為主流

### RLHF 的獨特優勢

| 特性 | 傳統 RL | RLHF |
|------|---------|------|
| 獎勵來源 | 環境自動給出 | 人類判斷 |
| 任務定義 | 明確的目標函數 | 模糊的偏好 |
| 安全性 | 透過懲罰機制 | 透過人類判斷 |
| 擴展性 | 容易（自動化） | 困難（需人類） |

---

**下一步**：[程式實作](focus_code.md) → [強化學習基礎](focus1.md)

## 延伸閱讀

- [InstructGPT 論文](https://www.google.com/search?q=InstructGPT+training+language+models+to+follow+instructions)
- [Constitutional AI](https://www.google.com/search?q=Constitutional+AI+Anthropic)
- [RLHF 綜述](https://www.google.com/search?q=reinforcement+learning+from+human+feedback+survey)
