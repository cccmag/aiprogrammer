# RLHF 完整流程模擬

## rlhf_demo.py 說明

本程式是一個完整的 RLHF 流程模擬，展示從強化學習環境到 PPO 訓練的核心概念。使用純 Python 實作，無需外部深度學習框架。

### 核心元件

**1. 虛擬環境（VirtualEnv）**

模擬一個簡單的強化學習環境，包含三個狀態和兩個動作：
- 狀態：S0（起始）、S1（中繼）、S2（終端）
- 動作：A（前進）、B（重置）
- 獎勵：到達 S2 獲得 +1，其他為 0

```
S0 ──A──→ S1 ──A──→ S2 [+1]
 │                │
 └──B──→ S0       └──B──→ S0
```

**2. 策略網路（PolicyNetwork）**

使用 softmax 策略，參數化動作機率分佈。PPO 訓練即更新這些參數。

**3. 獎勵模型（RewardModel）**

從人類偏好配對中訓練，使用 Bradley-Terry 模型：
```
P(y_w > y_l) = σ(r(y_w) - r(y_l))
```

**4. PPO 訓練器**

實作 PPO 的截斷目標和 KL 正則化：
```
L_CLIP = min(r_t(θ) * A_t, clip(r_t, 1-ε, 1+ε) * A_t)
```

### 訓練流程

```
1. 隨機策略生成軌跡
2. 軌跡配對產生「人類偏好」
3. 訓練獎勵模型（Bradley-Terry）
4. 使用 PPO 最佳化策略
5. 計算 KL 懲罰防止過度偏離
```

### 執行結果範例

```
=== RLHF 完整流程模擬 ===

[Phase 1] 隨機策略採樣
  生成 100 條軌跡

[Phase 2] 獎勵模型訓練
  訓練 50 個配對，準確率: 82%

[Phase 3] PPO 策略最佳化
  Episode 1: reward=0.12, KL=0.04
  Episode 5: reward=0.45, KL=0.08
  Episode 10: reward=0.78, KL=0.12

[Phase 4] 最終評估
  平均獎勵: 0.85
  KL 距離: 0.11
  成功到達機率: 83%
```

### 關鍵設計決策

- **不使用深度學習框架**：保持程式碼自包含，專注展示 RLHF 的核心數學
- **簡化的離散環境**：讓讀者可以直觀理解策略學習過程
- **Bradley-Terry 獎勵模型**：展示偏好學習的核心機制
- **KL 正則化**：展示防止獎勵駭客的關鍵技術

### 延伸實驗

讀者可以嘗試以下修改：

1. **改變環境結構**：增加更多狀態和動作
2. **調整 PPO 截斷參數**：觀察 ε 對訓練穩定性的影響
3. **調整 KL 懲罰係數**：觀察過度正則化 vs 不足正則化的效果
4. **引入獎勵雜訊**：模擬更真實的人類反饋場景
5. **實作 DPO 比較**：在同一環境中對比 RLHF 和 DPO

---

## 延伸閱讀

- [完整程式碼](_code/rlhf_demo.py)
- [PPO 實作詳解](https://www.google.com/search?q=PPO+implementation+from+scratch+python)
- [Bradley-Terry 模型教學](https://www.google.com/search?q=Bradley+Terry+model+tutorial)
