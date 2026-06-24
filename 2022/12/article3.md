# DALL-E 2 與 Stable Diffusion

## 生成式 AI 的視覺革命

2022 年，AI 繪圖從實驗室技術一躍成為大眾產品。DALL-E 2 和 Stable Diffusion 代表了這場革命的兩條不同路線——前者追求最高品質，後者追求最大普及度。

## 擴散模型的原理

兩者都基於擴散模型（Diffusion Model），其核心思想是學習從雜訊還原影像的過程：

### 前向擴散過程

從一張清晰的影像開始，逐步加入雜訊，直到完全變成隨機雜訊。這個過程是固定的，不需要學習。

### 反向去噪過程

從隨機雜訊開始，逐步預測並去除雜訊，最終還原出清晰的影像。神經網路學習的就是這個反向過程。

```python
# 簡化的擴散去噪步驟
def denoise_step(model, noisy_image, t, text_embedding):
    predicted_noise = model(noisy_image, t, text_embedding)
    # 去除預測的雜訊
    denoised = remove_noise(noisy_image, predicted_noise, t)
    return denoised

# 完整生成過程
def generate(model, text_prompt, steps=50):
    text_embedding = clip_encode(text_prompt)
    x = torch.randn(1, 3, 512, 512)  # 隨機雜訊
    for t in reversed(range(steps)):
        x = denoise_step(model, x, t, text_embedding)
    return x
```

## DALL-E 2 的技術架構

DALL-E 2 採用兩階段生成架構：

### 第一階段：先驗模型（Prior）

將 CLIP 文字編碼器的輸出轉換為 CLIP 影像編碼器的嵌入向量。這是一個基於 Transformer 的生成模型，學習文字和影像之間的語義映射。

### 第二階段：去噪解碼器（Decoder）

使用擴散模型將影像嵌入向量解碼為最終像素。這個階段負責高品質影像的生成。

### DALL-E 2 的關鍵能力

- **文字渲染**：可以在影像中生成文字
- **風格遷移**：在給定風格下生成新影像
- **影像編輯**：基於文字修改現有影像
- **變化生成**：對同一提示生成多種變化

## Stable Diffusion 的技術突破

Stable Diffusion 的關鍵創新是將擴散過程從像素空間轉移到潛在空間（Latent Space）：

### 潛在擴散模型（LDM）

```
傳統擴散：像素空間 [1024, 1024, 3] = 3.1M 維度
潛在擴散：潛在空間 [64, 64, 4] = 16K 維度
運算量降低：約 200 倍
```

### VAE 壓縮

使用預訓練的 VAE（變分自編碼器）將影像壓縮到低維潛在空間，然後在潛在空間中執行擴散過程。

## 使用 Diffusers 進行生成

```python
from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt, num_inference_steps=50).images[0]
image.save("astronaut.png")
```

## 技術對比總結

| 面向 | DALL-E 2 | Stable Diffusion |
|------|----------|-----------------|
| 開源 | 否 | 是 |
| 參數 | 35 億 | 8.6 億 |
| 架構 | 兩階段擴散 | 潛在擴散 |
| 解析度 | 1024x1024 | 512x512 |
| 生成速度 | 慢 | 快 |
| 硬體需求 | 雲端 | 消費級 GPU |
| 可控性 | 低 | 高（Prompt 工程） |

## 延伸閱讀

- [DALL-E 2 論文](https://www.google.com/search?q=DALL-E+2+hierarchical+text+conditional+image+generation+paper)
- [Stable Diffusion 論文](https://www.google.com/search?q=High+Resolution+Image+Synthesis+with+Latent+Diffusion+Models)
- [Diffusers 文檔](https://www.google.com/search?q=Hugging+Face+Diffusers+documentation)
- [Promp Engineering 指南](https://www.google.com/search?q=Stable+Diffusion+prompt+engineering+guide)
