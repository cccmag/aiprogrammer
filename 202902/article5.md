# 資料擴增策略比較

## 1. 引言

資料擴增（Data Augmentation）是解決資料稀缺問題最直接的方法。從早期的幾何變換到現代的生成式擴增，各種策略在不同場景下各有優劣。本文透過系統性比較與實作，幫助讀者選擇適合的擴增策略。

## 2. 基礎變換

```python
import torchvision.transforms as T
basic_augment = T.Compose([
    T.RandomHorizontalFlip(p=0.5),
    T.RandomRotation(degrees=15),
    T.ColorJitter(brightness=0.2, contrast=0.2),
    T.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)),
])
```

文字領域可搭配 EDA（Easy Data Augmentation）進行同義詞替換與隨機插入。

## 3. 混合式擴增

混合式擴增透過融合多個樣本產生新資料：

```python
def mixup(x1: torch.Tensor, x2: torch.Tensor,
          y1: torch.Tensor, y2: torch.Tensor,
          alpha: float = 1.0):
    """MixUp 資料擴增"""
    lam = torch.distributions.Beta(alpha, alpha).sample()
    x_mixed = lam * x1 + (1 - lam) * x2
    y_mixed = lam * y1 + (1 - lam) * y2
    return x_mixed, y_mixed

def cutmix(x1: torch.Tensor, x2: torch.Tensor,
           y1: torch.Tensor, y2: torch.Tensor):
    """CutMix 資料擴增"""
    lam = torch.distributions.Beta(1.0, 1.0).sample()
    _, h, w = x1.shape[1:]
    cut_w = int(w * (1 - lam).sqrt())
    cut_h = int(h * (1 - lam).sqrt())
    cx, cy = torch.randint(w, (1,))[0], torch.randint(h, (1,))[0]
    x1[:, :, cy-cut_h//2:cy+cut_h//2, cx-cut_w//2:cx+cut_w//2] = \
        x2[:, :, cy-cut_h//2:cy+cut_h//2, cx-cut_w//2:cx+cut_w//2]
    y_mixed = lam * y1 + (1 - lam) * y2
    return x1, y_mixed
```

## 3. 策略比較

| 策略 | 計算成本 | 多樣性 | 語意保留 | 適用場景 |
|------|---------|--------|---------|---------|
| 基礎變換 | 低 | 低 | 高 | 影像分類 |
| 混合式 | 低 | 中 | 中 | 一般任務 |
| 生成式 | 高 | 高 | 高 | 資料稀缺 |
| 對抗式 | 中 | 高 | 低 | 穩健訓練 |

## 4. 自動擴增搜尋

```python
# 使用 AutoAugment 策略
from torchvision.transforms import AutoAugment, AutoAugmentPolicy

auto_augment = AutoAugment(
    policy=AutoAugmentPolicy.IMAGENET
)
```

AutoAugment 透過強化學習搜尋最佳的擴增組合，在 ImageNet 上取得了顯著的增益。

## 5. 選擇指南

選擇擴增策略的建議流程：

1. **資料量不足**：首選基礎變換，成本最低
2. **類別不平衡**：對少數類別使用生成式擴增
3. **過擬合**：逐步增加擴增強度，觀測驗證損失
4. **分佈偏移**：使用與目標域相關的生成式擴增

## 6. 結語

沒有萬能的擴增策略。選擇時需考慮資料型態、任務性質和計算預算。建議從最簡單的基礎變換開始，逐步嘗試更複雜的方法。

## 延伸閱讀

- [AutoAugment 論文](https://www.google.com/search?q=AutoAugment+learning+augmentation+policies)
- [EDA 文字擴增](https://www.google.com/search?q=EDA+easy+data+augmentation+text+classification)
