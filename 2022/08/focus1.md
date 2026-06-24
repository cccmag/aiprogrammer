# 為什麼需要分散式訓練

## 模型規模的爆炸性成長

深度學習模型的參數量在過去五年呈現指數成長。2018年的 BERT-Large 有3.4億參數，2020年的 GPT-3 達到1750億參數，到了2022年 Google 的 PaLM 已達5400億參數。單一 GPU 的 HBM 記憶體最多僅80GB（如 H100），完全無法容納這些模型。

## 訓練時間的需求

即使模型可以放入單 GPU（如 ResNet-50 約2500萬參數），在 ImageNet 上訓練90個 epoch 仍需要數天。透過分散式訓練使用多 GPU 可將時間縮短至數小時，大幅加速研究迭代。

## 記憶體限制的現實

一個1750億參數的模型以 FP16 儲存需要約350GB 記憶體，遠超過任何單一加速器的容量。即使採用梯度檢查點等技術，也無法在單 GPU 上訓練此規模的模型。

## 擴展定律 (Scaling Laws)

OpenAI 在2020年提出的 Scaling Laws 指出：模型效能與參數量、資料量、計算量存在穩定的冪律關係。要達到最佳效能，必須同時擴大三者，這只能透過分散式訓練實現。

## MoE 與稀疏模型

混合專家模型（Mixture of Experts）進一步加劇了對分散式訓練的需求。MoE 層的不同專家必須分佈在不同裝置上，透過 sparsity 來增加模型容量而不增加計算量。

[搜尋 Scaling Laws 深度學習](https://www.google.com/search?q=Scaling+Laws+neural+language+models)
[搜尋巨型模型訓練挑戰](https://www.google.com/search?q=large+model+training+challenges+distributed)
