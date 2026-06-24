# Debug PyTorch 程式碼技巧

## 1. 常見錯誤

### 設備不匹配

```python
# 錯誤示範
model = MyModel().cuda()
output = model(input)  # input 在 CPU，model 在 GPU

# 解決方法
input = input.cuda()
# 或
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
input = input.to(device)
```

### 梯度未清除

```python
# 錯誤：梯度累加
for data, target in dataloader:
    output = model(data)
    loss = criterion(output, target)
    loss.backward()  # 每次都會累加梯度
    optimizer.step()

# 正確：在每次迭代開始時清除梯度
for data, target in dataloader:
    optimizer.zero_grad()  # 清除
    output = model(data)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

### 維度錯誤

```python
# 使用 assert 檢查維度
assert input.shape == (batch_size, seq_len, features)
assert output.shape == (batch_size, num_classes)
```

## 2. Debug 工具

### 直接列印張量

```python
x = torch.randn(3, 4)
print(x)  # 直接查看張量內容
print(x.shape)  # 維度
print(x.dtype)  # 資料型別
```

### 啟用 anomaly detection

```python
torch.autograd.set_detect_anomaly(True)
```

### 使用 pytest 進行單元測試

```python
import pytest

def test_model_output_shape():
    model = MyModel()
    x = torch.randn(2, 10)
    y = model(x)
    assert y.shape == (2, 2)
```

## 3. 計算圖除錯

```python
# 檢查哪些張量需要梯度
print(x.requires_grad)  # 應為 True

# 檢查梯度
loss.backward()
print(model.weight.grad)  # 檢查權重梯度
```

## 4. 小結

PyTorch 的動態圖特性讓除錯變得直覺。多用 assert 檢查維度，確保設備一致，並善用 anomaly detection 發現問題。

---

**參考資料**
- [PyTorch Debugging Guide](https://www.google.com/search?q=PyTorch+debugging+tips+tricks)
- [Common Errors in PyTorch](https://www.google.com/search?q=PyTorch+common+errors+debugging)