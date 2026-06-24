# 本月新知

## 2022 年 9 月程式與 AI 技術動態

### 深度學習與注意力機制

**Transformer 架構持續進化**

2022 年 9 月，Google 研究團隊發表了 CoCa（Contrastive Captioners），這是一個結合對比學習與字幕生成的視覺語言模型。CoCa 在 ImageNet 分類任務上達到了 91.0% 的 Top-1 準確率，並在多個視覺語言基準測試中創下新紀錄。其核心架構基於注意力機制，採用串聯式的編碼器-解碼器設計。

**稀疏注意力取得突破**

本月，多家研究機構發表了稀疏注意力機制的改進版本。ETA（Efficient Transformer Attention）通過 Learnable Downsampling 方法，將長序列注意力的計算複雜度從 O(n²) 降低到 O(n log n)，同時保持模型品質。這項進展對處理長文件、基因序列和程式碼理解等任務至關重要。

**FlashAttention 成為標準**

FlashAttention 技術在本月被 PyTorch 2.0 的實驗性版本整合，提供 CUDA 核心級別的注意力計算優化。通過減少 HBM 讀寫次數，FlashAttention 將注意力計算速度提升了 2-4 倍，記憶體使用量減少了 5-10 倍。這使得在單張 GPU 上訓練更長序列的 Transformer 模型成為可能。

### 語言模型與 NLP

**PaLM 的後續研究**

Google 持續發布關於 PaLM（Pathways Language Model）的技術報告。本月發表的論文詳細分析了 PaLM 的注意力模式，發現模型的深層頭部（deep heads）傾向於關注語法結構，而淺層頭部則關注詞彙語義。這項分析對理解大型語言模型的內部運作機制提供了重要線索。

**Meta 開源 OPT-IML**

Meta 於本月開源了 OPT-IML，這是一個經過指令微調的 175B 參數語言模型。OPT-IML 在 1500+ 個 NLP 任務上進行了微調，展現出強大的泛化能力。研究人員特別關注了注意力權重的可解釋性分析，發現指令微調使注意力頭更專注於任務相關的資訊。

### 電腦視覺

**ViT 與注意力在視覺的應用**

Vision Transformer（ViT）的變體在本月大量湧現。Swin Transformer V2 發布了支援 1536x1536 解析度的版本，在物體偵測和分割任務上超越了 CNN 架構。研究人員也發現，ViT 的注意力圖與生物的視覺皮層有驚人的相似性，為注意力機制的生物學基礎提供了新的證據。

### 開發工具與框架

**Hugging Face Transformers 更新**

Hugging Face 於本月發布 Transformers 庫 v4.22，新增對 Longformer、BigBird 等高效注意力模型的支援。新版本還改進了注意力權重的可視化工具，讓研究人員能夠更直觀地分析模型的注意力模式。

**PyTorch 發布 1.13**

PyTorch 1.13 本月發布，重點優化了 Transformer 相關操作的效能。新增了 `torch.nn.functional.scaled_dot_product_attention` 函數，提供一個統一的注意力計算介面，支援 FlashAttention 和 Memory-Efficient Attention 兩種後端實現。

### 業界動態

- **Stability AI 發布 Stable Diffusion**：開源的文字生成圖像模型，基於潛在擴散模型和 CLIP 注意力引導
- **DeepMind 的 AlphaTensor**：使用強化學習發現矩陣乘法演算法，展示了注意力機制在科學發現中的潛力
- **OpenAI 的 Whisper**：開源語音辨識系統，使用編碼器-解碼器 Transformer 架構
- **Anthropic 發布 Claude**：注重安全的對話 AI，基於 Transformer 的解碼器架構

### 標準與規範

- **ONNX 發布 1.13 版本**：優化了 Transformer 模型的匯出與推論
- **MLPerf Inference v2.1**：新增 BERT 和 DLRM 等注意力模型的基準測試
- **TensorFlow 發布 2.10**：整合了 TF-TRT 對 Transformer 模型的最佳化支援

### 延伸閱讀

- [CoCa: Contrastive Captioners for Image-Text Retrieval](https://www.google.com/search?q=CoCa+contrastive+captioners+2022)
- [FlashAttention: Fast and Memory-Efficient Exact Attention](https://www.google.com/search?q=FlashAttention+2022)
- [OPT-IML: Scaling Language Model Instruction MetaLearning](https://www.google.com/search?q=OPT-IML+2022)
