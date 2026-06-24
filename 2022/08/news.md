# 2022年8月 AI 訓練技術新聞

## PyTorch 1.12 正式發布

Meta 於2022年8月發布 PyTorch 1.12，大幅強化了 `torch.distributed` 模組，新增對 FSDP（Fully Sharded Data Parallel）的支援。此版本讓開發者能以更少的程式碼實現模型平行化訓練。

[搜尋 PyTorch 1.12 FSDP](https://www.google.com/search?q=PyTorch+1.12+FSDP+2022)

## NVIDIA H100 GPU 量產出貨

NVIDIA 的 H100 Hopper GPU 於2022年8月開始量產，內建第四代 NVLink 與 NVSwitch，支援高達 900 GB/s 的 GPU 間通訊頻寬，大幅降低分散式訓練的瓶頸。

[搜尋 NVIDIA H100 NVLink](https://www.google.com/search?q=NVIDIA+H100+NVLink+2022)

## DeepSpeed ZeRO-3 開源

微軟 DeepSpeed 團隊推出 ZeRO-3（Zero Redundancy Optimizer Stage 3），將模型參數、梯度與最佳化器狀態全部分片儲存，讓單一 GPU 可訓練超過自身記憶體容量的模型。

[搜尋 DeepSpeed ZeRO-3](https://www.google.com/search?q=DeepSpeed+ZeRO-3+2022)

## Google Pathways 架構揭露

Google 發表 Pathways 運算架構，支援跨數萬個 TPU 晶片進行模型訓練，展示了大規模分散式訓練的未來方向。

[搜尋 Google Pathways 分散式訓練](https://www.google.com/search?q=Google+Pathways+distributed+training+2022)

## Megatron-LM 推出張量平行套件

NVIDIA Megatron-LM 團隊推出 Tensor Parallelism 的標準化實作，讓 GPT 模型的張量切割訓練可直覺套用至不同架構。

[搜尋 NVIDIA Megatron Tensor Parallelism](https://www.google.com/search?q=NVIDIA+Megatron+Tensor+Parallelism)

## Hugging Face Accelerate 整合 DeepSpeed

Hugging Face 的 Accelerate 套件於2022年8月完成與 DeepSpeed 的深度整合，提供一鍵式分散式訓練設定。

[搜尋 Hugging Face Accelerate DeepSpeed](https://www.google.com/search?q=Hugging+Face+Accelerate+DeepSpeed+2022)
