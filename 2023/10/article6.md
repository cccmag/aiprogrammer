# 結構風險最小化 SRM

## 從 ERM 到 SRM

ERM 的關鍵問題是如何選擇 H。**太小**則欠擬合，**太大**則過擬合。交叉驗證是一種實踐解法，但缺乏理論指導。

結構風險最小化（Structural Risk Minimization，SRM）是 Vapnik 提出的替代框架。它不是選擇一個固定的 H，而是在一個嵌套的假說空間序列中**自動選擇**最優的複雜度。

## SRM 的定義

SRM 考慮一個嵌套的假說空間序列：

```
H₁ ⊂ H₂ ⊂ H₃ ⊂ ... ⊂ H_k ⊂ ...
```

其中每個 H_k 的 VC 維度 d_k 滿足 d₁ < d₂ < d₃ < ...。

SRM 選擇最小化結構風險的模型：

```
k* = argmin_k [ R̂(ĥ_k) + Φ(d_k / n, δ/n) ]
```

其中 Φ 是複雜度懲罰，ĥ_k 是 H_k 中的 ERM 解。

### 結構風險的組成

```
結構風險 = 經驗風險 + 置信區間
```

- **經驗風險**：在訓練資料上的誤差（隨 k 增加而遞減）
- **置信區間**：泛化誤差的上界（隨 k 增加而遞增）

最佳點在兩者之和的最小值處。

## 常見的複雜度懲罰

| 準則 | 懲罰項 | 形式 |
|------|--------|------|
| VC-SRM | Φ = √(d/n * log(n/d + 1)) | Vapnik 原始 |
| AIC | Φ = d/n | Akaike |
| BIC | Φ = (d/2) * log(n)/n | Schwarz |
| MDL | Φ = (d/2) * log(n)/n | Rissanen |

### AIC vs BIC 的哲學差異

**AIC**（Akaike Information Criterion）基於資訊理論，目標是最小化預測誤差：

```
AIC = R̂(h) + d/n
```

**BIC**（貝氏資訊準則）基於貝氏模型比較，目標是找到最可能的模型：

```
BIC = n*R̂(h) + (d/2)*log(n)
```

- AIC 傾向選擇更複雜的模型（懲罰較輕）
- BIC 傾向選擇更簡單的模型（懲罰較重，尤其是 n 很大時）

## SRM 的理論保證

SRM 最重要的理論結果是：**SRM 在 VC 維度有限時是一致的**。

更精確地說，對任意 ε > 0，當 n → ∞ 時：

```
P[R(ĥ_SRM) > inf_{k} inf_{h∈H_k} R(h) + ε] → 0
```

此外，SRM 提供了**非漸近的**泛化保證——對有限 n，我們有明確的誤差上界。

## SRM 的實作

```python
def SRM(X, y, hypothesis_classes, vc_dims, delta=0.05):
    n = len(y)
    best_h = None
    best_risk = float('inf')
    
    for H, d in zip(hypothesis_classes, vc_dims):
        h = ERM(X, y, H)
        R_emp = empirical_risk(h, X, y)
        # VC 置信區間
        phi = np.sqrt(d/n * np.log(n/d + 1) + np.log(1/delta)/(2*n))
        struct_risk = R_emp + phi
        
        if struct_risk < best_risk:
            best_risk = struct_risk
            best_h = h
    
    return best_h
```

## SRM 的實際範例

### SVM 中的 SRM

SVM 是 SRM 的實際體現。在 SVM 中：

- H_k = {sign(w·x + b) | ||w|| ≤ C_k}
- 較小的 ||w|| 對應較小的有效 VC 維度
- 最大化間隔 = 最小化結構風險

### 正則化路徑

Lasso 和 Ridge 的正則化路徑可以視為 SRM 的連續版本：

```
隨著 λ 從大到小變化，有效模型複雜度逐漸增加
SRM 選擇 λ 使得結構風險最小
```

## SRM vs 交叉驗證

| 方法 | 優點 | 缺點 |
|------|------|------|
| SRM | 理論保證，無需驗證集 | 需要計算 VC 維度 |
| 交叉驗證 | 無需理論計算 | 計算成本高、無理論保證 |

## 小結

SRM 是學習理論從 ERM 的自然延伸：

| 概念 | ERM | SRM |
|------|-----|-----|
| 選擇 | 固定 H 中的最優 h | 選擇最優的 H_k 和 h |
| 風險 | R̂(h) | R̂(h) + Φ(d/n) |
| 複雜度控制 | 隱式（選擇 H）| 顯式（$Phi 懲罰）|
| 理論基礎 | Uniform 收斂 | VC 維度 + 結構 |

## 延伸閱讀

- [Structural Risk Minimization](https://www.google.com/search?q=structural+risk+minimization+Vapnik)
- [SRM vs ERM](https://www.google.com/search?q=SRM+vs+ERM+machine+learning)
- [AIC vs BIC](https://www.google.com/search?q=AIC+vs+BIC+model+selection)
