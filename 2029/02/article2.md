# 擴散模型影像合成

## 1. 引言

擴散模型（Diffusion Models）在 2020 年代快速崛起，成為影像生成領域的主流技術。不同於 GAN 的對抗訓練，擴散模型透過漸進式去噪的過程生成高品質影像。本文探討如何使用擴散模型進行影像合成資料擴增，並以 Python 實作示範。

## 2. 擴散模型核心概念

擴散模型的運作分為兩個階段：

- **前向擴散**：逐步對原始影像添加高斯雜訊，直到完全變成隨機噪聲
- **反向去噪**：學習從雜訊中逐步還原原始影像

其數學基礎是隨機微分方程（SDE），但實際使用時只需呼叫預訓練模型即可。

## 3. 使用 Stable Diffusion 生成合成影像

```python
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os

# 載入預訓練模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

def generate_synthetic_images(
    prompts: list[str],
    save_dir: str = "synthetic_images",
    n_per_prompt: int = 3
):
    os.makedirs(save_dir, exist_ok=True)
    for idx, prompt in enumerate(prompts):
        for i in range(n_per_prompt):
            image = pipe(
                prompt,
                num_inference_steps=50,
                guidance_scale=7.5
            ).images[0]
            path = os.path.join(save_dir, f"gen_{idx}_{i}.png")
            image.save(path)
            print(f"已儲存：{path}")

# 生成不同類別的合成影像
prompts = [
    "a red apple on white background, product photo",
    "a wooden chair in empty room, interior design",
    "a handwritten digit 7, MNIST style"
]
generate_synthetic_images(prompts)
```

## 4. 條件控制生成

有時需要精確控制生成內容。結合 ControlNet 可以實現條件式生成：

```python
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from diffusers.utils import load_image

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16
)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# 根據邊緣圖生成
edge_image = load_image("edge_map.png")
image = pipe(
    "a photograph of a cat",
    image=edge_image,
    num_inference_steps=30,
).images[0]
```

## 5. 資料擴增應用

擴散模型在資料擴增中的典型場景：

| 應用場景 | 方法 | 優勢 |
|---------|------|------|
| 分類任務 | 生成各類別新樣本 | 平衡類別分佈 |
| 異常檢測 | 生成邊緣案例 | 補足長尾資料 |
| 醫學影像 | 跨模態轉換（CT→MRI） | 克服資料稀缺 |

## 6. 結語

擴散模型提供了目前品質最高的合成影像生成能力。比起傳統的幾何變換資料擴增，擴散模型能產生語意層面的多樣性。但需注意計算成本較高，且生成結果仍需人工過濾。

## 延伸閱讀

- [Hugging Face Diffusers Guide](https://www.google.com/search?q=huggingface+diffusers+guide)
- [Denoising Diffusion Probabilistic Models](https://www.google.com/search?q=DDPM+denoising+diffusion+probabilistic+models)
