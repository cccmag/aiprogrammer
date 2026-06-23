# GAN 與對抗訓練

## 1. 引言

生成對抗網路（GAN）由 Ian Goodfellow 於 2014 年提出，是合成資料領域的經典技術。儘管近年擴散模型在影像品質上後來居上，GAN 仍然在特定場景中具有不可取代的優勢，特別是在即時生成和對抗訓練方面。

## 2. GAN 的基本架構

GAN 由兩個神經網路組成：生成器（Generator）和鑑別器（Discriminator）。生成器試圖產生逼真的假資料，鑑別器則試圖分辨真假。兩者透過對抗訓練共同進步。這個「貓捉老鼠」的動態過程正是 GAN 名稱的由來。

## 3. PyTorch 實作

```python
import torch
import torch.nn as nn
import torch.optim as optim

class Generator(nn.Module):
    def __init__(self, latent_dim=100):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256), nn.ReLU(),
            nn.Linear(256, 512), nn.ReLU(),
            nn.Linear(512, 784), nn.Tanh()
        )
    def forward(self, z): return self.model(z)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(784, 512), nn.ReLU(),
            nn.Linear(512, 256), nn.ReLU(),
            nn.Linear(256, 1), nn.Sigmoid()
        )
    def forward(self, x): return self.model(x)
```

訓練時交替最佳化兩個網路：鑑別器最大化分類正確率，生成器最小化鑑別器的正確率。

## 4. 模式坍縮與解決方案

GAN 最常見的問題是模式坍縮（Mode Collapse），生成器只學會產生少數幾種樣本。WGAN-GP 透過梯度懲罰來緩解：

```python
def gradient_penalty(d, real, fake, lambda_gp=10):
    alpha = torch.rand(real.size(0), 1)
    interp = alpha * real + (1 - alpha) * fake
    interp.requires_grad_(True)
    d_interp = d(interp)
    grads = torch.autograd.grad(
        outputs=d_interp, inputs=interp,
        grad_outputs=torch.ones_like(d_interp),
        create_graph=True
    )[0]
    gp = ((grads.norm(2, dim=1) - 1) ** 2).mean()
    return lambda_gp * gp
```

## 5. GAN 在合成資料的應用

| 應用 | 說明 | GAN 變體 |
|------|------|----------|
| 影像到影像 | 衛星圖→地圖 | Pix2Pix |
| 文字到影像 | 文字描述生成圖片 | StackGAN |
| 超解析度 | 低解析→高解析 | SRGAN |

## 6. 結語

GAN 雖然在影像品質上被擴散模型超越，但其對抗訓練的框架思想對合成資料領域影響深遠。理解 GAN 的訓練動態，有助於掌握生成式 AI 的核心原理。

## 延伸閱讀

- [GAN 原始論文](https://www.google.com/search?q=Generative+Adversarial+Nets+Goodfellow)
- [Wasserstein GAN](https://www.google.com/search?q=Wasserstein+GAN+improved+training)
