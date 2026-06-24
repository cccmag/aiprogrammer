# PyTorch 張量運算

## 張量基礎

張量是 PyTorch 的核心資料結構，可視為多維陣列：

```python
import torch

# 創建張量
a = torch.tensor([1, 2, 3])           # 1D
b = torch.randn(3, 4)                  # 2D, 常態分佈
c = torch.zeros(2, 3, 4)              # 3D, 全零
d = torch.ones(2, 3, 4)               # 3D, 全一
```

## 常見運算

```python
# 算數運算
c = a + b
c = torch.add(a, b)

# 矩陣乘法
result = torch.matmul(matrix1, matrix2)

# 逐元素運算
result = torch.relu(x)
result = torch.softmax(x, dim=1)
```

## 形狀變換

```python
#  reshape
x = torch.randn(4, 16)
y = x.view(8, 8)      # 改變形狀
z = x.flatten()        # 展平

#  transpose
t = x.transpose(0, 1) # 交換維度
```

## 設備轉換

```python
# CPU to GPU
x_gpu = x.to('cuda')

#  Half precision
x_half = x.half()

# 與 NumPy 轉換
np_array = x.numpy()
x_back = torch.from_numpy(np_array)
```

---

## 延伸閱讀

- [PyTorch Tensor 官方文檔](https://www.google.com/search?q=PyTorch+Tensor+documentation)
- [張量運算詳解](https://www.google.com/search?q=torch+tensor+operations+tutorial)
- [GPU+加速PyTorch](https://www.google.com/search?q=PyTorch+GPU+acceleration)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*