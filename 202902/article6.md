# 差分隱私合成資料

## 1. 引言

當合成資料涉及個人隱私時，單純的生成是不夠的——還必須確保合成資料不會洩漏原始資料中的敏感資訊。差分隱私（Differential Privacy, DP）提供了嚴格的數學框架，保證合成資料的隱私保護程度。本文探討如何在合成資料中導入差分隱私機制。

## 2. 差分隱私的核心概念

差分隱私的核心思想是：在資料中引入可控的雜訊，使得任何單一個體的加入或移除，對最終結果的影響都是有限的。形式化定義為：一個隨機演算法 M 滿足 ε-差分隱私，若對任意相鄰資料集 D 和 D'，以及任意輸出 S，有：

`Pr[M(D) ∈ S] ≤ e^ε × Pr[M(D') ∈ S]`

其中 ε 稱為隱私預算，值越小隱私保護越強。

## 3. 隱私預算管理

對梯度加入高斯雜訊並進行梯度裁剪，是 DP-SGD 的核心做法：

```python
import numpy as np

class PrivacyAccountant:
    def __init__(self, epsilon: float, delta: float = 1e-5):
        self.epsilon = epsilon
        self.delta = delta

    def compute_noise_scale(self, batch_size: int, epochs: int,
                            total_samples: int) -> float:
        q = batch_size / total_samples
        steps = epochs * (total_samples / batch_size)
        return max(q * np.sqrt(steps * np.log(1 / self.delta)) / self.epsilon, 1.0)

    def add_noise(self, gradients: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(gradients)
        clip = gradients / max(1, norm)
        noise = np.random.normal(0, 1.0, size=gradients.shape)
        return clip + noise

accountant = PrivacyAccountant(epsilon=8.0)
noise_scale = accountant.compute_noise_scale(64, 50, 60000)
print(f"雜訊尺度：{noise_scale:.4f}")
```

## 4. 隱私與效用的權衡

| 隱私預算 ε | 隱私保護 | 資料效用 | 典型應用 |
|-----------|---------|---------|---------|
| 0.1-1.0 | 極強 | 低 | 醫療資料 |
| 1.0-8.0 | 中等 | 中 | 一般用途 |
| > 8.0 | 弱 | 高 | 公開統計 |

## 6. 結語

差分隱私為合成資料提供了可量化的隱私保證。雖然高強度隱私保護會降低資料效用，但對於醫療、金融等敏感領域，DP 合成資料是目前少數可行的方案。

## 延伸閱讀

- [Differential Privacy 概述](https://www.google.com/search?q=differential+privacy+explained+simple)
- [DP-SGD 演算法](https://www.google.com/search?q=DP-SGD+differentially+private+stochastic+gradient+descent)
