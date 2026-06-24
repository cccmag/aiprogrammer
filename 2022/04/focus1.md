# 深度學習框架演進：Theano → TensorFlow → PyTorch

## 框架的黎明：Theano

2007 年，蒙特婁大學的 MILA 實驗室釋出了 Theano，這是第一個專門為深度學習設計的 Python 框架。Theano 引入了計算圖（Computation Graph）的概念，讓使用者可以用符號式的方式定義數學運算，再由框架自動產生最佳化的 GPU 程式碼。

Theano 的核心貢獻在於：
- 符號式計算圖與自動微分
- GPU 加速支援
- 運算最佳化與穩定性檢查

然而，Theano 的低階 API 使得模型建構相當繁瑣，且偵錯困難，這為後續框架的誕生埋下了伏筆。

## TensorFlow 的崛起

2015 年，Google Brain 團隊釋出了 TensorFlow，迅速成為深度學習領域的主流框架。TensorFlow 帶來了更強大的生態系統，包括 TensorBoard 視覺化工具、TensorFlow Serving 部署方案、以及後來的手機端解決方案 TensorFlow Lite。

TensorFlow 採用靜態計算圖（Static Graph），使用者先建構圖再執行。這種設計雖然有利於效能最佳化，卻也導致了偵錯不便——你無法在圖建構時用 Python 的 pdb 進行中斷點除錯。

## PyTorch 的逆襲

2016 年，Facebook AI Research 推出了 PyTorch，其動態計算圖（Dynamic Graph / Define-by-Run）徹底改變了框架設計的思維。在 PyTorch 中，計算圖是在執行過程中即時建立的，這讓 Python 原生的控制流（if、for）可以直接用於神經網路建構。

PyTorch 的優勢：
- 動態計算圖，直覺且易於偵錯
- Pythonic API，學習曲線平緩
- 豐富的社群生態（Hugging Face、Lightning）

## 框架之爭的終局？

截至 2022 年，PyTorch 在學術界已取得壓倒性優勢，大多數頂尖會議的論文都使用 PyTorch 實作。TensorFlow 2.x 雖然引入了 Eager Execution（動態執行），但先機已失。

JAX 作為新興框架，在高效能計算領域展現潛力，但生態系統仍遠不及 PyTorch。

## 參考資料

- Theano 官方文件：https://github.com/Theano/Theano
- TensorFlow 官方網站：https://www.tensorflow.org/
- PyTorch 官方網站：https://pytorch.org/
- JAX 官方文件：https://jax.readthedocs.io/
