# 隱私與邊緣推論

## 1. 邊緣推論的隱私優勢

傳統雲端 AI 需上傳資料至伺服器，存在隱私風險。邊緣推論將資料處理留在本機，從根本上解決問題。

## 2. 差分隱私

在訓練階段加入雜訊，防止攻擊者從參數推斷出單筆資料：

```python
import numpy as np

def add_dp_noise(gradients, epsilon=1.0, sensitivity=1.0):
    noise_scale = sensitivity / epsilon
    noisy = []
    for grad in gradients:
        noise = np.random.laplace(0, noise_scale, size=grad.shape)
        noisy.append(grad + noise)
    return noisy

grads = [np.array([0.5, -0.3, 0.8])]
private = add_dp_noise(grads, epsilon=0.5)
print(f'原始: {grads[0]}\n加噪: {private[0]}')
```

## 3. 聯邦學習

模型在使用者端訓練，只回傳梯度更新而非原始資料：

```python
import numpy as np

class FederatedClient:
    def __init__(self, client_id, data, labels):
        self.client_id = client_id
        self.data = data
        self.labels = labels

    def local_train(self, global_weights, epochs=1):
        """在本地訓練，只回傳權重更新"""
        local_w = global_weights.copy()
        for _ in range(epochs):
            idx = np.random.randint(len(self.data))
            pred = local_w @ self.data[idx]
            grad = (pred - self.labels[idx]) * self.data[idx]
            local_w -= 0.01 * grad
        return local_w - global_weights

client = FederatedClient('d001', np.random.randn(10, 64), np.random.randint(0, 10, 10))
update = client.local_train(np.zeros(64))
print(f'回傳 {len(update)} 個參數（原始資料未離開裝置）')
```

## 4. 結語

邊緣推論是 AI 隱私保護的最佳路徑。更多資訊請參考 https://www.google.com/search?q=on-device+AI+privacy+federated+learning
