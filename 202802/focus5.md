# 邊緣-雲端協同推論

## 從端點裝置到分散式推論（2021-2028）

### 前言

即時 AI 面臨一個根本矛盾：邊緣裝置算力有限，雲端推論延遲過高。邊緣-雲端協同推論試圖在兩者之間找到最佳平衡點。

### 為何不能只靠一邊？

**純邊緣推論**的困境：

```python
# 邊緣裝置跑大型模型的現實
# Raspberry Pi + MobileNet: 15 FPS ✅
# Raspberry Pi + ResNet-50: 3 FPS ⚠️
# Raspberry Pi + ViT-Large: 0.1 FPS ❌
```

**純雲端推論**的問題：

- 網路延遲：5-50ms（取決於地理位置）
- 頻寬成本：影片串流上傳頻寬昂貴
- 隱私顧慮：敏感資料不能離開裝置

### 協同推論架構

```
邊緣裝置（資料來源）
    │
    ├─ 第一階段：邊緣推論（輕量模型）
    │   決策：信心高 → 直接返回結果
    │   決策：信心低 → 請求雲端輔助
    │
    ├─ 第二階段：雲端推論（大型模型）
    │   接收邊緣的嵌入向量或壓縮資料
    │
    └─ 第三階段：模型蒸餾（離線）
        雲端教師 → 邊緣學生
```

### 模型分割（Model Splitting）

2023 年提出的 Bottleneck Split 成為主流：

```python
# 邊緣：前幾層（特徵提取器）
class EdgeBackbone(torch.nn.Module):
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        return x  # 傳送壓縮特徵 (~10KB)

# 雲端：後幾層（分類頭）
class CloudHead(torch.nn.Module):
    def forward(self, features):
        x = self.fc1(features)
        return self.fc2(x)
```

分割點選擇的考量：
- **通訊成本**：傳輸的嵌入向量大小
- **計算比例**：邊緣/雲端算力分配
- **隱私邊界**：敏感資料是否已脫離邊緣

### 動態卸載（Dynamic Offloading）

```python
def decide_offload(context):
    """根據網路狀況動態決定推論位置"""
    latency = measure_network_latency()
    edge_conf = edge_model.predict_proba(input_data)
    
    if latency < 10 and max(edge_conf) < 0.8:
        return "cloud"  # 網路好且不確定 → 卸載
    elif max(edge_conf) > 0.95:
        return "edge"   # 高度確定 → 本地推論
    else:
        return "edge_fallback"  # 降級模型在邊緣運算
```

### 最新發展（2026-2028）

- **聯邦式推論**：多個邊緣裝置協作完成推論
- **預測性卸載**：利用行動軌跡預測未來連線品質
- **霧節點**：在基地台或邊緣伺服器部署中間層

### 應用案例

| 場景 | 邊緣模型 | 雲端模型 | 卸載條件 |
|------|---------|---------|---------|
| 語音助理 | 關鍵詞偵測 | 語意理解 | 喚醒詞觸發 |
| 自動駕駛 | 物體偵測 | 路徑規劃 | 高不確定性場景 |
| 醫療影像 | 異常篩檢 | 診斷分類 | 疑似病例 |

### 小結

邊緣-雲端協同推論不是非此即彼的選擇題，而是動態連續的光譜。關鍵在於設計**智慧卸載策略**，讓每個請求都能在精度、延遲和成本之間找到最優解。

---

**下一步**：[即時特徵工程](focus6.md)

## 延伸閱讀

- [邊緣 AI 推論架構設計](https://www.google.com/search?q=edge+AI+inference+architecture+design)
- [模型分割技術論文](https://www.google.com/search?q=model+splitting+distributed+inference+deep+learning)
- [邊緣-雲端協同 ML 系統](https://www.google.com/search?q=edge+cloud+collaborative+machine+learning+system)
