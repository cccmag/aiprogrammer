# 影像生成與編輯技術（2014-2026）

## 從 GAN 到 Diffusion：生成模型的革命

影像生成是 AI 最引人注目的視覺成就。從 2014 年 GAN 的誕生到 2022 年 Stable Diffusion 的爆發，影像生成從實驗室技術變成了人人可用的工具。

## GAN 時代（2014-2021）

生成對抗網路（GAN）由 Generator 和 Discriminator 互相博弈。貢獻是首次讓 AI 生成逼真圖片，但訓練不穩定（mode collapse）、難以控制內容。

## Diffusion 模型（2020-2026）

擴散模型（Diffusion Model）的直覺是：先將圖片逐步加噪到純雜訊，再學習反向去噪：

```python
def denoise_loop(model, steps=1000):
    """從純雜訊逐步去噪生成圖片"""
    x = np.random.randn(3, 256, 256)
    for t in reversed(range(steps)):
        noise = model(x, t)
        x = (x - noise) / np.sqrt(1 - 0.02)  # 簡化版去噪
    return x
```

## Stable Diffusion 的關鍵架構

2022 年的 Stable Diffusion 將擴散搬到潛在空間（Latent Space），大幅降低計算成本：

```python
def sd_text_to_image(prompt):
    """Stable Diffusion 核心：潛在空間擴散"""
    z = torch.randn(4, 64, 64)       # 潛在雜訊
    text_emb = clip_text_encoder(prompt)
    for t in reversed(range(50)):    # DDIM 加速
        noise = unet(z, t, text_emb)
        z = denoise_step(z, noise, t)
    return vae_decode(z)              # 32×32 → 256×256
```

## 影像編輯技術

生成之外，用自然語言指令編輯圖片（InstructPix2Pix）是更實用的能力：

```python
def edit_image(image, instruction):
    """用文字指令編輯圖片（InstructPix2Pix）"""
    return diffusion_model.generate(
        condition={"input": image, "instruction": instruction}
    )
```

## 影像生成里程碑

| 年份 | 模型 | 創新 |
|------|------|------|
| 2014 | GAN | 生成對抗網路概念 |
| 2015 | DCGAN | 卷積 GAN |
| 2017 | CycleGAN | 無配對的風格轉換 |
| 2018 | StyleGAN | 高解析度人臉生成 |
| 2020 | DDPM | 擴散模型實用化 |
| 2021 | DALL-E | 文字到圖片生成 |
| 2022 | Stable Diffusion | 開源、高效率 |
| 2023 | DALL-E 3 | 精確文字理解 |
| 2024 | Sora | 文字到影片生成 |
| 2025 | 即時生成 | 一秒內生成高品質圖片 |
| 2026 | 多模態編輯 | 同時接受文字+語音+圖片指令 |

## 小結

影像生成從 GAN 的不穩定訓練到 Diffusion 的穩定擴散，再到 DiT（Diffusion Transformer）的統一架構。Stable Diffusion 的開放生態讓全球開發者參與到影像生成革命中。多模態編輯（文字+語音+圖片同時控制）代表了未來的方向。

---

**下一步**：[多模態 Agent](focus7.md)

## 延伸閱讀

- [Stable Diffusion 論文](https://www.google.com/search?q=Stable+Diffusion+High+Resolution+Image+Synthesis+with+Latent+Diffusion+Models)
- [DDPM 論文](https://www.google.com/search?q=Denoising+Diffusion+Probabilistic+Models+paper)
- [InstructPix2Pix 論文](https://www.google.com/search?q=InstructPix2Pix+Learning+to+Follow+Image+Editing+Instructions)
