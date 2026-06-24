# 正則化理論

## 為什麼需要正則化？

正則化（Regularization）是控制模型複雜度、防止過擬合的核心技術。從偏差-變異的角度看，正則化通過增加偏差來換取變異的更大降低。

從學習理論的角度，正則化對應於**對假說空間施加限制**——縮小 H 的大小或降低其 VC 維度。

## 正則化的數學形式

標準的正則化經驗風險最小化（RERM）：

```
ĥ = argmin_{h∈H} [ R̂(h) + λΩ(h) ]
```

其中：
- R̂(h) 是經驗風險（資料擬合項）
- Ω(h) 是正則化項（複雜度懲罰）
- λ ≥ 0 是正則化參數（控制權衡強度）

### 常見的正則化項

| 正則化 | Ω(h) | 特點 |
|--------|------|------|
| L2（Ridge） | ||w||²₂ | 均勻收縮 |
| L1（Lasso） | ||w||₁ | 稀疏解 |
| Elastic Net | α||w||₁ + (1-α)||w||²₂ | 兩者兼顧 |
| Dropout | — | 隱式集成 |

## L2 正則化（Ridge）

L2 正則化在線性回歸中對應於 Ridge Regression：

```
J(w) = (1/n)||Xw - y||² + λ||w||²₂
```

**閉式解**：ŵ = (X^T X + λI)^{-1} X^T y

L2 正則化的效果是所有權重都向零收縮，但不會完全變零。當 λ 越大時，收縮越強。

### 從貝氏角度看

L2 正則化對應於高斯先驗：

```
p(w) = N(0, (2λ)^{-1}I)
```

Ridge 回歸的 MAP 估計：

```
ŵ = argmax log p(y|X,w) + log p(w)
```

## L1 正則化（Lasso）

L1 正則化對應於 Lasso（Least Absolute Shrinkage and Selection Operator）：

```
J(w) = (1/n)||Xw - y||² + λ||w||₁
```

L1 的關鍵特性是**產生稀疏解**——許多權重正好為零。

### L1 產生稀疏解的直觀解釋

L1 正則化的約束區域是菱形（L1 ball），L2 是圓形。菱形有尖角位於坐標軸上，最優解容易落在這些尖角上，對應於某些權重為零。

```
L2：圓形約束 → 解在邊界任意位置
L1：菱形約束 → 解傾向於在頂點（坐標軸上）
```

## λ 的選擇

正則化參數 λ 是學習者需要設定的關鍵超參數。

**太大**（λ → ∞）：模型完全忽略資料，僅最小化 Ω(h)
**太小**（λ → 0）：回歸 ERM，可能過擬合
**適中**：平衡擬合與複雜度

選擇方法：
- 交叉驗證（Cross-validation）
- 驗證集（Validation set）
- AIC/BIC 準則
- 結構風險最小化

## 正則化與 VC 維度

正則化可以被理解為降低有效 VC 維度。對於 L2 正則化的線性模型，有效自由度為：

```
d_eff = Σ σ_i² / (σ_i² + λ)
```

其中 σ_i 是資料矩陣的奇異值。當 λ → 0 時，d_eff → d。當 λ → ∞ 時，d_eff → 0。

## 隱式正則化

並非所有正則化都是顯式的。以下機制也提供正則化效果：

| 機制 | 說明 |
|------|------|
| SGD | 隨機梯度的雜訊提供正則化 |
| Early Stopping | 提前終止訓練等同於 L2 正則化 |
| Data Augmentation | 透過虛擬樣本擴展訓練集 |
| Dropout | 隨機丟棄神經元 |
| Batch Normalization | 減少內部協變量偏移 |

## 小結

正則化是機器學習實踐中最強大的工具之一：

| 方法 | 形式 | 效果 |
|------|------|------|
| L2 | λ||w||² | 均勻收縮權重 |
| L1 | λ||w||₁ | 稀疏解 |
| Dropout | 隨機丟棄 | 隱式集成 |
| Early Stopping | 提前終止 | 限制迭代次數 |

---

**下一步**：[核方法與再生核 Hilbert 空間](focus6.md)

## 延伸閱讀

- [Regularization in Machine Learning](https://www.google.com/search?q=regularization+machine+learning+overview)
- [L1 vs L2 Regularization](https://www.google.com/search?q=L1+vs+L2+regularization+difference)
- [Understanding Lasso and Ridge](https://www.google.com/search?q=understanding+Lasso+Ridge+regression)
