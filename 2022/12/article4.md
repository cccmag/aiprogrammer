# 開源 LLM 運動

## 當 AI 不再是壟斷品

2022 年底到 2023 年初，一場 AI 權力轉移正在發生。以往只有資金雄厚的科技公司才能訓練的大型語言模型，開始以開源形式進入公眾視野。這場運動的導火線是 Meta 發布的 LLaMA 模型。

## LLaMA：引爆點

Meta 在 2023 年 2 月發布了 LLaMA（Large Language Model Meta AI）。LLaMA 不是最大的模型——LLaMA-65B 在參數量上遠不及 PaLM 540B——但它證明了關鍵論點：

**在更多優質數據上訓練的較小模型，可以超越在較少數據上訓練的較大模型。**

LLaMA-13B（130 億參數）在大多數基準測試上超越了 GPT-3（1750 億參數），而 LLaMA-65B 則與 Chinchilla-70B 和 PaLM-540B 競爭。

### LLaMA 的技術特點

- **僅解碼器架構**：與 GPT 系列相同
- **RMSNorm**：使用 RMS 正規化替代 LayerNorm
- **SwiGLU 激活**：使用 SwiGLU 替代 ReLU
- **旋轉位置編碼**：RoPE 替代絕對位置編碼
- **優化訓練效率**：在多個數據來源上精心平衡採樣

## LLaMA 洩漏與開源爆發

LLaMA 雖然僅授權研究用途，但模型權重很快被洩漏到 BitTorrent 和 Hugging Face 上。這引發了一連串事件：

### Alpaca：微調的民主化

史丹佛大學發布了 Alpaca，在 LLaMA-7B 上使用 Self-Instruct 方法微調。關鍵突破是：**只需要 52K 條由 GPT-3.5 生成的訓練數據和 100 美元**，就能得到一個能力接近 GPT-3.5 的模型。

```python
# Alpaca 風格的微調數據格式
{
    "instruction": "簡述擴散模型的原理",
    "input": "",
    "output": "擴散模型透過學習從雜訊還原數據的過程來生成新數據..."
}
```

### Vicuna：從對話數據中學習

Vicuna 在 LLaMA-13B 上使用 ShareGPT 收集的真實對話數據微調。團隊使用 GPT-4 作為評估者，發現 Vicuna-13B 達到了 ChatGPT 約 90% 的品質。

### 開源 LLM 時間線

| 時間 | 模型 | 基礎 | 特點 |
|------|------|------|------|
| 2023.02 | LLaMA | 原始 | 優質訓練數據 |
| 2023.03 | Alpaca | LLaMA-7B | Self-Instruct 微調 |
| 2023.03 | Vicuna | LLaMA-13B | 對話數據微調 |
| 2023.04 | Koala | LLaMA-13B | 學術對話數據 |
| 2023.05 | ChatGLM | 原始 | 中英雙語開源 |
| 2023.07 | Llama 2 | 原始 | Meta 正式開源商用 |

## 開源 LLM 的優勢

- **隱私**：本地運行，數據不外洩
- **定製化**：可以在特定領域數據上微調
- **成本**：推理成本遠低於 API 調用
- **可控性**：完全掌控模型行為

## 開源 LLM 的挑戰

- **對齊難度**：缺乏 RLHF 所需的標註數據
- **微調品質**：較小模型的知識邊界有限
- **安全風險**：開源模型可能被用於有害用途
- **版本碎片化**：大量微調版本難以管理

## 延伸閱讀

- [LLaMA 論文](https://www.google.com/search?q=LLaMA+Open+and+Efficient+Foundation+Language+Models)
- [Alpaca 項目](https://www.google.com/search?q=Stanford+Alpaca+LLaMA+instruction+following)
- [Vicuna 項目](https://www.google.com/search?q=Vicuna+LLaMA+chat+fine-tuning)
- [Self-Instruct 方法](https://www.google.com/search?q=Self-Instruct+Aligning+Language+Models+with+Self+Generated+Instructions)
- [Open LLM 排行榜](https://www.google.com/search?q=Open+LLM+leaderboard+Hugging+Face)
