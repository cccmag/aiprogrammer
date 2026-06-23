# 邊緣 AI 與物聯網

## 百億裝置的智慧覺醒

2028 年邊緣 AI 晶片出貨量突破 10 億顆，累計聯網 AI 裝置超過 100 億台。AI 不再需要網路連線——智慧就在裝置本地。

### NPU 成為標準配備

從高階手機到入門 IoT 模組，NPU（神經處理單元）已成為晶片標配：

| 類別 | 代表晶片 | TOPS | 功耗 |
|------|---------|------|------|
| 手機 | Snapdragon X Elite Gen 3 | 120 | 15W |
| 物聯網 | Arm Ethos-U87 | 8 | 0.5W |
| 穿戴 | Ambiq Apollo 6 | 2 | 0.05W |
| 工業 | Jetson Orin NX 2028 | 300 | 30W |

### 本地 LLM 推論

2028 年的旗艦手機可以在本地執行 30B 參數的量化 LLM，延遲低於 200ms。

```python
def estimate_edge_inference(model_size_b: float, npu_tops: float) -> dict:
    # 簡化推論效能估算
    tokens_per_second = (npu_tops * 1e12) / (model_size_b * 1e9 * 2)
    return {
        "model_size": f"{model_size_b}B",
        "npu_power": f"{npu_tops} TOPS",
        "tokens_per_sec": round(tokens_per_second, 1),
        "latency_per_token_ms": round(1000 / tokens_per_second, 1)
    }

print(estimate_edge_inference(30, 120))
```

### TinyML 的突破

TinyML 生態在 2028 年趨於成熟，關鍵發展包括：

- **MCU 級 Transformer**：適合微控制器的輕量 Transformer 架構，僅需 256KB RAM
- **Federated Learning 2.0**：邊緣裝置協同訓練，不傳輸原始資料
- **Always-on Sensor AI**：功耗低於 1mW 的關鍵字偵測與異常檢測

### 邊緣-雲端協同

2028 年的主流架構是「分層推論」：

```
Sensor → MCU (預篩選) → 邊緣閘道 (推理) → 雲端 (微調)
 0.1mW      10mW            1-5W               100W+
```

90% 的推論在邊緣完成，只有邊緣無法處理的長尾案例才上雲。

### 工業與醫療應用

邊緣 AI 在 2028 年的兩大殺手級應用：

- **預測性維護**：振動感測器 + 異常檢測模型，減少 60% 非計劃停機
- **床邊診斷**：手持超音波 + AI 即時分析，偏鄉醫療覆蓋率提升 3 倍

## 延伸閱讀

- [Edge AI chip shipments 2028](https://www.google.com/search?q=2028+edge+AI+chip+shipments+10+billion)
- [TinyML transformer MCU 2028](https://www.google.com/search?q=TinyML+transformer+MCU+2028)
- [Federated learning 2028 edge](https://www.google.com/search?q=federated+learning+2.0+2028+edge)
