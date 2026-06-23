# 影片理解與時序建模

## 前言

影片理解是將靜態圖片理解擴展到時間維度的挑戰。與單張圖片不同，影片包含連續的幀序列，模型需要捕捉時間動態、動作變化以及長程依賴關係。本文將介紹影片理解的核心技術，從 3D CNN 到 Video Transformer，並提供 Python 實作範例。

---

## 一、影片資料的表示

影片可以視為 \( T \times H \times W \times C \) 的張量（T 幀、高 H、寬 W、通道 C）。取樣策略對模型表現至關重要：

```python
import torch
import cv2
import numpy as np

def sample_frames(video_path, num_frames=16):
    """均勻取樣 num_frames 幀"""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

    frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (224, 224))
            frames.append(frame)

    cap.release()
    return torch.tensor(np.stack(frames)).permute(3, 0, 1, 2)
    # 回傳形狀: (C, T, H, W)
```

## 二、3D CNN

3D CNN 將 2D 卷積擴展為 3D，在空間和時間維度同時進行卷積：

```python
import torch.nn as nn

class Simple3DCNN(nn.Module):
    def __init__(self, num_classes=400):
        super().__init__()
        self.conv1 = nn.Conv3d(3, 64, kernel_size=(3, 3, 3), padding=1)
        self.bn1 = nn.BatchNorm3d(64)
        self.pool1 = nn.MaxPool3d((1, 2, 2))

        self.conv2 = nn.Conv3d(64, 128, kernel_size=(3, 3, 3), padding=1)
        self.bn2 = nn.BatchNorm3d(128)
        self.pool2 = nn.MaxPool3d((2, 2, 2))

        self.conv3 = nn.Conv3d(128, 256, kernel_size=(3, 3, 3), padding=1)
        self.bn3 = nn.BatchNorm3d(256)
        self.pool3 = nn.MaxPool3d((2, 2, 2))

        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool3d((1, 1, 1)),
            nn.Flatten(),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        # x: (batch, C, T, H, W)
        x = self.pool1(torch.relu(self.bn1(self.conv1(x))))
        x = self.pool2(torch.relu(self.bn2(self.conv2(x))))
        x = self.pool3(torch.relu(self.bn3(self.conv3(x))))
        return self.classifier(x)
```

## 三、Two-Stream 架構

Two-Stream 網路分別處理 RGB 幀（外觀）和光流（運動）：

```python
class TwoStreamVideoNet(nn.Module):
    def __init__(self, num_classes=400):
        super().__init__()
        # RGB 流：捕捉外觀
        self.rgb_stream = Simple3DCNN(num_classes)
        # 光流流：捕捉運動
        self.flow_stream = Simple3DCNN(num_classes)
        # 融合
        self.fusion = nn.Linear(num_classes * 2, num_classes)

    def forward(self, rgb_frames, flow_frames):
        rgb_out = self.rgb_stream(rgb_frames)
        flow_out = self.flow_stream(flow_frames)
        combined = torch.cat([rgb_out, flow_out], dim=1)
        return self.fusion(combined)
```

## 四、Video Transformer

Vision Transformer（ViT）的影片版本——Video Vision Transformer（ViViT）——將時空資訊編碼為 token 序列：

```python
class VideoPatchEmbed(nn.Module):
    """將影片切分為時空 patch"""
    def __init__(self, patch_size_t=2, patch_size_h=16, patch_size_w=16,
                 in_channels=3, embed_dim=768):
        super().__init__()
        self.patch_size = (patch_size_t, patch_size_h, patch_size_w)
        self.proj = nn.Conv3d(
            in_channels, embed_dim,
            kernel_size=self.patch_size, stride=self.patch_size
        )

    def forward(self, x):
        # x: (B, C, T, H, W)
        x = self.proj(x)  # (B, D, T', H', W')
        x = x.flatten(2).transpose(1, 2)  # (B, num_patches, D)
        return x

class VideoTransformer(nn.Module):
    def __init__(self, embed_dim=768, depth=12, num_heads=12, num_classes=400):
        super().__init__()
        self.patch_embed = VideoPatchEmbed(embed_dim=embed_dim)
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.randn(1, 1 + 196, embed_dim))  # 假設 14x14 patches
        self.blocks = nn.ModuleList([
            nn.TransformerEncoderLayer(embed_dim, num_heads, batch_first=True)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        x = self.patch_embed(x)
        cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        x = x + self.pos_embed[:, :x.size(1)]
        for block in self.blocks:
            x = block(x)
        x = self.norm(x[:, 0])
        return self.head(x)
```

## 五、動作辨識實戰

使用預訓練模型進行動作辨識：

```python
def classify_action(video_path, model, class_names):
    frames = sample_frames(video_path, num_frames=16).unsqueeze(0)
    with torch.no_grad():
        logits = model(frames)
        pred_idx = logits.argmax(dim=1).item()
    return class_names[pred_idx]

# 範例：使用 Kinetics-400 類別
kinetics_classes = ["跑步", "跳躍", "游泳", "彈鋼琴", "煮飯"]
result = classify_action("test_video.mp4", model, kinetics_classes)
```

---

## 結語

影片理解從 3D CNN、Two-Stream 到 Video Transformer，技術演進反映了從手工設計時序特徵到端到端學習的趨勢。隨著 Sora、VideoPoet 等影片生成模型的出現，影片理解與生成正在走向統一。掌握時序建模的核心技術，對於建構下一代多模態 AI 系統至關重要。

---

**參考資料**

- ViViT 論文：https://arxiv.org/abs/2103.15691
- Two-Stream 論文：https://arxiv.org/abs/1406.2199
- Kinetics 資料集：https://www.google.com/search?q=Kinetics+dataset+video+understanding
- Sora 技術報告：https://openai.com/index/video-generation-models-as-world-simulators
