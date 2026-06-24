# 模型儲存與載入

## 為什麼需要模型序列化？

訓練一個深度學習模型可能需要數小時到數週。模型的儲存與載入機制讓我們可以：
- 中斷後繼續訓練
- 部署訓練好的模型到生產環境
- 分享模型給其他研究者和開發者

## 狀態字典（state_dict）

每個 `nn.Module` 的 `state_dict` 是一個 Python 字典，將每層的參數名稱映射到對應的 Tensor。這是 PyTorch 推薦的儲存方式。

```python
# 儲存
torch.save(model.state_dict(), 'model.pth')

# 載入
model = MyModel()
model.load_state_dict(torch.load('model.pth'))
```

## 完整 checkpoint

除了模型參數外，訓練過程中還需要儲存最佳化器狀態、epoch 編號和 loss 記錄：

```python
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}
torch.save(checkpoint, 'checkpoint.pth')
```

## 載入 checkpoint 並恢復訓練

```python
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
start_epoch = checkpoint['epoch'] + 1
```

## 裝置對應

在不同裝置之間遷移模型時需要特別注意：
- 在 GPU 上訓練、GPU 上載入：直接載入
- 在 CPU 上訓練、CPU 上載入：直接載入
- GPU → CPU：`torch.load('model.pth', map_location='cpu')`
- CPU → GPU：先載入再到 GPU，確保 `map_location` 設定正確

## TorchScript 與序列化

PyTorch 的 TorchScript 提供了跨語言部署的能力：

```python
scripted_model = torch.jit.script(model)
scripted_model.save('model.pt')
```

TorchScript 模型可以在 C++ 環境中執行，不依賴 Python 執行環境。

## 參考資料

- 模型儲存載入教學：https://pytorch.org/tutorials/beginner/saving_loading_models.html
- TorchScript：https://pytorch.org/docs/stable/jit.html
- ONNX 匯出：https://pytorch.org/docs/stable/onnx.html
