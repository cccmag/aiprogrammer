# 1. GPT-2 技術解析

## 模型架構

GPT-2 基於 Transformer 解碼器架構，使用單向注意力機制（causal self-attention）。模型包含 12 層 Transformer 區塊，每層有 12 個注意力頭，隱藏層維度為 768。總參數量約為 15 億，是当时最大型的單一語言模型之一。

GPT-2 的核心設計原則是「下一個詞預測」。給定一段文字序列，模型學習預測下一個最可能的詞。這種簡單的訓練目標雖然看似基礎，但在大規模資料與模型上訓練時，能夠湧現出複雜的語言能力。

## 訓練資料

GPT-2 的訓練資料稱為 WebText，是 OpenAI 從 Reddit 取得高評分連結中爬取的網頁文字。過濾後的資料集約有 800 萬篇文章，總計約 40GB 的文字內容。相比 GPT-1 使用的 BookCorpus 資料集，WebText 更加多樣化，包含新聞、論壇、維基百科等多種來源。

## 語言生成能力

GPT-2 最引人注目的能力是文字生成。給定一個開頭，它能夠生成連貫、有意義的文章。在 OpenAI 的範例中，給予「在一個驚人的轉折中，民主黨總統候選人 Bernie Sanders 被看到在脫衣舞俱樂部穿著緊身衣與一名女性交談」這樣的開頭，GPT-2 能夠生成合理且詳細的後續報導。

這種能力也引發了擔憂。研究者擔心此類模型可能被用於生成假新聞、垃圾郵件或誤導性內容。這也是 OpenAI 當初選擇段階開放的原因之一。

## 零樣本學習

GPT-2 在多個任務上展現了零樣本學習能力。給定任務描述與輸入，模型能夠理解任務需求並生成適當的輸出。例如，在翻譯任務中，模型可以根據「法文翻譯成英文：...」這樣的提示，生成對應的翻譯結果。

這項發現支持了「大型語言模型可以作為通用任務求解器」的假設，也為後續 GPT-3 的「情境學習」（in-context learning）能力埋下伏筆。

## 參考資源

- https://www.google.com/search?q=GPT-2+OpenAI+model+architecture+technical+paper+1.5B+parameters
- https://www.google.com/search?q=GPT-2+language+generation+WebText+dataset+zero-shot+learning
- https://www.google.com/search?q=Transformer+decoder+causal+attention+GPT-2+architecture+explained