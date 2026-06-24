# 資料擴增技術

## 為什麼需要資料擴增？

資料擴增（Data Augmentation）是深度學習中最重要的正則化技術之一。透過對訓練資料進行合理變換，可以在不增加真實資料的情況下提升模型的泛化能力。

## 影像資料擴增

### torchvision.transforms

PyTorch 透過 torchvision 提供豐富的影像擴增功能：

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomRotation(degrees=15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])
```

### 先進擴增技術

**MixUp**：將兩張圖片按比例混合：
```python
def mixup(x, y, alpha=0.2):
    lam = np.random.beta(alpha, alpha)
    index = torch.randperm(x.size(0))
    mixed_x = lam * x + (1 - lam) * x[index]
    mixed_y = lam * y + (1 - lam) * y[index]
    return mixed_x, mixed_y
```

**CutMix**：將一張圖片的區域貼到另一張圖片上。

## 文字資料擴增

NLP 領域的資料擴增方法包括：
- 同義詞替換（Synonym Replacement）
- 隨機插入／刪除（Random Insertion/Deletion）
- 回譯（Back Translation）
- EDA（Easy Data Augmentation）

```python
# 使用 Hugging Face 進行回譯
from transformers import pipeline
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-zh-en")
back_translated = translator("這是一句話")[0]['translation_text']
```

## 訊號資料擴增

- 加入高斯雜訊
- 時間拉伸／壓縮
- 頻率遮蔽（SpecAugment）
- 隨機平移

## Albumentations 函式庫

Albumentations 是專業的影像擴增函式庫，速度比 torchvision 更快：

```python
import albumentations as A
transform = A.Compose([
    A.RandomCrop(256, 256),
    A.HorizontalFlip(p=0.5),
    A.GaussNoise(var_limit=(10, 50)),
])
```

## 實踐建議

1. 驗證擴增後的資料仍然保留原始標籤資訊
2. 在訓練初期先不使用過強擴增
3. 測試時不使用擴增（僅使用標準化）
4. 擴增超參數可以透過驗證集調整

## 參考資料

- torchvision.transforms：https://pytorch.org/vision/stable/transforms.html
- Albumentations：https://albumentations.ai/
- MixUp 論文：https://arxiv.org/abs/1710.09412
- EDA 論文：https://arxiv.org/abs/1901.11196
