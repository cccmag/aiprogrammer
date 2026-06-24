# TensorBoard 視覺化

## 為什麼需要視覺化？

訓練深度學習模型時，僅靠終端機輸出的數字難以全面掌握訓練狀態。TensorBoard 提供了豐富的視覺化工具，幫助開發者監控訓練過程、偵錯模型、以及比較不同實驗。

## 啟用 TensorBoard

PyTorch 透過 `torch.utils.tensorboard` 整合 TensorBoard：

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')
```

啟動 TensorBoard 服務：
```bash
tensorboard --logdir=runs --port=6006
```

## 記錄訓練指標

### 標量（Scalar）
最常用的記錄方式：

```python
for epoch in range(num_epochs):
    train_loss = train_one_epoch()
    val_loss = validate()
    writer.add_scalar('Loss/train', train_loss, epoch)
    writer.add_scalar('Loss/val', val_loss, epoch)
    writer.add_scalar('LR', lr, epoch)
```

### 影像（Image）
檢視模型輸入或特徵圖：

```python
writer.add_images('input_batch', images, epoch)
writer.add_image('prediction', pred_map, epoch)
```

### 直方圖（Histogram）
觀察權重和梯度的分佈：

```python
for name, param in model.named_parameters():
    writer.add_histogram(f'weights/{name}', param, epoch)
    if param.grad is not None:
        writer.add_histogram(f'grads/{name}', param.grad, epoch)
```

### 計算圖（Graph）

```python
dummy_input = torch.randn(1, 3, 224, 224)
writer.add_graph(model, dummy_input)
```

## 超參數比較

使用 `add_hparams` 可以在 TensorBoard 中進行實驗對比：

```python
writer.add_hparams(
    {'lr': 0.001, 'batch_size': 32},
    {'hparam/val_loss': val_loss}
)
```

## 模型分析

TensorBoard 的投影儀（Projector）可以用於視覺化嵌入向量：

```python
writer.add_embedding(features, metadata=labels, label_img=images)
```

## 實戰技巧

1. 使用有意義的 runs 名稱（包含超參數資訊）
2. 定期清除舊的 runs 資料
3. 搭配 `flush_secs` 參數控制寫入頻率
4. 使用 `walltime` 參數同步不同機器的時間戳

## 參考資料

- TensorBoard 文件：https://www.tensorflow.org/tensorboard
- PyTorch TensorBoard 整合：https://pytorch.org/docs/stable/tensorboard.html
- Visdom 替代方案：https://github.com/fossasia/visdom
- Wandb 雲端方案：https://wandb.ai/
