# 訓練監控與調試

## 前言

訓練深度學習模型是一個複雜的過程，容易遇到各種問題。本篇文章將介紹如何監控訓練過程、診斷問題並進行調試。

## 訓練監控基礎

### 記錄關鍵指標

```python
import json
from datetime import datetime

class TrainingMonitor:
    def __init__(self):
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'train_acc': [],
            'val_acc': [],
            'learning_rate': [],
            'epoch_time': []
        }

    def log(self, metrics):
        for key, value in metrics.items():
            if key in self.history:
                self.history[key].append(value)

    def save(self, filename='training_history.json'):
        with open(filename, 'w') as f:
            json.dump(self.history, f)

    def plot(self):
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # Loss
        axes[0, 0].plot(self.history['train_loss'], label='Train')
        axes[0, 0].plot(self.history['val_loss'], label='Val')
        axes[0, 0].set_title('Loss')
        axes[0, 0].legend()

        # Accuracy
        axes[0, 1].plot(self.history['train_acc'], label='Train')
        axes[0, 1].plot(self.history['val_acc'], label='Val')
        axes[0, 1].set_title('Accuracy')
        axes[0, 1].legend()

        # Learning Rate
        axes[1, 0].plot(self.history['learning_rate'])
        axes[1, 0].set_title('Learning Rate')

        # Epoch Time
        axes[1, 1].plot(self.history['epoch_time'])
        axes[1, 1].set_title('Epoch Time')

        plt.tight_layout()
        plt.savefig('training_history.png')
```

## 常見問題診斷

### 1. Loss 不下降

```python
def diagnose_loss_not_decreasing(history):
    """診斷 loss 不下降的問題"""
    recent_losses = history['val_loss'][-10:]

    if all(recent_losses[i] >= recent_losses[i-1] for i in range(1, len(recent_losses))):
        print("Loss 持續上升或持平，可能的原因：")
        print("1. 學習率太高 → 降低學習率")
        print("2. 梯度爆炸 → 檢查梯度裁剪")
        print("3. 模型架構問題 → 檢查網路結構")
        print("4. 資料標籤錯誤 → 檢查資料")

    if len(recent_losses) > 0 and recent_losses[-1] > recent_losses[0]:
        print("Loss 先下降後上升：")
        print("1. 過擬合 → 增加正則化")
        print("2. 資料不平衡 → 檢查類別分佈")
```

### 2. 梯度問題

```python
def check_gradients(model):
    """檢查梯度是否正常"""
    total_norm = 0.0
    param_norms = {}

    for name, param in model.named_parameters():
        if param.grad is not None:
            param_norm = param.grad.data.norm(2).item()
            param_norms[name] = param_norm
            total_norm += param_norm ** 2

    total_norm = total_norm ** 0.5

    print(f"Total gradient norm: {total_norm:.4f}")

    if total_norm > 10:
        print("警告：梯度範圍過大，可能需要梯度裁剪")
    elif total_norm < 1e-5:
        print("警告：梯度範圍過小，可能需要檢查學習率")

    # 顯示最大的梯度
    sorted_norms = sorted(param_norms.items(), key=lambda x: x[1], reverse=True)
    print("\n梯度最大的層：")
    for name, norm in sorted_norms[:5]:
        print(f"  {name}: {norm:.6f}")
```

### 3. 梯度裁剪

```python
# 梯度裁剪，防止梯度爆炸
torch.nn.utils.clip_grad_norm_(
    model.parameters(),
    max_norm=1.0,  # 最大梯度範數
    norm_type=2    # L2 範數
)

# 或者裁剪特定範圍
torch.nn.utils.clip_grad_value_(
    model.parameters(),
    clip_value=1.0  # 裁剪到 [-1, 1]
)
```

## TensorBoard 整合

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')

for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        # 訓練步驟
        output = model(data)
        loss = criterion(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 記錄 scalar
        writer.add_scalar('Loss/train', loss.item(), global_step)
        writer.add_scalar('Learning_Rate',
                         optimizer.param_groups[0]['lr'],
                         global_step)

        # 記錄圖片
        if batch_idx % 100 == 0:
            writer.add_images('Input_Images', data[:8], global_step)

        # 記錄 histogram
        for name, param in model.named_parameters():
            writer.add_histogram(f'Params/{name}', param, global_step)
```

## 資料流追蹤

```python
def debug_dataflow(model, sample_batch):
    """追蹤資料流動"""
    x, y = sample_batch
    print(f"Input shape: {x.shape}, Label shape: {y.shape}")

    hooks = []

    def hook_fn(module, input, output):
        print(f"{module.__class__.__name__:20s} | "
              f"Input: {input[0].shape if isinstance(input, tuple) else input.shape} | "
              f"Output: {output.shape}")

    # 註冊鉤子
    for name, module in model.named_modules():
        if len(list(module.children())) == 0:  # 只有葉子節點
            hooks.append(module.register_forward_hook(hook_fn))

    # 前向傳播
    output = model(x)

    # 移除鉤子
    for hook in hooks:
        hook.remove()

    print(f"\nOutput: {output.shape}")
    return output
```

## 記憶體監控

```python
def print_memory_usage():
    """打印記憶體使用情況"""
    if torch.cuda.is_available():
        print(f"GPU Memory Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
        print(f"GPU Memory Cached: {torch.cuda.memory_cached() / 1e9:.2f} GB")

def clear_cache():
    """清理快取"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
```

## 實驗管理

```python
class ExperimentManager:
    def __init__(self, base_dir='experiments'):
        self.base_dir = base_dir
        self.experiments = {}

    def create_experiment(self, name, config):
        exp_dir = os.path.join(self.base_dir, name)
        os.makedirs(exp_dir, exist_ok=True)

        self.experiments[name] = {
            'config': config,
            'dir': exp_dir,
            'results': None
        }

        # 保存配置
        with open(os.path.join(exp_dir, 'config.json'), 'w') as f:
            json.dump(config, f, indent=2)

    def log_results(self, name, results):
        self.experiments[name]['results'] = results

        exp_dir = self.experiments[name]['dir']
        with open(os.path.join(exp_dir, 'results.json'), 'w') as f:
            json.dump(results, f, indent=2)

    def compare_experiments(self, metric='val_acc'):
        print("Experiment Comparison:")
        print("-" * 50)
        for name, exp in self.experiments.items():
            if exp['results'] and metric in exp['results']:
                value = exp['results'][metric]
                print(f"{name:30s}: {value:.4f}")
```

## 總結

訓練監控和調試的最佳實踐：

1. **記錄所有指標**：loss、accuracy、learning rate 等
2. **視覺化訓練過程**：使用 TensorBoard 或 matplotlib
3. **檢查梯度**：確保梯度在合理範圍
4. **監控記憶體**：特別是 GPU 記憶體
5. **保存檢查點**：方便恢復和重現

---

**延伸閱讀**

- [CS231n Debugging Tips](https://www.google.com/search?q=CS231n+debugging+tips)
- [TensorBoard Tutorial](https://www.google.com/search?q=tensorboard+pytorch+tutorial)
- [Neural Network Debugging](https://www.google.com/search?q=debugging+neural+networks)