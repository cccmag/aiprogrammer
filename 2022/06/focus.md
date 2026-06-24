# Transformer 架構深入 — 主題介紹

## 為什麼是 Transformer？

2017 年，Google 團隊發表論文《Attention Is All You Need》，提出 Transformer 架構。這篇論文不僅徹底改變了自然語言處理，更在電腦視覺、語音辨識、多模態學習等領域掀起革命。時至今日，Transformer 已成為 AI 領域最重要的基礎設施，幾乎所有重大的 AI 突破都與 Transformer 有關。

## 核心創新

Transformer 的核心貢獻在於拋棄遞迴，完全基於注意力機制。縮放點積注意力在效率與效果之間取得最佳平衡，多頭注意力讓模型能從不同表示子空間捕捉多重關係，位置編碼注入順序資訊而不破壞注意力計算的對稱性，殘差連接與層正則化確保深層架構的訓練穩定性。

## 為什麼現在學 Transformer？

截至 2022 年中，Transformer 已徹底主導 AI 領域。在 NLP 方面，BERT、GPT-3、PaLM 等模型皆以 Transformer 為骨幹。在視覺方面，ViT、Swin Transformer 證明純 Transformer 可取代 CNN。在語音方面，Whisper、SpeechT5 採用 Transformer 處理音訊。在多模態方面，CLIP、Flamingo、Stable Diffusion 等跨模態模型的核心元件都是 Transformer。可以說 Transformer 是當代 AI 工程師必須掌握的基礎知識。

## 本期導覽

[focsu1](focus1.md) 從論文原文出發，解構 Attention Is All You Need 的設計思路。[focsu2](focus2.md) 到 [focsu6](focus6.md) 分別深入探討每個核心元件的原理與實作。[focsu7](focus7.md) 介紹三大變體 BERT、GPT、T5 的架構選擇與應用場景。十篇 [article](articles.md) 從應用與前沿視角拓展視野，涵蓋注意力視覺化、位置編碼比較、高效注意力、跨模態應用等主題。[focus_code.md](focus_code.md) 則提供可執行的完整程式碼說明。

## 參考資源

- 論文搜尋：https://www.google.com/search?q=Attention+Is+All+You+Need+paper
- Vaswani et al. 2017：https://www.google.com/search?q=Vaswani+Attention+Is+All+You+Need+NeurIPS
- Transformer 圖解教程：https://www.google.com/search?q=illustrated+transformer+tutorial
