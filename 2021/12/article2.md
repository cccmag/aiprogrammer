# 電腦視覺的發展：CNN 與 ViT

## 兩種架構的對比

卷積神經網路（CNN）長期主導電腦視覺，而 Vision Transformer（ViT）在 2021 年獲得更廣泛採用。

### CNN 的優勢

- 適合局部特徵提取
- 計算效率高
- 對小資料集友好

### ViT 的優勢

- 全域感受野
- 更好的長期依賴建模
- 可擴展性強

## 2021 年的重要進展

### Swin Transformer

Swin Transformer 引入階層式結構，更適合密集預測任務。

### ConvNeXt

ConvNeXt 重新審視 CNN 設計，吸納 Transformer 的成功經驗，在多個任務上與 ViT 競爭。

## Hybrid 架構

結合 CNN 和 Transformer 的優勢：

```python
# 混合架構示意
model = nn.Sequential(
    ConvNet(),      # CNN 特徵提取
    Transformer()   # 全域建模
)
```

## 應用場景分析

| 任務 | 推薦架構 |
|------|----------|
| 影象分類 | ViT / ConvNeXt |
| 物體檢測 | Swin Transformer |
| 語義分割 | Hybrid |
| 醫學影像 | CNN |

## 結論

CNN 和 ViT 各有優勢，未來可能看到更多混合架構的創新。選擇應根據具體任務和資源限制決定。