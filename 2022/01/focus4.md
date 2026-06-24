# 啟用函數：Sigmoid、ReLU、GELU

## 為什麼需要啟用函數？

啟用函數（Activation Function）是神經網路中非線性變換的來源。如 focus3 所述，如果沒有非線性啟用函數，多層網路將退化為單層線性模型。

## Sigmoid

Sigmoid 是最早使用的啟用函數之一：

```
σ(x) = 1 / (1 + e^(-x))
```

其輸出範圍在 (0, 1) 之間，適合表示機率。

```
σ(x) 圖形：
1.0 ┤          ▄▄█▄▄
0.8 ┤       ▄█     █▄
0.5 ┤     ▄█         █▄
0.2 ┤   ▄█             █▄
0.0 ┤▄█                  █▄
    └────────────────────
      -4  -2   0   2   4
```

### 優點
- 輸出平滑、可微
- 輸出範圍在 0 到 1 之間，適合機率輸出
- 歷史悠久，理論成熟

### 缺點
- **梯度消失**：在兩端飽和區，梯度接近零
- 非零中心：輸出恆為正，導致梯度更新呈鋸齒狀
- 指數運算計算量大

## Tanh

Tanh 是 Sigmoid 的改良版：

```
tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
```

輸出範圍在 (-1, 1) 之間，是零中心的。

### 優點
- 零中心化，改善梯度更新
- 梯度比 Sigmoid 更陡（梯度更強）

### 缺點
- 仍然有梯度消失問題（兩端飽和）
- 計算量仍然較大

## ReLU

ReLU（Rectified Linear Unit）的出現是深度學習的重大突破：

```
ReLU(x) = max(0, x)
```

```
ReLU 圖形：
f(x)
│
│         ╱
│        ╱
│       ╱
│      ╱
│     ╱
│    ╱
╶───╱────────────────
│   ╱
```

### 優點
- 計算極簡單：只需 max(0, x)
- 不收斂到零（正半軸梯度恒為 1）
- 稀疏啟用：負半軸輸出為零，增加稀疏性
- 經驗上加速收斂

### 缺點
- **Dead ReLU 問題**：如果某個神經元的輸出永遠為負，其梯度為零，將永遠無法恢復
- 非零中心
- 不區分負值的重要性（全部截斷為零）

## GELU

GELU（Gaussian Error Linear Unit）是近年來流行的啟用函數，被 BERT、GPT 等模型廣泛使用：

```
GELU(x) = x · Φ(x)
```

其中 Φ(x) 是標準高斯分布的累積分布函數。實用的近似公式：

```
GELU(x) ≈ 0.5 · x · (1 + tanh(√(2/π) · (x + 0.044715 · x³)))
```

```
GELU vs ReLU 圖形：
f(x)
│
│        GELU ── 平滑曲線
│        ReLU ── 折線
│       ╱╱
│      ╱ ╱
│     ╱  ╱
│    ╱   ╱
╶───╱────╱─────────────
│   ╱   ╱
│  ╱   ╱
│ ╱   ╱
```

### 優點
- 平滑可微，梯度更穩定
- 在負值區域保留資訊（不像 ReLU 直接截斷）
- 在許多現代模型中表現優於 ReLU

### 缺點
- 計算量較大（需要 tanh 或 erf）
- 沒有 ReLU 的稀疏性優勢

## 如何選擇？

| 函數 | 優點 | 缺點 | 適用場景 |
|------|------|------|---------|
| Sigmoid | 機率輸出 | 梯度消失 | 輸出層（二分類） |
| Tanh | 零中心 | 梯度消失 | RNN、舊式架構 |
| ReLU | 高效、稀疏 | Dead ReLU | CNN、隱藏層預設 |
| GELU | 平滑、穩定 | 計算量大 | Transformer、LLM |

### 實戰建議

- **隱藏層預設 ReLU**：對新手最友好，訓練最快
- **嘗試 Leaky ReLU**：解決 Dead ReLU 問題
- **GELU/SwiGLU**：用於大型模型和 Transformer
- **Sigmoid** 僅用於輸出層的二分類
- **Softmax** 用於輸出層的多分類

---

## 延伸閱讀

- [ReLU 論文 2011](https://www.google.com/search?q=Rectified+Linear+Units+Improve+Restricted+Boltzmann+Machines)
- [GELU 論文 2016](https://www.google.com/search?q=Gaussian+Error+Linear+Units+GELU)
- [啟用函數比較](https://www.google.com/search?q=activation+function+comparison+deep+learning)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」歷史回顧系列之一。*
