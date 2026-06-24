# 影像增強技巧

資料增強是提高模型泛化能力的重要技術。

## 1. 隨機變換

```python
from torchvision import transforms

transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor()
])
```

## 2. Cutout 和 MixUp

```python
class Cutout:
    def __init__(self, n_holes=1, length=16):
        self.n_holes = n_holes
        self.length = length

    def __call__(self, img):
        h, w = img.size(1), img.size(2)
        mask = torch.ones((h, w))

        for _ in range(self.n_holes):
            y = random.randint(0, h)
            x = random.randint(0, w)
            y1 = max(0, y - self.length // 2)
            y2 = min(h, y + self.length // 2)
            x1 = max(0, x - self.length // 2)
            x2 = min(w, x + self.length // 2)
            mask[y1:y2, x1:x2] = 0

        return img * mask
```

## 3. 測試時增強 (TTA)

在推理時使用多個 augmentations 然後平均結果。

---

## 延伸閱讀

- [資料增強綜述](https://www.google.com/search?q=data+augmentation+computer+vision+techniques)
- [MixUp+增強](https://www.google.com/search?q=mixup+data+augmentation+ regularization)