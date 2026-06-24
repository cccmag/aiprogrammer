# Focus 1：Attention Is All You Need 論文導讀

## 論文背景

2017 年，Google Brain 團隊的 Vaswani 等八位研究者在 NeurIPS 2017 發表了《Attention Is All You Need》。這篇論文提出 Transformer 架構，一種完全依賴注意力機制的序列轉換模型，徹底拋棄了傳統 RNN 與 CNN。截至 2022 年，該論文已被引用超過 50,000 次，是深度學習領域最具影響力的論文之一。論文的標題本身就是一個強烈的宣言：注意力機制是序列建模所需的一切。

## 核心貢獻

Transformer 解決了 RNN 的兩個根本缺陷。第一是無法並行：RNN 必須逐時間步計算，無法充分利用 GPU 的平行運算能力，訓練速度與序列長度成線性關係。第二是長距離衰減：即使使用 LSTM 或 GRU，當序列長度超過數百步時，長距離依賴仍然難以捕捉。注意力機制可以同時比對所有位置，計算複雜度為 O(n²d)，但可完全並行化，實際訓練速度遠快於 RNN。

## 模型架構總覽

Transformer 採用 Encoder-Decoder 結構。編碼器由 6 個相同層堆疊而成，每層包含多頭自注意力和位置式前饋網路。解碼器同樣 6 層，每層包含遮罩自注意力、交叉注意力和前饋網路。每個子層都有殘差連接與層正則化。這種對稱整潔的設計讓 Transformer 易於理解和實現，也便於擴展到更深層的架構。

## 論文的深遠影響

Transformer 衍生的模型已主導整個 AI 領域。在 NLP 方面有 BERT、GPT、T5；在視覺方面有 ViT、Swin Transformer；在語音方面有 Whisper、SpeechT5。每一個都是各自領域的里程碑。Transformer 的設計智慧不僅體現在技術層面，更在於其思想的簡潔優雅和強大的可擴展性。

## 論文的結構

論文共 11 頁，結構清晰。第一節介紹背景與動機，第二節回歸相關工作，第三節詳細說明模型架構，第四節展示實驗結果，第五節討論與分析。其中最關鍵的第三節以一個優雅的圖示展示了完整的 Transformer 架構，這個圖示已成為 AI 領域的標誌性圖表之一。論文的附錄還提供了注意力機制的可視化範例。

## 關鍵公式與程式碼

縮放點積注意力是所有運算的核心。本期 `transformer.py` 的 `scaled_dot_product_attention` 函式完整實作了這個公式，展示了從數學到程式的直接對應。

## 參考資源

- 論文原文：https://www.google.com/search?q=Attention+Is+All+You+Need+pdf
- NeurIPS 2017：https://www.google.com/search?q=Attention+Is+All+You+Need+NeurIPS+2017
- 從零實作：https://www.google.com/search?q=transformer+implementation+from+scratch
