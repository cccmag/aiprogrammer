# 深度學習最佳化

深度學習的最佳化演算法持續發展。

## 1. 經典優化器

**SGD**：
```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
```

**Adam**：
```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))
```

## 2. 學習率調整

```python
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
```

## 3. 正規化

- L2 正規化：weight_decay 參數
- Dropout：隨機丟棄神經元
- Batch Normalization：批次正規化

---

## 延伸閱讀

- [優化器比較](https://www.google.com/search?q=optimizer+comparison+SGD+Adam+deep+learning)
- [學習率排程](https://www.google.com/search?q=learning+rate+scheduler+pytorch+tutorial)