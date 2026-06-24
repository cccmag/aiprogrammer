# Focus 7：深度學習理論的演進

## 理論的三個層次

深度學習理論可分為三個層次。最基礎的是逼近理論（Approximation Theory）：神經網路能夠逼近任意函數嗎？第二層是優化理論（Optimization Theory）：為何梯度下降能成功訓練深度網路？第三層是泛化理論（Generalization Theory）：為何訓練好的模型能泛化到新資料？

## 逼近理論的進展

經典結果是 Universal Approximation Theorem：單層感知機可以逼近任意連續函數（但需要足夠多的神經元）。這引發了疑問：為何需要深度？近期理論證明，深度網路比寬度網路有指數級的表示效率——對於某些函數，深度網路所需的神經元數量遠少於寬網路。

## 優化理論的謎題

經典優化理論預測深度網路應該很難訓練——損失函數是非凸的，充滿局部極小。但實驗表明簡單的梯度下降能達到很好的解。2021 年的研究提出了一些解釋：超引數網路的梯度下降可以逃離尖點、Sharp vs Flat Minima、彩票假說等。

## 泛化理論的困惑

傳統 VC 維度理論無法解釋深度網路的泛化能力——網路可以輕易打敗 VC 維度 bound，但仍然泛化良好。2021 年的焦點是 implicit bias（隱式偏置）：梯度下降本身是否偏愛某類解？研究發現梯度下降偏愛「簡單」的解，這在某種程度上解釋了泛化。

## 未來方向

深度學習理論落後於實踐，但正在追趕。兩個前沿方向是：第一，理解 Transformer 和 Attention 的理論特性；第二，理解大規模預訓練的理論基礎，如 GPT-3 等大模型的泛化能力從何而來。

## 參考資源

- Deep Learning Theory：https://www.google.com/search?q=deep+learning+theory+approximation
- Generalization in Deep Learning：https://www.google.com/search?q=generalization+deep+learning+theory+2021