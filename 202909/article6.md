# 科學模擬與 AI

## 加速物理模擬

傳統科學模擬（如流體力學、量子化學）計算成本極高。AI 代理模型（surrogate model）能以極低計算成本逼近高保真模擬結果，有潛力實現即時預測。

## 物理資訊神經網路（PINN）

PINN 將物理定律（偏微分方程）直接嵌入神經網路的損失函數，使模型在無標註數據的情況下學習滿足物理約束的解。這對流體模擬、固體力學、熱傳導等問題特別有效。

```python
# 簡化 PINN：求解一維熱傳導方程
import numpy as np

class SimplePINN:
    def __init__(self, alpha=0.01):
        self.alpha = alpha  # 熱擴散係數
        self.w = np.random.randn(10) * 0.1
        self.b = np.random.randn(10) * 0.1
    
    def forward(self, x, t):
        h = np.tanh(x * self.w + t * self.b[:len(self.w)])
        return np.sum(h)
    
    def physics_loss(self, x, t):
        # 殘差: u_t - alpha * u_xx = 0
        h = np.tanh(x * self.w + t * self.b[:len(self.w)])
        u_t = np.sum(h * (1 - h**2) * self.b[:len(self.w)])
        u_x = np.sum(h * (1 - h**2) * self.w)
        u_xx = np.sum((1 - h**2) * self.w**2 - 2 * h * (1 - h**2) * self.w**2)
        return u_t - self.alpha * u_xx

pinn = SimplePINN()
x, t = 0.5, 0.1
u = pinn.forward(x, t)
residual = pinn.physics_loss(x, t)
print(f"u({x}, {t}) = {u:.4f}")
print(f"物理殘差 = {residual:.6f}")
```

## 分子動力學加速

傳統分子動力學模擬的時間步長限制在飛秒級。AI 增強方法如深度學習勢能（DeepMD、NequIP）和粗粒化模型，可將模擬時間尺度擴展到微秒甚至毫秒級。

## 應用案例

DeepMind 的 GraphCast 以 AI 天氣預報模型超越傳統數值預報；DeepZ 結合深度學習與密度泛函理論加速電子結構計算。AI 模擬不是取代傳統方法，而是與之互補，實現多尺度建模。

> 參考資料：https://www.google.com/search?q=AI+scientific+simulation+physics+informed+neural+network
