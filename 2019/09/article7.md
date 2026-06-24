# PyTorch 1.3：量化與張量

## 前言

PyTorch 1.3 於 2019 年 10 月發布，帶來了量化支持、增強的張量處理以及更好的行動裝置部署能力。

## 量化支持

### 8 位元量化

```python
import torch

# 量化模型以減少記憶體和加速
model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)
```

---

## 新功能

### 張量處理

```python
# 新的張量操作
x = torch.tensor([1.0, 2.0, 3.0])

# 類似 NumPy 的操作
x.clip(1, 2)  # 剪切值
x.round()    # 四捨五入
```

---

## 結語

PyTorch 1.3 的量化支持和行動裝置優化使其在邊緣運算場景更有競爭力。

---

**延伸閱讀**

- [PyTorch 1.3 Release](https://www.google.com/search?q=PyTorch+1.3+release+notes)