# 模型後門檢測

## 概述

模型後門（Backdoor Attack）是攻擊者在訓練階段植入特定觸發模式，使模型在正常輸入時表現正常，但在觸發條件下產生預設惡意輸出。

## 後門攻擊類型

### 資料汙染後門

```python
def poison_dataset(dataset, trigger, target_label, poison_rate=0.01):
    n_poison = int(len(dataset) * poison_rate)
    return [
        (apply_trigger(img, trigger), target_label)
        if i < n_poison else (img, label)
        for i, (img, label) in enumerate(dataset)
    ]
```

## 檢測方法

### 神經元啟用分析

分析特定神經元對觸發模式的敏感度：

```python
def neuron_inspection(model, clean_loader, trigger):
    activations = {}
    for name, module in model.named_modules():
        hook = lambda m, i, o: activations.update({name: o})
        module.register_forward_hook(hook)

    clean_acts = []
    trigger_acts = []
    for x, _ in clean_loader:
        model(x)
        clean_acts.append(activations.copy())
        model(apply_trigger(x, trigger))
        trigger_acts.append(activations.copy())

    diff = abs(np.mean(trigger_acts) - np.mean(clean_acts))
    return diff > threshold
```

### STRIP 檢測

透過擾動輸入觀察預測一致性：

```python
def strip_detection(model, sample, num_perturbations=100):
    predictions = []
    base_pred = model(sample.unsqueeze(0))
    for _ in range(num_perturbations):
        perturbed = sample + torch.randn_like(sample) * 0.1
        pred = model(perturbed.unsqueeze(0))
        predictions.append(F.softmax(pred, dim=-1))
    entropy = -torch.stack(predictions).mean(0) * \
              torch.log(torch.stack(predictions).mean(0) + 1e-10)
    return entropy.sum().item()
```

### 頻譜分析

在頻域中檢測異常模式：

```python
import torch.fft as fft

def spectral_backdoor_detect(model, sample):
    """利用傅立葉變換分析後門觸發頻率"""
    pred = model(sample.unsqueeze(0))
    spectrum = fft.fft2(pred)
    magnitude = torch.abs(spectrum)
    high_freq_ratio = (magnitude > magnitude.mean()).float().mean()
    return high_freq_ratio > 0.3
```

## 持續監控

```python
class BackdoorMonitor:
    def __init__(self, model, threshold=0.8):
        self.model = model
        self.threshold = threshold
        self.baseline_distribution = None

    def evaluate(self, eval_loader):
        scores = [strip_detection(self.model, x)
                  for x, _ in eval_loader]
        return {"mean": np.mean(scores),
                "anomaly": np.mean(scores) > self.threshold}
```

參考資料：https://www.google.com/search?q=model+backdoor+detection+techniques+2026
