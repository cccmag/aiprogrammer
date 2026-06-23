# 程式實作：從零實作多模態搜尋引擎

## 簡介

本實作從零建構一個跨模態搜尋引擎，展示文字、圖片、音訊三種模態的統一向量表示與相似度搜尋。完整程式碼在 `_code/multimodal_search.py`。

## 核心元件

### 1. 多模態嵌入器

將不同模態的資料映射到同一向量空間：

```python
embedder = MultiModalEmbedder(dim=64)
text_vec = embedder.embed_text("cat on windowsill")
image_vec = embedder.embed_image("cat on windowsill")
audio_vec = embedder.embed_audio("cat meowing")
```

### 2. 跨模態搜尋

文字搜圖片、圖片搜文字、任意模態互搜：

```python
index.search(text_query_vec, k=3, modality="image")  # text→image
index.search(image_query_vec, k=3, modality="text")   # image→text
index.search(query_vec, k=5)                          # all modalities
```

### 3. 對比學習（CLIP 風格）

用 InfoNCE loss 評估跨模態對齊：

```python
loss = contrastive_loss(text_embs, image_embs)
```

## 執行方式

```bash
cd _code
python3 multimodal_search.py
```

## 延伸練習

1. **串接真實模型**：用 `sentence-transformers/clip-ViT-B-32` 替換模擬嵌入
2. **加入影片模態**：用關鍵幀嵌入實現影片搜尋
3. **建立索引快取**：將嵌入結果儲存到向量資料庫
4. **重新排名**：在第一階段檢索後用跨模態注意力重新排序
