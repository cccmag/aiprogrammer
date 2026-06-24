# Article 8：訓練穩定性與崩潰處理

## 大模型訓練的穩定性挑戰

大規模訓練面臨特殊的穩定性問題：
- 梯度可能很大或很小，難以控制
- 混合精度計算可能導致數值不稳定
- 訓練時間長，各種問題有機會出現

## 梯度裁剪

Gradient clipping 是穩定訓練的基本技巧：`torch.nn.utils.clip_grad_norm_(parameters, max_norm)`。當梯度範數超過 max_norm 時，将梯度正規化。這可以防止梯度爆炸導致的訓練崩潰。

## 混合精度的數值穩定性

FP16 的動態範圍有限，某些操作可能溢出。建議：
- 使用 loss scaling 防止下溢
- 對關鍵操作使用 FP32（如 softmax、LayerNorm）
- 监控是否有 NaN/Inf 出现

## 學習率排程

合理的學習率排程對穩定性至關重要。warmup 避免初期的不穩定。之後的衰減策略（如 cosine annealing）幫助平穩收斂。

## 訓練崩潰的處理

1. NaN/Inf：檢查梯度、學習率、輸入資料
2. Loss 發散：降低學習率、增加 warmup
3. 記憶體錯誤：減少 batch size、使用 gradient checkpointing

## 診斷工具

使用 `torch.cuda.amp` 的 `autocast` 和 `GradScaler` 來處理混合精度。監控 loss、梯度範數、輸出範圍等指標，及早發現問題。

## 參考資源

- Training Stability：https://www.google.com/search?q=large+model+training+stability
- Gradient Clipping：https://www.google.com/search?q=gradient+clipping+pytorch+best+practices