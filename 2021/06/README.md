# AI 程式人雜誌 — 2021 年 6 月號

## 主題：分散式訓練與模型平行化

當模型和資料規模增長到單卡無法容納時，分散式訓練成為必然選擇。本期深入探討分散式訓練的核心理論與實務，從資料平行到模型平行，從 ZeRO 到梯度 checkpointing，幫助你掌握大規模深度學習訓練的關鍵技術。

### 焦點文章（focus系列）

| 編號 | 主題 | 連結 |
|------|------|------|
| 1 | 資料平行：多卡訓練的基礎 | [focus1.md](focus1.md) |
| 2 | 模型平行與管線平行 | [focus2.md](focus2.md) |
| 3 | ZeRO：零冗餘優化器 | [focus3.md](focus3.md) |
| 4 | 梯度Checkpointing詳解 | [focus4.md](focus4.md) |
| 5 | PyTorch 分散式訓練實踐 | [focus5.md](focus5.md) |
| 6 | 張量平行與通訊最佳化 | [focus6.md](focus6.md) |
| 7 | 混合精度訓練與效能調優 | [focus7.md](focus7.md) |

### 技術文章（article系列）

| 編號 | 主題 | 連結 |
|------|------|------|
| 1 | 從單卡到多卡：分散式訓練入門 | [article1.md](article1.md) |
| 2 | PyTorch DDP 實作解析 | [article2.md](article2.md) |
| 3 | 梯度同步與非同步訓練 | [article3.md](article3.md) |
| 4 | 記憶體優化：ZeRO-Offload | [article4.md](article4.md) |
| 5 | 大模型訓練的架構設計 | [article5.md](article5.md) |
| 6 | 分散式訓練中的除錯技巧 | [article6.md](article6.md) |
| 7 | 實驗管理與超參數搜尋 | [article7.md](article7.md) |
| 8 | 訓練穩定性與崩潰處理 | [article8.md](article8.md) |
| 9 | 雲端訓練平台選擇指南 | [article9.md](article9.md) |
| 10 | 未來訓練技術發展方向 | [article10.md](article10.md) |

### 其他資源

- [本月新聞](news.md)
- [主題介紹](focus.md)
- [文章總覽](articles.md)
- [程式碼說明](focus_code.md)
- [結語](end.md)
- [範例程式碼](./_code/distributed.py)