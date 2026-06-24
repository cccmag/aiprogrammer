# 2022 年 AI 全景：技術突破一覽

## 從「能看」到「能創造」的跨越

2022 年之前，AI 的主要角色是「分析」——分類影像、預測趨勢、推薦內容。2022 年，AI 的角色轉變為「創造」。這一年，生成式 AI 的三個支柱——文字、影像、程式——同時迎來了質的突破。

## 三大技術支柱

### 1. 大型語言模型

2022 年是語言模型的軍備競賽年。Google 的 PaLM 以 5400 億參數登上規模巔峰，OpenAI 的 GPT-3.5 則在實用性上取得突破。關鍵在於訓練方法的創新：

- **Scaling Law**：隨著參數量和訓練數據的增加，模型能力呈現可預測的提升
- **RLHF（人類回饋強化學習）**：InstructGPT / ChatGPT 的核心，讓模型輸出更符合人類偏好
- **指令微調（Instruction Tuning）**：在大量任務上微調，顯著提升泛化能力

### 2. 文字生成影像

2022 年最令人驚豔的技術突破。DALL-E 2、Stable Diffusion、Midjourney 三強鼎立，各自代表了不同的技術路線：

- **DALL-E 2**：OpenAI 的 CLIP + 擴散模型架構，影像品質最高
- **Stable Diffusion**：開源方案，在潛在空間（latent space）中執行擴散，大幅降低計算需求
- **Midjourney**：專注於美學風格的產品化方案

擴散模型取代了 GAN 成為影像生成的主流技術。其核心思想是：從雜訊開始，逐步去雜訊直到產生清晰的影像。

### 3. 程式碼生成

AlphaCode 和 GitHub Copilot 展示了 AI 在程式碼生成上的能力：

- **AlphaCode**：解決競賽級程式問題，需要理解問題描述並設計演算法
- **Copilot**：日常開發輔助，補全函式、生成測試、撰寫文檔

兩者都基於 Transformer 架構，在大量公開程式碼上訓練。程式碼生成的獨特優勢在於——生成的品質可以透過編譯和測試自動驗證。

## 多模態融合

2022 年的另一趨勢是多模態——讓一個模型同時理解和生成多種形式的資料：

- **Gato**（DeepMind）：同一個模型玩 Atari 遊戲、描述影像、控制機械手臂
- **Flamingo**（DeepMind）：視覺語言模型，可以根據影像回答問題
- **PaLI**（Google）：將語言和視覺編碼器統一到同一個架構

多模態被視為通向通用人工智慧（AGI）的關鍵路徑。

## 硬體基礎設施

2022 年的 AI 突破離不開硬體的支援：

- **NVIDIA A100**：成為 LLM 訓練的標配 GPU，供不應求
- **Google TPU v4**：PaLM 540B 在 6144 顆 TPU v4 上訓練
- **訓練成本**：PaLM 540B 的單次訓練成本估計在 1000 萬美元以上

## 數據視角

根據腳本 year_review_2022.py 的計算，2022 年全球 AI 市場規模達 425 億美元，年成長率 70.7%，CAGR（2020-2022）為 64.5%：

```
    2020       15.7 B$
    2021       24.9 B$   +58.6%
    2022       42.5 B$   +70.7%
```

這個成長率反映了生成式 AI 帶來的市場動能。

## 延伸閱讀

- [Scaling Laws for Neural Language Models](https://www.google.com/search?q=Scaling+Laws+Neural+Language+Models+Kaplan+2022)
- [Diffusion Models Beat GANs](https://www.google.com/search?q=Diffusion+Models+Beat+GANs+2022)
- [Pathways: Google 的多任務架構](https://www.google.com/search?q=Google+Pathways+architecture+2022)
- [Emergent Abilities of Large Language Models](https://www.google.com/search?q=Emergent+Abilities+Large+Language+Models+2022)
