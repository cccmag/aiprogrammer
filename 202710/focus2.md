# 多模態嵌入與對比學習（2020-2026）

## 嵌入：把世界放進向量空間

嵌入是將語義壓縮到稠密向量的技術。多模態的關鍵挑戰是讓不同模態的嵌入位於**同一向量空間**：

```
文字嵌入空間                 影像嵌入空間
   ┌──────┐                   ┌──────┐
   │"貓"  │                   │  🐱  │
   │[0.2] │                   │[0.3] │
   │[0.8] │    ──── 對齊 ──→  │[0.7] │
   │[0.1] │                   │[0.2] │
   └──────┘                   └──────┘
         ╲                   ╱
          ╲  同一向量空間    ╱
           ╲               ╱
        ┌────────────────────┐
        │  Unified Space     │
        │ [0.2, 0.8, 0.1]   │  ← "貓" 文字嵌入
        │ [0.3, 0.7, 0.2]   │  ← 🐱 圖片嵌入
        │ [0.25, 0.75, 0.15]│  ← 喵叫聲音嵌入
        └────────────────────┘
```

## CLIP：對比學習的里程碑

2021 年 OpenAI 的 CLIP（Contrastive Language-Image Pre-training）是跨模態學習的經典之作。核心是對比學習（InfoNCE loss），目標是讓配對的 (image, text) 在向量空間中接近，非配對的遠離：

```python
def clip_contrastive_loss(image_embs, text_embs, temperature=0.07):
    """對比損失：讓正確配對的相似度 > 錯誤配對"""
    n = len(image_embs)
    sim_matrix = [[cosine_similarity(image_embs[i], text_embs[j])
                   for j in range(n)] for i in range(n)]
    loss = 0
    for i in range(n):
        exp_pos = math.exp(sim_matrix[i][i] / temperature)
        exp_all = sum(math.exp(s / temperature) for s in sim_matrix[i])
        loss += -math.log(exp_pos / exp_all)
    return loss / n
```

CLIP 在 4 億個配對上訓練，實現零樣本分類與跨模態檢索。

## ImageBind：六模態統一嵌入

2023 年 Meta 的 ImageBind 將統一嵌入推廣到六個模態：影像、文字、音訊、深度、熱感應、IMU。關鍵洞見：**所有模態透過影像橋樑自動對齊**。

```python
class ImageBindStyleEmbedder:
    """
    概念：所有模態透過影像這個「橋樑」對齊
    
    影像 ↔ 文字  （已對齊）
    影像 ↔ 音訊  （已對齊）
    → 文字 ↔ 音訊  （自動對齊，不需要直接的 text-audio 配對）
    """
    def embed(self, data, modality):
        # 每個模態有專屬的 encorder，但輸出到同一空間
        if modality == "image":
            return self.image_encoder(data)   # ViT
        elif modality == "text":
            return self.text_encoder(data)    # Transformer
        elif modality == "audio":
            return self.audio_encoder(data)   # AST
        # ... depth, thermal, IMU ...
```

## 小結

多模態嵌入是連接不同感知世界的橋樑。CLIP 證明了對比學習在跨模態對齊上的有效性，ImageBind 則展示了框架可擴展到任意模態。嵌入空間正成為 AI 理解世界的統一語言。

---

**下一步**：[視覺語言模型（VLM）架構](focus3.md)

## 延伸閱讀

- [CLIP 論文](https://www.google.com/search?q=CLIP+Learning+Transferable+Visual+Models+from+Natural+Language+Supervision)
- [ImageBind 論文](https://www.google.com/search?q=ImageBind+One+Embedding+Space+To+Bind+Them+All)
- [SigLIP 論文](https://www.google.com/search?q=SigLIP+Sigmoid+Loss+for+Language+Image+Pre+Training)
