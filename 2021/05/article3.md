# Article 3：Dropout 的理論解釋

## Dropout 的生物學靈感

Dropout 的靈感來自於有性繁殖：每個基因都無法依賴另一個基因，必須學會独立有用的功能。類似地，每個神經元無法依賴特定其他神經元，必須學習對群體有價值的表示。

## 數學推導

訓練時，每層以機率 p 隨機將神經元置零。推斷時，使用完整網路但權重乘以 (1-p)。可以證明這兩種做法在某些假設下是等價的：當 dropout 遮罩服從 Bernoulli 分佈時，權重縮放的期望值等於完整網路的輸出。

## 作為貝葉斯近似

Gal 和 Ghahramani (2016) 指出，Dropout 可以被視為貝葉斯神經網路的變分近似。訓練時最小化變分下界，推斷時通過權重平均近似後驗分佈。這理論框架為理解 Dropout 的泛化提供了視角。

## 變體技術

Variational Dropout 將 Bernoulli 遮罩替換為 Gaussian dropout，實現更平滑的正則化。Concrete Dropout 將離散的 dropout 放鬆為連續分佈，可在訓練過程中學習最優的 dropout 率。DropConnect 作用於權重而非激活值。

## 實務建議

1. 標準 dropout 率為 0.5，但可視任務調整
2. 視覺任務的卷積層後通常用較小的 dropout 率（如 0.2）
3. RNN 的 dropout 通常僅應用於垂直連接
4. 近年有研究指出較小的 dropout 率或許更優

## 參考資源

- Dropout as Bayesian Approximation：https://www.google.com/search?q=dropout+bayesian+approximation+paper
- Concrete Dropout：https://www.google.com/search?q=concrete+dropout+2017