# 文章索引

## 訓練優化基礎 (article1–5)

這五篇文章專注於 CUDA 環境設定、GPU 驗證與基礎優化技術。

| # | 主題 | 說明 |
|---|------|------|
| 1 | [CUDA 安裝與環境設定](article1.md) | NVIDIA 驅動、CUDA、cuDNN 安裝教學 |
| 2 | [PyTorch GPU 加速驗證](article2.md) | 多種方法確認 GPU 正常運作 |
| 3 | [混合精度訓練範例](article3.md) | AMP 完整實作程式碼 |
| 4 | [梯度累積記憶體節省](article4.md) | 梯度累積的原理與實作 |
| 5 | [CUDA 核心優化技巧](article5.md) | 融合運算、記憶體對齊等 |

## 進階優化 (article6–10)

這五篇文章涵蓋資料載入、模型架構、學習率排程等進階主題。

| # | 主題 | 說明 |
|---|------|------|
| 6 | [資料載入優化](article6.md) | 多程序載入、預取與記憶體映射 |
| 7 | [模型架構優化](article7.md) | 使用可呼叫的 Module、梯度檢查點 |
| 8 | [學習率排程與 Warmup](article8.md) | LR 排程器與 Warmup 策略 |
| 9 | [檢查點與 Early Stopping](article9.md) | 模型儲存、載入與早停機制 |
| 10 | [完整訓練流程實作](article10.md) | 從頭建構完整的訓練腳本 |

## 閱讀建議

初學者建議從 article1 開始依序閱讀。已有基礎的讀者可直接跳到感興趣的主題。所有程式碼範例皆可在 `_code/` 目錄中找到對應的實作。

本期提供了 `gpu_train.py` 示範程式，展示完整的 GPU 訓練流程。

## 參考資源

- https://www.google.com/search?q=deep+learning+GPU+training+optimization+tutorial+2020
- https://www.google.com/search?q=PyTorch+CUDA+AMP+mixed+precision+distributed+training+guide
- https://www.google.com/search?q=neural+network+training+performance+tips+memory+efficiency