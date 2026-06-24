# 影像生成：從 Diffusion 到 DiT

## 前言

影像生成是近年 AI 領域進展最快的方向之一。從 2020 年的 DDPM 到 Stable Diffusion，再到 2024 年的 DiT（Diffusion Transformer），模型架構經歷了從 CNN 到 Transformer 的重大轉變。本文將探討 Diffusion 模型的核心原理，並介紹 DiT 這一新世代架構。

---

## 一、Diffusion 模型基礎

擴散模型包含兩個過程：前向擴散（逐步添加雜訊）和反向去噪（逐步去除雜訊）：

```python
import torch
import torch.nn.functional as F

def forward_diffusion(x0, t, noise_schedule):
    """前向擴散：從 x0 逐步添加雜訊到 xt"""
    alpha_cumprod = noise_schedule["alpha_cumprod"][t]
    noise = torch.randn_like(x0)
    xt = torch.sqrt(alpha_cumprod) * x0 + torch.sqrt(1 - alpha_cumprod) * noise
    return xt, noise

def p_losses(denoise_model, x0, t, noise_schedule):
    """計算去雜訊模型的預測損失"""
    xt, noise = forward_diffusion(x0, t, noise_schedule)
    noise_pred = denoise_model(xt, t)
    return F.mse_loss(noise_pred, noise)
```

## 二、簡化的 UNet 去噪器

傳統 Diffusion 使用 UNet 作為去噪網路：

```python
import torch.nn as nn

class SimpleUNet(nn.Module):
    def __init__(self, in_channels=3):
        super().__init__()
        self.down = nn.Sequential(
            nn.Conv2d(in_channels, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, padding=1, stride=2),
            nn.ReLU(),
        )
        self.mid = nn.Sequential(
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(),
        )
        self.up = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, in_channels, 3, padding=1),
        )

    def forward(self, x, t):
        # t 是時間步，在此簡化版本中未使用
        x = self.down(x)
        x = self.mid(x)
        x = self.up(x)
        return x
```

## 三、取樣（反向去噪）

```python
@torch.no_grad()
def sample(model, image_size, channels, noise_schedule, steps=100):
    model.eval()
    x = torch.randn(1, channels, image_size, image_size)

    for t in reversed(range(steps)):
        t_tensor = torch.full((1,), t, dtype=torch.long)
        noise_pred = model(x, t_tensor)

        alpha = noise_schedule["alpha"][t]
        alpha_cumprod = noise_schedule["alpha_cumprod"][t]

        if t > 0:
            noise = torch.randn_like(x)
        else:
            noise = 0

        x = (1 / torch.sqrt(alpha)) * (
            x - (1 - alpha) / torch.sqrt(1 - alpha_cumprod) * noise_pred
        ) + torch.sqrt(1 - alpha) * noise

    return x.clamp(-1, 1)
```

## 四、DiT：Diffusion Transformer

DiT（Diffusion Transformer）用 Transformer 取代 UNet，核心創新在於將雜訊圖片切分成 patch，並將時間步和條件資訊作為 token 輸入：

```python
class DiTBlock(nn.Module):
    """DiT 的基本模塊：自注意力 + 交叉注意力 + FFN"""
    def __init__(self, dim, num_heads=8):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = nn.MultiheadAttention(dim, num_heads, batch_first=True)
        self.norm2 = nn.LayerNorm(dim)
        self.ffn = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.GELU(),
            nn.Linear(dim * 4, dim),
        )
        self.adaLN = nn.Sequential(
            nn.SiLU(),
            nn.Linear(dim, dim * 6),
        )

    def forward(self, x, c):
        # c 為條件嵌入（時間步 + class label）
        shift_msa, scale_msa, gate_msa, shift_mlp, scale_mlp, gate_mlp = \
            self.adaLN(c).chunk(6, dim=-1)

        x = x + gate_msa * self.attn(
            *self.norm1(x).chunk(3, dim=-1)  # QKV split
        )[0]

        x = x + gate_mlp * self.ffn(self.norm2(x))
        return x
```

## 五、Stable Diffusion 的關鍵：潛空間擴散

Stable Diffusion 不是在像素空間擴散，而是在 VAE 的潛空間中進行，大幅降低了計算成本：

```python
class StableDiffusionPipeline:
    def __init__(self, vae, unet, clip_text_encoder):
        self.vae = vae
        self.unet = unet
        self.text_encoder = clip_text_encoder

    @torch.no_grad()
    def generate(self, prompt, num_steps=50, guidance_scale=7.5):
        # 文字編碼
        text_emb = self.text_encoder(prompt)

        # 初始化潛變數
        latents = torch.randn(1, 4, 64, 64)

        # 在潛空間中進行擴散去噪
        for t in self.scheduler.timesteps:
            noise_pred = self.unet(latents, t, text_emb)
            latents = self.scheduler.step(noise_pred, t, latents)

        # VAE 解碼回像素空間
        image = self.vae.decode(latents)
        return image
```

---

## 結語

從 UNet 到 DiT，Diffusion 模型的進化反映了 AI 領域的整體趨勢：用 Transformer 統一所有架構。DiT 證明了 Transformer 在影像生成領域的潛力，後續的 Sora 等影片生成模型也延續了這條技術路線。理解 Diffusion 和 DiT 的原理，是掌握當前影像生成技術的關鍵。

---

**參考資料**

- DDPM 論文：https://arxiv.org/abs/2006.11239
- DiT 論文：https://arxiv.org/abs/2212.09748
- Stable Diffusion：https://github.com/CompVis/stable-diffusion
- Diffusion 模型綜述：https://www.google.com/search?q=diffusion+models+survey+2024
