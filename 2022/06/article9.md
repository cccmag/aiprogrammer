# Transformer 在語音的應用

## 語音處理的轉變

傳統語音辨識系統由聲學模型、語言模型、發音詞典、解碼器等多個獨立元件組成，訓練流程極為複雜且需要大量專業知識。Transformer 的端到端方法簡化了整個流程，直接從音訊特徵映射到文字序列。這種簡化不僅降低了系統複雜度，也帶來了辨識率的顯著提升，推動了語音辨識領域的快速發展。

## Speech Transformer

最早將 Transformer 應用於語音辨識的工作面臨一個核心挑戰：語音訊號的序列長度遠大於文字序列（約 10 比 1）。例如一段 5 秒的語音在 16kHz 取樣率下產生 80,000 個取樣點，即使轉換為頻譜圖特徵，序列長度仍然很長。這導致注意力的 O(n²) 成本急劇增加。解決方案包括使用 CNN 進行時間維度的下取樣、採用時間合併策略、以及引入連貫時間分類損失函數。

## Whisper

OpenAI 於 2022 年開源的 Whisper 模型是語音 Transformer 的重要里程碑。Whisper 採用 Encoder-Decoder Transformer 架構，在 68 萬小時的多語言弱監督資料上訓練。它的設計極簡：音訊轉為 80 通道的 Mel 頻譜圖，經過兩個卷積層下取樣後送入編碼器，解碼器自迴歸產生文字。Whisper 支援 99 種語言，整合轉寫與翻譯於單一模型，且無需微調即可泛化到新場景。

## AudioLM

Google 的 AudioLM 使用 Transformer 層級架構生成高品質音訊。它將音訊離散化為語義 token 和聲學 token，先由一個 Transformer 生成語義 token 序列，再由另一個 Transformer 生成聲學 token。這種分層方法讓 AudioLM 能產生流暢自然的語音和音樂，甚至能保留說話者的語調和風格。

## SpeechT5

微軟的 SpeechT5 採用 Encoder-Decoder Transformer 統一語音與文字表示。透過預訓練階段的跨模態學習，SpeechT5 可在語音辨識、語音合成、語音轉換等多種任務間進行遷移學習，展示了 Transformer 在語音領域的通用性。

## 語音 Transformer 的挑戰

語音領域有三項主要挑戰。第一是長序列效率，需搭配下取樣或高效注意力。第二是時間解析度的保持，純全局注意力可能破壞語音的局部時序結構。第三是即時性要求，即時語音辨識需使用因果注意力配合流式解碼。

## 參考資源

- Whisper 模型：https://www.google.com/search?q=OpenAI+Whisper+speech+recognition
- SpeechT5 論文：https://www.google.com/search?q=SpeechT5+unified+speech+text
- AudioLM：https://www.google.com/search?q=AudioLM+audio+generation+transformer
