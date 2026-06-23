# 領域適應合成資料

## 1. 引言

機器學習模型在域外資料上常常表現不佳——這個問題稱為領域偏移（Domain Shift）。領域適應（Domain Adaptation）透過將知識從標註豐富的源域遷移到目標域來解決這個問題。合成資料在其中扮演關鍵角色：我們可以合成目標域的標註資料來進行微調。

## 2. 領域適應的問題設定

想像在白天拍攝的照片上訓練的車牌辨識模型，部署到夜間場景時準確率暴跌。解決方案之一是使用合成引擎生成夜間車牌影像，用這些合成資料來適應模型。

## 3. 風格轉換合成

```python
import torch
import torch.nn as nn
from torchvision import transforms

class AdaptiveInstanceNorm(nn.Module):
    """自適應實例正規化，用於風格轉換"""
    def __init__(self, channels: int):
        super().__init__()
        self.instance_norm = nn.InstanceNorm2d(channels)

    def forward(self, x: torch.Tensor,
                style_mean: torch.Tensor,
                style_std: torch.Tensor) -> torch.Tensor:
        # 標準化內容特徵
        normalized = self.instance_norm(x)
        # 用風格特徵重新縮放
        return normalized * style_std + style_mean

def apply_style_transfer(
    content: torch.Tensor,
    style_loader
) -> torch.Tensor:
    """將內容影像轉換為目標風格"""
    # 收集一批風格影像的統計資訊
    style_features = []
    for style_img in style_loader:
        # 使用預訓練 VGG 提取特徵
        style_features.append(style_img)
    style_stats = {
        "mean": torch.stack([f.mean([2, 3]) for f in style_features]).mean(0),
        "std": torch.stack([f.std([2, 3]) for f in style_features]).mean(0)
    }
    adain = AdaptiveInstanceNorm(content.shape[1])
    return adain(content, style_stats["mean"], style_stats["std"])
```

## 4. 領域隨機化

領域隨機化（Domain Randomization）是合成資料領域適應的強大技術。其核心思想是在合成過程中隨機化所有非關鍵參數，迫使模型學習真正重要的特徵。

```python
import random
from PIL import Image, ImageFilter, ImageEnhance

def domain_randomize(img: Image.Image) -> Image.Image:
    if random.random() < 0.5:
        img = ImageEnhance.Brightness(img).enhance(random.uniform(0.5, 1.5))
    if random.random() < 0.5:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0, 2)))
    if random.random() < 0.3:
        import numpy as np
        arr = np.array(img) + np.random.normal(0, 15, np.array(img).shape)
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img
```

## 5. 自訓練與偽標籤

自訓練（Self-training）是另一個重要策略：先用源域模型對目標域無標籤資料進行預測，保留高信度的偽標籤作為訓練資料，然後在混合資料上重新訓練模型。

## 6. 結語

合成資料在領域適應中扮演雙重角色：一方面是生成目標域的模擬資料，另一方面透過領域隨機化提升模型的泛化能力。關鍵在於掌握合成資料與真實資料之間的「語意差距」，並透過策略性的隨機化來橋接這個差距。

## 延伸閱讀

- [Domain Randomization 概念](https://www.google.com/search?q=domain+randomization+synthetic+data)
- [Unsupervised Domain Adaptation](https://www.google.com/search?q=unsupervised+domain+adaptation+survey)
