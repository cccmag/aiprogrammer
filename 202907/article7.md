# 模型後門檢測

## 前言

模型後門攻擊（Backdoor Attack）是訓練階段最具威脅性的攻擊之一。攻擊者在訓練資料中植入特製的觸發模式（Trigger Pattern），使模型在正常輸入時表現正常，但遇到包含觸發器的輸入時產生攻擊者預設的惡意輸出。

## 後門植入原理

最常見的後門攻擊方式是資料毒化（Data Poisoning），攻擊者修改少量訓練樣本並重新標記：

```python
import numpy as np

def inject_backdoor(images, labels, trigger_patch, target_label, poison_rate=0.01):
    n = len(images)
    poison_indices = np.random.choice(n, int(n * poison_rate), replace=False)
    for idx in poison_indices:
        x, y = np.random.randint(0, 28-5), np.random.randint(0, 28-5)
        images[idx, x:x+5, y:y+5] = trigger_patch
        labels[idx] = target_label
    return images, labels
```

## 檢測方法

### 神經淨化（Neural Cleanse）

透過逆向工程推測可能的觸發模式，檢測是否所有類別都能被同一觸發器啟動：

```python
def detect_backdoor(model, input_shape, num_classes):
    triggers = []
    for target_class in range(num_classes):
        trigger = optimize_trigger(model, target_class, input_shape)
        triggers.append(trigger)
    anomaly_index = compute_anomaly_index(triggers)
    return anomaly_index > 2.0
```

### STRIP 檢測

在推論階段對輸入進行擾動，觀察模型預測的一致性。被植入後門的樣本對擾動的敏感度較低。

## 防禦策略

在訓練過程中加入穩健聚合（Robust Aggregation）與差分隱私訓練，稀釋單一惡意樣本的影響力。詳見 [https://www.google.com/search?q=backdoor+detection+neural+network+2026](https://www.google.com/search?q=backdoor+detection+neural+network+2026)。
