# 自動微分計算圖

## 計算圖的基本概念

計算圖（Computation Graph）是深度學習框架實現自動微分的核心資料結構。它是一個有向無環圖（DAG），其中節點代表張量或運算，邊代表資料流向。

在 PyTorch 中，每次對 Tensor 的操作都會在背景建立計算圖的邊。當呼叫 `backward()` 時，Autograd 引擎會從輸出節點開始，沿著計算圖反向遍歷，利用鏈鎖法則計算每個節點的梯度。

## 動態計算圖的特性

PyTorch 採用動態計算圖（Define-by-Run），這意味著計算圖是在每次前向傳播時即時建立的。這種設計帶來幾個好處：

1. **控制流原生支援**：Python 的 `if`、`for` 迴圈可以直接用於網路定義
2. **容易偵錯**：可以在前向傳播中使用 pdb 中斷點
3. **動態架構**：每次前向傳播可以有不同結構

```python
def dynamic_forward(x):
    if x.sum() > 0:
        return self.net1(x)
    else:
        return self.net2(x)
```

## Autograd 的運作機制

當你對一個 `requires_grad=True` 的 Tensor 進行操作時，PyTorch 會：
1. 建立一個 `Function` 物件記錄該操作
2. 在 Tensor 的 `grad_fn` 屬性中保存該 `Function`
3. 串聯所有 `grad_fn` 形成計算圖

```python
x = torch.tensor([1.0], requires_grad=True)
y = x ** 2          # y.grad_fn = PowBackward0
z = y.mean()        # z.grad_fn = MeanBackward0
z.backward()        # 從 z 開始反向傳播
print(x.grad)       # dz/dx = 2*x / 1 = 2.0
```

## 梯度累積與清零

PyTorch 預設會累積梯度，這在 RNN 或特殊訓練策略中很有用，但一般情況下需要在每個 step 前歸零：

```python
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

## 高階梯度

Autograd 也支援高階梯度計算，透過 `create_graph=True`：

```python
x = torch.tensor([1.0], requires_grad=True)
y = x ** 3
grad = torch.autograd.grad(y, x, create_graph=True)[0]
hgrad = torch.autograd.grad(grad, x)[0]
print(hgrad)  # d^2(y)/dx^2 = 6*x = 6
```

## 參考資料

- Autograd 文件：https://pytorch.org/docs/stable/autograd.html
- 計算圖視覺化：https://pytorch.org/docs/stable/tensorboard.html
- 自訂 autograd Function：https://pytorch.org/docs/stable/notes/extending.html
