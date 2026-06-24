# AI 繪圖的爆發：DALL-E 2、Stable Diffusion

## 從 GAN 到擴散模型

2022 年之前，AI 影像生成的主流技術是生成對抗網路（GAN）。GAN 透過生成器與鑑別器的對抗訓練產生影像，但訓練不穩定、模式崩潰等問題始終困擾研究者。

擴散模型（Diffusion Model）在 2022 年徹底改變了這個局面。其核心思想優雅而簡單：從一個隨機雜訊開始，透過反覆的去噪過程逐步還原出清晰的影像。這就像是從一團雪花開始，看著它逐漸凝結成一個蘋果的過程。

## 三大玩家

### DALL-E 2（2022.03）

OpenAI 的 DALL-E 2 是 2022 年最早引爆 AI 繪圖熱潮的產品。相較於 2021 年的 DALL-E 1，DALL-E 2 的解析度提升了 4 倍，從 256x256 到 1024x1024。

DALL-E 2 的技術架構分為三個部分：
- **CLIP 編碼器**：將文字提示轉換為語義向量
- **先驗模型**：將文字向量映射到影像向量空間
- **擴散去噪器**：從影像向量生成最終像素

這種「先理解，後生成」的兩階段架構讓 DALL-E 2 能夠產生與文字描述高度一致的影像。

### Stable Diffusion（2022.08）

Stability AI 發布的 Stable Diffusion 是 2022 年最具影響力的開源 AI 專案之一。它的核心創新是將擴散過程從像素空間轉移到潛在空間（Latent Space），這使得：

- **計算需求大幅降低**：可以在消費級 GPU 上運行
- **生成速度更快**：潛在空間的維度遠低於像素空間
- **擴展性更強**：可以在壓縮的潛在表示上進行編輯

Stable Diffusion 的開源策略引發了 AI 繪圖的民主化浪潮。開發者可以在自己的電腦上運行、微調、修改模型，社群迅速建立了豐富的工具生態：

- **Automatic1111 WebUI**：最受歡迎的圖形介面
- **DreamStudio**：Stability AI 官方產品
- **Diffusers**：Hugging Face 的擴散模型套件
- **LoRA**：輕量級模型微調技術

### Midjourney（2022.07）

Midjourney 以 Discord 機器人的形式提供服務，專注於美術風格和創意品質。它的優勢在於：

- **美學品質**：在藝術風格、構圖和色彩上優於競爭對手
- **社群驅動**：Discord 上的社群創造了獨特的創作文化
- **迭代創作**：透過圖片的變體和升級功能引導創作過程

## 技術對比

| 特性 | DALL-E 2 | Stable Diffusion | Midjourney |
|------|----------|-----------------|------------|
| 開源 | 否 | 是 | 否 |
| 參數量 | 35 億 | 8.6 億 | 未公開 |
| 架構 | 擴散 + CLIP | 潛在擴散 | 擴散（改進版） |
| 消費級 GPU | 否 | 可 | 否 |
| 特長 | 語義理解 | 可控性、擴展性 | 美學品質 |

## 版權與社會爭議

AI 繪圖的爆發也帶來了嚴峻的版權問題：

- **訓練數據的版權**：模型是在大量受版權保護的影像上訓練的
- **風格的模仿**：使用者可以生成「在 XXX 風格下的 YYY」
- **藝術家的抵制**：ArtStation 等平台上出現了藝術家的抗議活動
- **Getty Images 訴訟**：Getty Images 起訴 Stability AI 侵犯版權

這些爭議在 2023 年持續發酵，並推動了 AI 監管法規的加速制定。

## 延伸閱讀

- [DALL-E 2 技術報告](https://www.google.com/search?q=DALL-E+2+hierarchical+text+conditional+image+generation)
- [Stable Diffusion 論文](https://www.google.com/search?q=High+Resolution+Image+Synthesis+with+Latent+Diffusion+Models)
- [Diffusers 套件](https://www.google.com/search?q=Hugging+Face+Diffusers+library)
- [AI 繪圖版權爭議](https://www.google.com/search?q=AI+art+copyright+controversy+2022)
