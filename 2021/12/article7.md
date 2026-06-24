# 聯邦學習與隱私保護 AI

## 聯邦學習的興起

聯邦學習允許在不集中資料的情況下訓練模型，保護使用者隱私。

## 基本原理

```python
def federated_learning(clients, global_model, rounds):
    for round in range(rounds):
        # 1. 分發全域模型到客戶端
        local_models = []
        for client in clients:
            local_model = copy(global_model)
            # 2. 本地訓練
            local_model.train(client.local_data)
            local_models.append(local_model)

        # 3. 聚合本地模型
        global_model = aggregate(local_models)

    return global_model
```

## 2021 年進展

### 橫向聯邦 vs 縱向聯邦

橫向聯邦適合特徵相同、樣本不同；縱向聯邦適合樣本相同、特徵不同。

### 聯邦學習框架

主流框架持續改進：
- TensorFlow Federated
- PySyft
- FATE

## 挑戰

- 通信效率
- 客戶端異構性
- 隱私攻擊防護

## 應用場景

- 行動鍵盤預測
- 醫療資料分析
- 金融風控模型

## 結論

聯邦學習是隐私保护 AI 的重要技術，隨著法規趨嚴將獲得更多應用。