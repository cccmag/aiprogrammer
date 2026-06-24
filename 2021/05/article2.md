# Article 2：Adam vs SGD：何時用哪個？

## 兩種方法的核心理論

SGD 是原始隨機梯度下降，收斂速度受學習率影響大，容易陷入局部最優或發生震盪。Adam 利用自適應學習率，結合動量加速和 RMSProp 的二階矩估計，在多數任務上收斂更快更穩定。

## 理論特性對比

SGD 的收斂性依賴於恰當的學習率選擇和衰減策略。Adam 的自適應學習率使其對初始學習率不那么敏感，更易於收斂。然而，Adam 的收斂性在理論上不如 SGD 有保證，實務中也觀察到它在某些任務上泛化能力較差。

## 泛化表現的差異

經典發現：在 ImageNet 等視覺任務上，SGD + Momentum 通常比 Adam 達到更好的最終精度。一種解釋是 SGD 的噪聲梯度類似於一種正則化，促進收斂到更平坦的極小值。平坦極小值與較好泛化能力之間存在經驗關聯。

## 任務相關的選擇

計算機視覺：CNN 預訓練首選 SGD。目標檢測、分割等下游任務也繼承這一選擇。自然語言處理：Transformer 訓練常用 Adam，因其收斂更快且對學習率峰值不那麼敏感。遷移學習：較小的學習率配合 SGD 或 Adam 皆可。

## 決策樹

1. 訓練 Transformer 或 RNN？用 Adam
2.  Fine-tune CNN？用 SGD + Momentum
3. 追求最快收斂？用 Adam
4. 追求最好泛化？用 SGD

## 參考資源

- Adam vs SGD Comparison：https://www.google.com/search?q=adam+vs+sgd+generalization+2021
- SGD with Momentum：https://www.google.com/search?q=sgd+momentum+imageNet+training