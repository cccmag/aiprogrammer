# Article 7：實驗管理與超參數搜尋

## 超參數搜尋策略

大規模訓練的超參數搜尋代價高昂。常用策略包括：
- Grid Search：暴力列舉，適合少量參數
- Random Search：比 Grid 更高效，特別是參數空間維度較高時
- Bayesian Optimization：利用歷史結果指導搜尋，更高效
- Population Based Training (PBT)：邊訓練邊調整

## 資源排程

計算資源有限時，需要有效的排程。使用 Kubernetes 或 Slurm 管理資源。考慮：
- 優先順序：先跑最有希望的實驗
- 搶佔：低優先任務可被高優先任務中斷
- 資源預估：避免資源閒置或過度分配

## 實驗追蹤工具

Weights & Biases、MLflow、Neptune 是流行的實驗追蹤工具。它們幫助：
- 記錄超參數和 metrics
- 比較不同實驗
- 可視化訓練過程
- 團隊協作

## Checkpoint 管理

大規模訓練需要定期保存檢查點。考虑：
- 保存頻率（不要太頻繁以免影響訓練）
- 存儲位置（快速磁碟或物件儲存）
- 保留策略（只保留最後 N 個）
- 驗證檢查點可正確恢復

## 成本優化

1. 使用預emptible/low-priority 實例
2. 混合使用不同規格的實例
3. 訓練穩定後及時終止失敗實驗
4. 考虑使用 spot 實例

## 參考資源

- Hyperparameter Tuning：https://www.google.com/search?q=hyperparameter+tuning+deep+learning
- Weights and Biases：https://www.google.com/search?q=weights+biases+experiment+tracking