# AI for Science 導論（2018-2029）

## 從科學計算到科學 AI

傳統科學計算仰賴數值方法：有限元素分析、分子動力學模擬、蒙地卡羅方法。2018 年之後，深度學習開始從根本上改變這個範式。

```
傳統範式：物理定律 → 數學模型 → 數值求解
AI 範式：實驗數據 → 深度學習 → 預測模型
混合範式：物理定律 + 數據 → 物理資訊神經網路 → 精準求解
```

## 關鍵里程碑

**2018** — Google 的 AlphaFold 在 CASP13 競賽中首次展現深度學習在蛋白質結構預測上的威力。同年，Graph Neural Networks 開始在分子性質預測中取得突破。

**2020** — DeepMind 的 AlphaFold2 在 CASP14 上震驚世界，預測精度接近實驗水準。MIT 的《Scientific Machine Learning》課程開設，標誌著這個領域正式進入學術主流。

**2021** — Physics-Informed Neural Networks (PINNs) 成為熱點，直接將 PDE 作為損失函數的一部分：

```python
import torch

def pinn_loss(model, x, t, nu=0.01):
    u = model(x, t)
    u_t = torch.autograd.grad(u, t, grad_outputs=torch.ones_like(u), create_graph=True)[0]
    u_x = torch.autograd.grad(u, x, grad_outputs=torch.ones_like(u), create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, grad_outputs=torch.ones_like(u), create_graph=True)[0]
    # Burgers 方程殘差: u_t + u*u_x - nu*u_xx = 0
    residual = u_t + u * u_x - nu * u_xx
    return torch.mean(residual ** 2)
```

**2024-2026** — 大型科學模型崛起：Google 的 GraphCast 在氣象預報上超越傳統數值模式；NVIDIA 的 FourCastNet 實現全球天氣的秒級預測。

**2027-2029** — 基礎模型（Foundation Models）進駐科學領域，單一模型可同時處理分子、材料、蛋白質等不同科學數據。

## 核心方法論

AI for Science 的核心方法可以歸納為三類：

1. **代理模型（Surrogate Model）**：用神經網路近似昂貴的數值模擬器
2. **逆問題求解（Inverse Design）**：從目標性質反向搜尋最優結構
3. **科學假說生成（Hypothesis Generation）**：AI 自動發現數據中的隱藏模式

## 參考資源

- [Scientific Machine Learning 課程（MIT）](https://www.google.com/search?q=MIT+Scientific+Machine+Learning+course)
- [Physics-Informed Neural Networks](https://www.google.com/search?q=Physics+Informed+Neural+Networks+PINNs)
- [GraphCast 氣象模型](https://www.google.com/search?q=Google+GraphCast+weather+prediction)
