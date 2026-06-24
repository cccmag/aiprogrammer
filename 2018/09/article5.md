# 影像分類競賽常用技巧

## 1. Ensemble

```python
# 訓練多個模型，預測結果投票或平均
predictions = []
for model in models:
    pred = model.predict(x_test)
    predictions.append(pred)

# 平均
final_pred = np.mean(predictions, axis=0)

# 投票
final_pred = np.argmax(np.sum(predictions, axis=0), axis=1)
```

## 2. Test-Time Augmentation (TTA)

```python
# 測試時對同一張圖的多個增強版本預測
def predict_with_tta(model, image, num_aug=5):
    predictions = []
    for _ in range(num_aug):
        augmented = augment(image)
        pred = model.predict(augmented)
        predictions.append(pred)
    return np.mean(predictions, axis=0)
```

## 3. 學習率循環（Cyclical Learning Rate）

```python
from keras.callbacks import CyclicLR

clr = CyclicLR(
    base_lr=1e-5,
    max_lr=1e-3,
    step_size=len(train_loader) * 2,
    mode='triangular2'
)

model.fit(X_train, y_train, callbacks=[clr])
```

## 4. Snapshot Ensemble

```python
# 在學習率週期的不同峰值點保存模型
# 最後集成多個 snapshot
```

## 5. 2018 年 Kaggle 競賽技巧

| 競賽類型 | 常用技巧 |
|----------|----------|
| 影像分類 | Ensemble, TTA, Pseudo-labeling |
| 物體偵測 | Multi-scale, OHEM, FPN |
| 語義分割 | Multi-scale, CRF, Auxiliary Loss |

## 6. 小結

競賽中的技巧核心是提升模型多樣性和預測穩定性。Ensemble 和 TTA 是最基礎且有效的兩個技巧。

---

**參考資料**
- [Kaggle Competition Tips](https://www.google.com/search?q=Kaggle+image+classification+tips+2018)
- [TTA Test Time Augmentation](https://www.google.com/search?q=test+time+augmentation+deep+learning)