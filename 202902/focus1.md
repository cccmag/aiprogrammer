# 合成資料的崛起（2014-2029）

## 從 GAN 到 LLM：合成資料的演進史

合成資料從學術概念變為產業標配，經歷了三個關鍵階段。

### 2014-2019：GAN 時代

Goodfellow 在 2014 年提出生成對抗網路（GAN），為合成資料開啟新紀元。DCGAN 引入卷積架構穩定訓練，WGAN 用 Wasserstein 距離解決模式崩潰，StyleGAN 實現風格分離控制。2017 年 NVIDIA 的 Progressive GAN 首次生成 1024x1024 人臉影像。CycleGAN 讓無配對的跨域影像轉換成為可能，大幅擴展合成資料的應用場景。

```python
# 從 _code/synthetic_data.py 引入文字生成
from _code.synthetic_data import SyntheticDataGenerator

gen = SyntheticDataGenerator()
records = gen.generate_text(5)
for r in records:
    print(f"[{r.label}] {r.text}")
```

### 2020-2023：擴散模型崛起

2020 年 DDPM（Denoising Diffusion Probabilistic Models）提出前向加噪與逆向去噪的框架。2021 年 OpenAI 的 GLIDE 將文字條件引入擴散模型。2022 年 Stable Diffusion 開源後引爆影像合成應用——任何人都能在消費級 GPU 上生成高品質影像。同期 GPT-3/ChatGPT 帶動 LLM 合成文字資料，Prompt Engineering 成為合成資料的核心技術。2023 年 DALL-E 3 和 Midjourney V6 將文字到影像合成推向新高度。

### 2024-2029：合成資料規模化

2024 年合成資料市場突破 10 億美元。LLM 能生成高品質的對話、程式碼、學術論文。Google 的 SynthID 為合成資料添加不可見浮水印以便溯源。2025 年 OpenAI 的 Sora 將影片合成帶入主流。2026 年合成資料管線（Synthetic Data Pipeline）成為 MLOps 的標準元件。2027 年後合成資料已佔 AI 訓練資料的 60% 以上，主流策略從「擴增真實資料」轉向「完全合成訓練」。

### 驅動因素

合成資料崛起的背後有三個驅動力：真實資料取得成本持續上升、隱私法規趨嚴（GDPR、CCPA、EU AI Act）、以及生成模型的品質已跨越實用門檻。

### 關鍵里程碑

- 2014：GAN 提出
- 2017：CycleGAN 無配對跨域轉換
- 2020：DDPM 擴散模型
- 2022：ChatGPT / Stable Diffusion
- 2024：合成資料市場 10 億美元
- 2027：合成資料佔訓練資料 60%
- 2029：多數垂直領域使用全合成訓練

## 延伸閱讀

- [GAN synthetic data generation](https://www.google.com/search?q=GAN+Goodfellow+2014+synthetic+data)
- [Diffusion models synthetic data 2020](https://www.google.com/search?q=DDPM+diffusion+model+synthetic+data+generation)
- [Synthetic data market 2024](https://www.google.com/search?q=synthetic+data+market+size+2024+billion)
