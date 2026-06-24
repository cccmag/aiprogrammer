# Transformer 架構基礎（2017-2026）

## Attention Is All You Need 的革命

2017 年，Google 團隊發表了《Attention Is All You Need》，提出 Transformer 架構。這篇論文從根本上改變了 NLP 的方向——它拋棄了傳統的 RNN/CNN，完全依賴注意力機制。

```python
# Transformer 的核心公式
Attention(Q, K, V) = softmax(Q @ K.T / sqrt(d_k)) @ V
```

這個看似簡單的公式包含了三個關鍵洞察：
1. **Q × K^T** 計算序列中所有位置對之間的相似度
2. **除以 √d_k** 防止內積過大使 softmax 梯度消失
3. **softmax** 產生機率分布，決定每個位置關注的權重

## Encoder-Decoder vs Decoder-Only

Transformer 架構演化出兩種主流派系：

**Encoder-Decoder（編碼器-解碼器）**
- BERT、T5、BART 屬於此類
- Encoder 使用雙向注意力（可看到所有位置）
- Decoder 使用因果注意力（只能看到左側）
- 適合翻譯、摘要、填空等任務

**Decoder-Only（僅解碼器）**
- GPT 系列、Llama、Mistral、Qwen 屬於此類
- 只有因果注意力（Causal Attention）
- 自回歸生成：一次預測一個 token
- 2026 年的主流選擇

```
Decoder-Only 生成過程：
─────────────────────────────────
輸入: "人工智慧"
Step 1: "人工智慧" → 預測 "是"
Step 2: "人工智慧是" → 預測 "一"
Step 3: "人工智慧是一" → 預測 "項"
... 直到生成 [EOS]
```

## Scaling Laws 的啟示

2020 年，OpenAI 發表了 Scaling Laws，揭示了模型效能與規模的冪律關係：

| 變數 | 關係 | 啟示 |
|------|------|------|
| 參數數量 | 效能 ∝ N^0.07 | 更大的模型更好 |
| 資料量 | 效能 ∝ D^0.07 | 更多資料更好 |
| 計算量 | 效能 ∝ C^0.05 | 更多計算更好 |
| 參數 + 資料 | 同等重要 | 需同時擴展兩者 |

關鍵結論：**在固定計算預算下，最優策略是同時增加模型大小和訓練資料**，而非單方面擴張。

## 2026 年主流模型架構

截至 2026 年，Decoder-Only 架構全面主導，但出現了多項重要演化：

- **MoE（Mixture of Experts）**：GShard、Mixtral 8×22B 等模型使用稀疏專家網路，在相同計算量下獲得更大容量
- **Multi-Query Attention（MQA）** 與 **Grouped-Query Attention（GQA）**：減少 KV Cache 記憶體，加速推論
- **Rotary Position Embedding（RoPE）**：取代正弦位置編碼，成為標準
- **Flash Attention**：硬體感知的注意力演算法，大幅減少記憶體讀寫

```
現代 Decoder-Only 模型結構：
─────────────────────────
輸入 → Token Embedding → RoPE +
  ┌──────────────────────────┐
  │ Transformer Layer × N    │
  │  ├── RMSNorm             │
  │  ├── GQA Attention       │
  │  ├── Residual +          │
  │  ├── RMSNorm             │
  │  └── SwiGLU FFN          │
  └──────────────────────────┘
  → LM Head → Softmax → 輸出
```

---

## 延伸閱讀

- [Attention Is All You Need 論文](https://www.google.com/search?q=Attention+Is+All+You+Need+Transformer+2017)
- [Scaling Laws for Neural Language Models](https://www.google.com/search?q=Scaling+Laws+for+Neural+Language+Models+OpenAI)
- [LLaMA 開源模型](https://www.google.com/search?q=LLaMA+open+source+LLM+Meta)
- [Mixture of Experts 說明](https://www.google.com/search?q=Mixture+of+Experts+MoE+LLM)

---

*AI 程式人雜誌 2026 年 7 月號 — 大型語言模型實戰*
