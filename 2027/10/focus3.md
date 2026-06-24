# 視覺語言模型（VLM）架構（2021-2026）

## 從 CLIP 到 VLM：不只是對齊

CLIP 把圖片和文字映射到同一空間，但**不能生成文字**。視覺語言模型（VLM）更進一步：理解圖片並生成描述、回答問題、進行對話。

## VLM 的主流架構

### 1. 編碼器-解碼器

ViT 編碼圖片 + Transformer 解碼文字：

```python
def vlm_generate(image, prompt):
    feat = vit_encoder(image)          # 視覺特徵
    proj = projection_layer(feat)      # 映射到語言空間
    return llm.generate(prefix=proj, prompt=prompt)
```

### 2. Q-Former：BLIP-2 的關鍵創新

BLIP-2 提出的 Q-Former（Querying Transformer）用可學習的 query tokens 從視覺特徵中提取任務相關資訊，作為視覺編碼器和 LLM 之間的橋樑，避免了大規模訓練整個模型的需求。

### 3. LLaVA 風格：簡單線性投影

LLaVA 用最簡單的 ViT + 線性投影（單層 Linear） + LLM 就達到極佳效果，證明視覺語言的對齊不必複雜：

```python
def llava_forward(image, text_tokens):
    vis = clip_vit(image)                     # 凍結 ViT
    vis = nn.Linear(768, 4096)(vis)           # 唯一訓練層
    return llama(torch.cat([vis, text_tokens])) # 凍結 LLM
```

## VLM 的關鍵能力

| 能力 | 說明 | 代表模型 |
|------|------|---------|
| 圖像描述 | 描述圖片內容 | BLIP-2, LLaVA |
| 視覺問答 | 根據圖片回答問題 | Flamingo | 
| 引用分割 | 用文字指定位圖中的物體 | SAM + VLM |
| 文件分析 | 讀取圖表中的文字與數字 | GPT-4V, Claude |
| 多輪對話 | 以圖片為背景的連續對話 | LLaVA-NeXT |

## VLM 里程碑

| 年份 | 模型 | 創新 |
|------|------|------|
| 2021 | Flamingo | 第一個通用 VLM |
| 2022 | BLIP-2 | Q-Former 高效連結 |
| 2023 | LLaVA | 簡單線性投影 + 指令微調 |
| 2023 | GPT-4V | 商業級多模態能力 |
| 2024 | LLaVA-NeXT | 動態解析度支援 |
| 2025 | 原生多模態 | 統一架構無需投影層 |
| 2026 | 即時影片理解 | VLM 擴展到影片串流 |

## 小結

VLM 從複雜的跨模態注意力到極簡的線性投影，再到統一架構。教訓是：**視覺與語言的對齊不必複雜**——簡單投影 + 強大 LLM 即可達到驚人效果。

---

**下一步**：[語音與音訊 AI 技術](focus4.md)

## 延伸閱讀

- [BLIP-2 論文](https://www.google.com/search?q=BLIP+2+BLIP+2+Bootstrapping+Language+Image+Pre+training+with+Frozen+Image+Encoders+and+Large+Language+Models)
- [LLaVA 論文](https://www.google.com/search?q=LLaVA+Large+Language+and+Vision+Assistant)
- [Flamingo 論文](https://www.google.com/search?q=Flamingo+a+Visual+Language+Model+for+Few+Shot+Learning)
