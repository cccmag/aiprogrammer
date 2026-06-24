# 本月新知

## 2022 年 5 月語言模型技術動態

### GPT-3 應用生態蓬勃發展

OpenAI 的 GPT-3 模型在 2022 上半年持續擴張應用場景。GitHub Copilot 已整合至主流 IDE，協助開發者自動補齊程式碼。多家新創公司基於 GPT-3 API 開發了文案生成、客服對話、程式除錯等工具。GPT-3 的 few-shot 學習能力使其在少量樣本下就能完成多種 NLP 任務。

### Google PaLM 發布

Google 在 2022 年 4 月發布了 PaLM（Pathways Language Model），擁有 5400 億參數。PaLM 在多個推理基準測試上超越了 GPT-3，特別是在數學推理和常識理解方面。PaLM 採用了 Pathways 系統，在多達 6144 個 TPU 晶片上進行訓練。

### DeepMind Chinchilla 研究

DeepMind 發表了 Chinchilla 模型，提出了「計算最優訓練」的觀點——對於固定的計算預算，模型大小和訓練資料量應該按比例擴展。Chinchilla 僅有 70B 參數，但在多個任務上超越了 GPT-3（175B），證明了資料量與模型大小的平衡至關重要。

### Hugging Face Transformers 生態

Hugging Face 的 Transformers 函式庫已支援超過 100 種模型架構。2022 年 5 月，Hugging Face 發布了 Accelerate 函式庫，簡化了大型模型的多 GPU 分散式訓練。社群持續貢獻各語言的預訓練模型，包括繁體中文的模型。

### Meta OPT 開源語言模型

Meta 發布了 OPT（Open Pre-trained Transformer）系列模型，從 125M 到 175B 參數的模型完全開源。OPT-175B 是首個公開權重的 GPT-3 級別模型，研究人員可以自由存取模型權重和訓練日誌。

### 中文語言模型進展

2022 年上半年，多個中文預訓練語言模型發布，包括 ERNIE 3.0、CPM-2 和悟道 2.0。這些模型在中文理解、生成和對話任務上表現優異。中國學術界和工業界在超大規模語言模型領域的投入持續增加。

### 業界動態

- **DeepMind 的 Sparrow**：基於語言模型的對話代理，整合了 RLHF（人類回饋強化學習）
- **OpenAI API 更新**：新增了自訂模型微調功能和內容過濾機制
- **AI21 Labs Jurassic-1**：以色列 AI21 Labs 的 178B 參數模型開放了 API 存取
- **NVIDIA NeMo Megatron**：NVIDIA 發布了 NeMo Megatron 框架，支援數千 GPU 的語言模型訓練
