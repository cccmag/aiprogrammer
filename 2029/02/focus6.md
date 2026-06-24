# 隱私保護合成資料（2021-2029）

## 差分隱私到合成隱私

合成資料的一個核心承諾是：使用合成資料可以避免隱私洩漏。但事實上，合成資料如果設計不當仍可能還原真實記錄。

### 2021-2023：差分隱私合成

Dwork 的差分隱私（Differential Privacy, DP）框架被引入合成資料領域。核心想法是在訓練生成模型時加入雜訊，使模型無法記住任何單一記錄。

```python
# 差分隱私雜訊模擬
import random

def dp_noise(epsilon: float, sensitivity: float = 1.0) -> float:
    scale = sensitivity / epsilon
    return random.laplace(0, scale)

def dp_count(records: list, epsilon: float) -> int:
    true_count = len(records)
    noise = int(dp_noise(epsilon))
    return max(0, true_count + noise)

sample = list(range(100))
print(f"真實計數: 100")
print(f"DP 計數 (ε=1.0): {dp_count(sample, 1.0)}")
print(f"DP 計數 (ε=0.1): {dp_count(sample, 0.1)}")
```

主要技術路線包括：
- **DP-GAN**：將 DP 加入 GAN 訓練
- **DP-SGD**：在隨機梯度下降中加入 DP 雜訊
- **Private PGM**：基於圖模型的隱私合成

### 2023-2026：成員推論攻擊

Carlini 等人的研究顯示，即使使用 DP 訓練，LLM 仍可能記憶並輸出訓練資料中的敏感片段。MIA（Membership Inference Attack）成為合成資料安全評估的標準方法。

### 2026-2029：合成隱私標準化

2026 年 NIST 發布隱私保護合成資料指南。主要技術進展：
- **DP 與合成協同**：在合成管線的多個階段加入隱私保護
- **可驗證隱私**：形式化驗證合成資料的隱私保證
- **聯邦合成**：多組織在不共享原始資料的情況下共同訓練合成模型

### 實務對策

1. 合成前：移除直接識別資訊（PII）
2. 合成中：應用差分隱私訓練
3. 合成後：執行 MIA 測試與隱私審計

## 延伸閱讀

- [Differential privacy synthetic data 2021](https://www.google.com/search?q=differential+privacy+synthetic+data+generation+2021)
- [Membership inference attack LLM 2023](https://www.google.com/search?q=membership+inference+attack+LLM+synthetic+data+2023)
- [NIST privacy synthetic data 2026](https://www.google.com/search?q=NIST+privacy+protecting+synthetic+data+guidelines+2026)
