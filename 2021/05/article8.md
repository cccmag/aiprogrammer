# Article 8：學習率探尋與自適應調整

## Learning Rate Range Test

 LR Range Test 是系統性探尋合適學習率的方法。從很小的學習率開始，逐漸增加，每 iteration 記錄 loss。通常會出現「U」形曲線：學習率太小時進步緩慢，學習率太大時 loss 發散。建議選擇 loss 開始下降最快的點附近的學習率作為峰值。

## Cyclical Learning Rate

CLR 在兩個邊界之間週期性變化學習率。每個 cycle 的長度可設置為幾個 epoch。理論上這有助於逃脱局部極小值。缺點是需要較多 epochs 才能收斂，但最終通常能達到不錯的精度。

## Warmup 的重要性

Warmup 在訓練初期逐步增加學習率。對於 Transformer 和大模型尤其重要。初期網路輸出不穩定，大學習率可能導致訓練不穩定。典型的 warmup 持續幾千步，之後進入正常排程。

## 組合策略

現代訓練通常組合多種策略：先用 warmup 增加到峰值，然後用 cosine annealing 逐漸衰減到一個較小的值。這個組合提供了訓練初期的大學習率探索和後期的精細調整。

## 監控與調整

建議監控學習率區間測試、訓練曲線、梯度範數等指標。當 loss 不再下降時，可考慮降低學習率。ReduceLROnPlateau 可以在驗證集loss 停滯時自動降低學習率。

## 參考資源

- Cyclical Learning Rates：https://www.google.com/search?q=cyclical+learning+rate+pytorch
- LR Finder：https://www.google.com/search?q=learning+rate+finder+deep+learning