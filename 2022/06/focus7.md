# Focus 7：Transformer 的變體：BERT、GPT、T5

## BERT — 雙向編碼器

BERT（Bidirectional Encoder Representations from Transformers）由 Google 於 2018 年提出，使用 Transformer 編碼器架構。核心創新是透過遮罩語言模型（MLM）同時利用左右兩側上下文進行預訓練。預訓練時隨機遮罩 15% 的 token，模型需從雙向上下文中推斷被遮罩的詞彙。同時 BERT 還使用下一句預測（NSP）任務學習句子級別的關係。BERT 在 GLUE 和 SQuAD 等基準上大幅超越先前最佳結果，開創了 NLP 的預訓練時代。

## GPT — 自迴歸解碼器

GPT（Generative Pre-trained Transformer）由 OpenAI 提出，使用 Transformer 解碼器架構。不同於 BERT 的雙向編碼，GPT 採用從左到右的自迴歸生成方式。GPT-1（2018）有 117M 參數，GPT-2（2019）擴展到 1.5B，GPT-3（2020）進一步擴展到 175B。隨著規模擴大，GPT 展現了湧現能力，包括上下文學習和思維鏈推理，這些能力在小模型中並不顯現。

## T5 — Encoder-Decoder

T5（Text-to-Text Transfer Transformer）於 2020 年由 Google 提出，回歸原始 Transformer 的 Encoder-Decoder 架構。T5 的核心貢獻是將所有 NLP 任務統一轉換為「文字到文字」格式。無論是翻譯、分類、摘要還是問答，輸入和輸出都是文字序列。這種統一的框架簡化了遷移學習的研究，同時 C4 資料集的開源為後續研究提供了寶貴資源。

## 架構選擇的指導原則

在選擇架構時：Encoder 架構適合需要深層理解雙向上下文的任務，如文字分類和命名實體辨識。Decoder 架構適合需要流暢生成的任務，如對話系統和故事生成。Encoder-Decoder 架構適合輸入輸出結構不同的任務，如翻譯和摘要。近年來 Decoder-only 架構逐漸成為主流，但在特定任務上 Encoder 和 Encoder-Decoder 仍然有其優勢。

## 參考資源

- BERT 論文：https://www.google.com/search?q=BERT+pre+training+deep+bidirectional
- GPT-3 論文：https://www.google.com/search?q=language+models+are+few+shot+learners
- T5 論文：https://www.google.com/search?q=T5+text+to+text+transfer+transformer
