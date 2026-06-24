# 焦點文章 6：神經網路的訓練技巧

## 前言

訓練深度神經網路是一項挑戰，需要各種技巧來提高性能並防止過擬合。本章節介紹常用的訓練技巧與最佳實踐。

## 資料處理

### 資料標準化

將輸入特徵調整到相同 scale：

```python
X = (X - μ) / σ
```

好處：
- 加速收斂
- 避免梯度因尺度差異而大小不一
- 提高模型穩定性

### 資料增強（Data Augmentation）

透過 transformations 增加訓練樣本：
- 圖像：翻轉、旋轉、裁剪、色彩變換
- 文字：同義詞替換、隨機插入
- 音頻：時間偏移、音調變換

## 正則化技術

### L1 正則化

```
L = L₀ + λΣ|w|
```

促進稀疏權重，可用於特徵選擇。

### L2 正則化（Weight Decay）

```
L = L₀ + λΣw²
```

使權重趨於較小值，提高泛化能力。

### Dropout

訓練時隨機「關閉」部分神經元：

```python
# 前向傳播時
h = ReLU(Wx + b)
h = Dropout(h, p=0.5)  # 50% 的神經元設為 0
```

迫使網路學習更魯棒的特征。

### 提前停止（Early Stopping）

監控驗證集誤差，在開始上升時停止訓練：

```python
if val_loss > best_val_loss + patience:
    break
best_val_loss = val_loss
```

## 批次正規化（Batch Normalization）

對每個 mini-batch 進行標準化：

```
μ_B = mean(X)
σ²_B = variance(X)
X_norm = (X - μ_B) / √(σ²_B + ε)
Y = γX_norm + β
```

作用：
- 加速收斂
- 減輕梯度消失
- 提供輕微正則化效果

## 權重初始化

### Xavier 初始化

適合 Sigmoid 和 Tanh：

```python
W = uniform(-√(6/(n_in+n_out)), √(6/(n_in+n_out)))
```

### He 初始化

適合 ReLU：

```python
W = normal(0, √(2/n_in))
```

## 調試技巧

1. **先在小數據集上驗證**：確認模型能擬合訓練數據
2. **使用 TensorBoard/Visdom**：視覺化損失、梯度、權重
3. **Grdient Checking**：數值梯度驗證分析梯度
4. **單因素實驗**：每次只改變一個超參數

## 總結

訓練深度神經網路需要綜合運用多種技巧。從資料预处理、正則化到學習率調整，每個環節都影響最終性能。

## 延伸閱讀

- https://www.google.com/search?q=neural+network+training+tricks+regularization
- https://www.google.com/search?q=batch+normalization+deep+learning