# Transformer 在其他領域的應用

## 前言

Transformer 最初為 NLP 設計，但現在已擴展到電腦視覺、音訊、強化學習等多個領域。

---

## 一、電腦視覺

### Vision Transformer (ViT)

2020 年提出的 ViT 將 Transformer 應用於圖像分類：

```
圖像 -> 補丁分割 -> 線性嵌入 -> Transformer Encoder -> 分類
```

```python
# ViT 的核心思想
image = load_image()
patches = split_into_patches(image, patch_size=16)  # (N, 16, 16, 3)
patches = linear_embed(patches)  # (N, d_model)
cls_token = learnable_embedding()
tokens = concat([cls_token, patches])
output = transformer_encoder(tokens)
prediction = classifier(output[0])
```

### 與 CNN 的比較

| 方面 | CNN | ViT |
|------|-----|-----|
| 資料需求 | 較少 | 較多 |
| 計算成本 | 較低 | 較高 |
| 長距離依賴 | 有限 | 強 |
| 可解釋性 | 中等 | 較強 |

### DETR (Detection Transformer)

端到端物體檢測：
```python
# 移除 NMS 等手工設計模組
output = detr(image)
# 直接輸出邊界框和類別
```

---

## 二、音訊處理

### Audio Spectrogram Transformer

將音訊轉為頻譜圖，再應用 Transformer：

```python
# 語音辨識流程
audio = load_audio()
spectrogram = convert_to_spectrogram(audio)  # (T, F)
transformer_output = ast_encoder(spectrogram)
transcription = decoder(transformer_output)
```

### Speech Transformer

用於機器翻譯：
- 音訊 -> Transformer Encoder
- 文字 -> Transformer Decoder

### 音樂生成

| 模型 | 應用 |
|------|------|
| Jukebox (OpenAI) | 音樂生成 |
| Music Transformer | 旋律生成 |
| MuseNet | 多樂器作曲 |

---

## 三、強化學習

### Decision Transformer

將強化學習問題框架為序列模型：

```python
# 輸入：過去的回饋、狀態、行動序列
trajectory = concat([
    returns_to_go,      # 回饋
    states,             # 狀態
    actions             # 行動
])

# 輸出：預測的最佳行動
next_action = decision_transformer(trajectory)
```

### 優勢

- 可以利用大型語言模型的預訓練
- 處理長序列決策問題
- 統一的序列建模范式

---

## 四、表格資料

### TabTransformer

對表格資料應用 Transformer：

```python
# 表格輸入 -> 類別和數值特徵
# 分別編碼後通過 Transformer
embeddings = tab_transformer( tabular_data )
prediction = classifier(embeddings)
```

---

## 五、分子與藥物發現

### 分子指紋當作序列

```python
# 分子結構 -> SMILES 字串 -> Transformer
smiles = "CCO"  # 乙醇
molecule_embedding = transformer(smiles)
property_prediction = predictor(molecule_embedding)
```

### 蛋白質結構

AlphaFold 2 使用 Transformer 進行蛋白質結構預測。

---

## 六、推薦系統

### Transformers4Rec

將使用者行為序列視為序列：

```python
# 使用者點擊序列
user_sequence = [item1, item2, item3, ...]
embeddings = transformer(user_sequence)
next_item_prediction = predictor(embeddings)
```

---

## 七、多模態學習

### CLIP (Contrastive Language-Image Pre-training)

連接文字和圖像：

```python
# 圖像編碼器 + 文字編碼器
image_features = clip_image_encoder(image)
text_features = clip_text_encoder(text)

# 對比學習
similarity = cos_sim(image_features, text_features)
```

### 應用

- 零樣本圖像分類
- 文字到圖像生成
- 圖像搜尋

---

## 總結

Transformer 的成功源於其通用性：

| 領域 | 應用 |
|------|------|
| NLP | 翻譯、生成、分類 |
| Vision | 分類、檢測、分割 |
| Audio | 語音辨識、生成 |
| 強化學習 | 決策、控制 |
| 多模態 | CLIP、DALL-E |

Transformer 正在成為深度學習的「Transformer」——一個通用基礎架構。

---

## 延伸閱讀

- [Vision+Transformer+ViT+2020](https://www.google.com/search?q=Vision+Transformer+ViT+2020)
- [transformer+reinforcement+learning+2020](https://www.google.com/search?q=transformer+reinforcement+learning+2020)
- [multimodal+transformer+CLIP+2020](https://www.google.com/search?q=CLIP+multimodal+transformer+2020)