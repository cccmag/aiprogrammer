# PyTorch 核心：Tensor 與 Autograd

## Tensor：深度學習的原子單位

Tensor（張量）是 PyTorch 中最基本的資料結構，概念上類似於 NumPy 的 ndarray，但多了 GPU 加速與自動微分的能力。

```python
import torch
x = torch.randn(3, 4)
y = x.cuda() if torch.cuda.is_available() else x
```

Tensor 支援豐富的運算操作：
- **形狀操作**：`reshape`、`transpose`、`squeeze`、`unsqueeze`
- **數學運算**：`mm`（矩陣乘法）、`sin`、`exp`、`pow`
- **索引切片**：與 NumPy 相同的語法
- **廣播機制**：自動擴展維度以進行逐元素運算

## Autograd：自動微分引擎

Autograd 是 PyTorch 自動計算梯度的核心系統。當我們將一個 Tensor 的 `requires_grad` 設為 `True`，PyTorch 會自動記錄所有對這個張量的操作，建立一個計算圖。

```python
a = torch.tensor([2.0], requires_grad=True)
b = a ** 2 + 3 * a
b.backward()
print(a.grad)  # 2*a + 3 = 7
```

計算圖由 `Function` 節點組成，每個節點記錄了前向傳播的運算，並實作了反向傳播的梯度計算方法。

## 計算圖的生命週期

每次呼叫 `.backward()` 後，預設情況下計算圖會被釋放以節省記憶體。如果需要保留計算圖（例如多次反向傳播），需要在 `backward()` 中設定 `retain_graph=True`。

## 停止梯度追蹤

有三種方式可以停止 Autograd 追蹤：
1. `with torch.no_grad():` — 推理或評估時使用
2. `.detach()` — 從計算圖中分離張量
3. `.requires_grad_(False)` — 直接修改張量屬性

## 參考資料

- PyTorch Tensor 文件：https://pytorch.org/docs/stable/tensors.html
- Autograd 機制說明：https://pytorch.org/docs/stable/autograd.html
- 計算圖視覺化：https://pytorch.org/docs/stable/tensorboard.html
