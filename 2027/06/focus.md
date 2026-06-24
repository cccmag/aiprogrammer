# 本期焦點

## 大型語言模型實戰 — 從 Transformer 到 RAG 應用

### 引言

大型語言模型（LLM）已經從研究實驗室走進生產環境。從 ChatGPT 到 Claude，從 Llama 到 Mistral——這些模型正在重新定義我們與程式碼、文字和知識互動的方式。

但理解 LLM 的內部運作並非只是學術興趣。當你需要：
- 微調一個模型來理解你的程式碼庫
- 建立 RAG 系統來回答產品文件問題
- 最佳化提示詞以獲得可靠輸出

——你需要真正理解 transformer 架構、注意力機制、以及 LLM 的部署策略。

本期將從基礎開始，逐步建構對 LLM 的完整理解。我們會用 Python 從零實作一個迷你 transformer，探討注意力機制的數學，然後深入 RAG、微調和部署等實戰主題。

---

## 大綱

* [程式：實作迷你 Transformer](focus_code.md)
   - 多頭注意力（Multi-Head Attention）
   - 位置編碼（Positional Encoding）
   - Transformer 區塊
   - 文字生成示範

1. [Transformer 架構基礎（2017-2026）](focus1.md)
   - Attention Is All You Need 的革命
   - Encoder-Decoder vs Decoder-Only
   - 模型規模與 Scailing Laws

2. [注意力機制的奧秘（2015-2026）](focus2.md)
   - 從 Seq2Seq + Attention 到 Self-Attention
   - 多頭注意力的直觀理解
   - 注意力可視化與除錯

3. [預訓練與資料（2018-2026）](focus3.md)
   - 預訓練目標（MLM、CLM、Seq2Seq）
   - 資料集規模與品質
   - Tokenization（BPE、SentencePiece）

4. [微調策略：SFT 與 RLHF（2020-2026）](focus4.md)
   - 監督式微調（SFT）
   - 指令微調（Instruction Tuning）
   - RLHF 與 DPO 的比較

5. [RAG：檢索增強生成（2020-2026）](focus5.md)
   - RAG 架構設計
   - 向量資料庫（Chroma、Pinecone）
   - 分塊策略與嵌入模型

6. [LLM 部署與量化（2022-2026）](focus6.md)
   - 模型量化（GPTQ、GGUF、AWQ）
   - 推論引擎（llama.cpp、vLLM、TGI）
   - GPU vs CPU 部署策略

7. [AI 輔助 LLM 開發（2024-2026）](focus7.md)
   - LLM 評估與監控
   - Prompt 工程最佳實踐
   - AI Agent：工具使用與多步驟推理
   - 未來展望：多模態、超長上下文

---

## LLM 技術堆疊

```
應用層 (Chat UI、RAG 系統、Agent、程式碼助手)
      │
提示工程 (System Prompt、Few-Shot、Chain-of-Thought)
      │
RAG/記憶 (向量資料庫、對話歷史、工具結果)
      │
模型層 (Transformer、Attention、Tokenization)
      │
部署層 (量化、推論引擎、GPU/CPU 排程)
```

## 濃縮回顧

### LLM 發展里程碑

| 年份 | 模型 | 要點 |
|------|------|------|
| 2017 | Transformer | Attention Is All You Need |
| 2018 | BERT、GPT | 預訓練 + 微調範式 |
| 2020 | GPT-3 | Scailing Laws、Few-Shot Learning |
| 2022 | ChatGPT、Llama | 指令微調、開源模型 |
| 2023 | GPT-4、Claude、Mistral | 多模態、長上下文 |
| 2024 | Llama 3、Qwen 2 | 開源逼近閉源 |
| 2025-26 | 小型高效模型 | 邊緣部署、領域特化 |

### 注意力機制核心公式

Scaled Dot-Product Attention：

```
Attention(Q, K, V) = softmax(Q × K^T / √d_k) × V
```

多頭注意力將輸入投影到多組 Q、K、V，並行計算後拼接：

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W^O
```

### 完整 Transformer 區塊

```python
class TransformerBlock:
    def __init__(self, d_model, n_heads):
        self.attention = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)

    def forward(self, x):
        x = x + self.attention(self.norm1(x))
        x = x + self.ffn(self.norm2(x))
        return x
```

### RAG 核心流程

```
使用者查詢 → 嵌入查詢 → 向量資料庫檢索 → 擷取文檔 → 
                 ↓
       LLM 回覆 ← 提示詞 + 文檔
```

---

**下一步**：[程式實作](focus_code.md) → [Transformer 架構基礎](focus1.md)

## 延伸閱讀

- [Attention Is All You Need](https://www.google.com/search?q=Attention+Is+All+You+Need+paper)
- [The Illustrated Transformer](https://www.google.com/search?q=illustrated+transformer+explanation)
- [Hugging Face NLP Course](https://www.google.com/search?q=Hugging+Face+NLP+course)
- [LLM 部署指南](https://www.google.com/search?q=LLM+deployment+guide+2026)
