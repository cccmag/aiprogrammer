# 動態計算圖 vs 靜態計算圖

## 計算圖的兩種模式

### 什麼是計算圖？

計算圖（Computational Graph）是表達運算之間依賴關係的圖結構。節點是運算，邊是資料流向。

```
a → [+] → c
b ↗     ↓
      [×] → d
```

### 靜態計算圖（TensorFlow 1.x）

```python
# TensorFlow 1.x：先定義後執行
import tensorflow as tf

# 定義圖
a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
c = a + b
d = c * a

# 執行圖
with tf.Session() as sess:
    result = sess.run(d, feed_dict={a: 2.0, b: 3.0})
    print(result)  # 10.0
```

**特點**：
- 先建立計算圖，再執行
- 圖結構靜態不变
- 需要 Session 來執行
- 可進行圖最佳化（XLA、JIT）

### 動態計算圖（PyTorch）

```python
# PyTorch：即時執行
import torch

a = torch.tensor(2.0, requires_grad=True)
b = torch.tensor(3.0, requires_grad=True)

c = a + b
d = c * a

print(d)  # tensor(10., grad_fn=<MulBackward>)
d.backward()
print(a.grad)  # tensor(7.)  # 2*(2+3) 對 a 的導數
```

**特點**：
- 運算立即執行並返回結果
- 圖結構動態變化
- 直接 Python 互動
- 直覺的除錯體驗

### 動態圖的優勢

```python
# 動態圖可以輕鬆實現條件分支
def dynamic_net(x, condition):
    if condition:
        return x * 2
    else:
        return x / 2

# 每次呼叫可以有不同的結構
result1 = dynamic_net(inp, True)
result2 = dynamic_net(inp, False)
```

靜態圖要做到相同的行為需要更多設定。

### 迴圈處理的差異

```python
# PyTorch：使用標準 Python 迴圈
def rnn_loop(input_seq, hidden_dim):
    hidden = torch.zeros(1, hidden_dim)
    for step in input_seq:
        # 每個時間步可以有不同的計算
        hidden = torch.tanh(torch.mm(step, Wxh) + torch.mm(hidden, Whh))
    return hidden

# TensorFlow 1.x 需要 tf.while_loop 或展開
```

### 兩者比較

| 面向 | 動態圖（PyTorch） | 靜態圖（TensorFlow） |
|------|-------------------|----------------------|
| 執行速度 | 稍微慢（但 JIT 追平） | 稍快（圖優化） |
| 除錯體驗 | 直覺，可直接列印 | 需要 Session |
| 程式碼複雜度 | 低 | 中 |
| 部署友善度 | 中（TorchScript 改善中） | 高（SavedModel） |
| 研究靈活性 | 高 | 中 |

### 小結

動態計算圖是 PyTorch 的核心優勢，特別適合研究用途。TensorFlow 2.0（Eager Execution 預設）也借鑒了這個設計。

---

**下一步**：[torch.autograd 自動微分詳解](focus3.md)