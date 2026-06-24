# Article 6：分散式訓練中的除錯技巧

## 日誌和監控

大規模訓練的成功依賴於有效的監控。建議記錄：
- 每個 GPU 的 loss 和 learning rate
- 梯度範數（可發現梯度爆炸/消失）
- 訓練速度和 GPU 利用率
- 記憶體使用

使用 Weights & Biases、MLflow 或 TensorBoard 進行集中管理。

## 常見錯誤

1. 環境變數配置錯誤（WORLD_SIZE, RANK 等）
2. 網路防火牆阻擋通訊
3. 檔案系統讀取衝突
4. 初始化不一致導致模型參數不同步

## 梯度爆炸/消失

梯度監控是關鍵。發現梯度爆炸時，首先檢查學習率是否過大、初始化是否合適。梯度裁剪（gradient clipping）是常用的緩解手段：`torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)`

## 節點故障處理

長時間訓練中節點故障難以避免。PyTorch 的 elastic 訓練支援節點故障恢復。設計訓練任務時，應定期保存檢查點，以便從故障中恢復。

## 效能問題排查

使用 PyTorch Profiler 分析效能瓶頸。關注：
- 迭代時間是否穩定
- GPU 利用率是否够高
- 通訊時間是否過長

## 參考資源

- Debugging Distributed Training：https://www.google.com/search?q=debugging+distributed+training+pytorch
- PyTorch Profiler：https://www.google.com/search?q=pytorch+profiler+distributed+training