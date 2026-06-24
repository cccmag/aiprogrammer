# 程式碼解說

## 概覽

`_code/distributed_training.py` 是一個純 Python + NumPy 的分散式訓練模擬程式。它不需要 GPU 或 PyTorch，可在任何有 Python 環境的機器上執行。程式透過四個類別分別模擬四種關鍵的分散式訓練技術。

## DataParallelSim

模擬資料平行中資料分割與梯度同步的過程。`scatter` 方法將資料平均分配到各 worker，`sync_gradients` 方法模擬 All-Reduce 對梯度進行平均。這對應 PyTorch DDP 中的梯度同步機制。

## ModelParallelSim

模擬按層切割的模型平行。每個 stage 包含一組權重與偏置，資料依序通過各 stage。雖然運算未真正並行，但展示了模型平行的核心概念：不同層的參數分開儲存與計算。

## GradientAccumulator

模擬梯度累積技術。當累積步數達到設定值時，返回平均梯度；否則返回 None。這是管線平行和大 batch 訓練中的關鍵技術。

## ZeROOptimizer

模擬 ZeRO Stage 1 最佳化器狀態分割。每個 worker 只負責更新自己擁有的參數。使用 Adam 更新規則，展示了參數狀態分散儲存的原理。

## 執行方式

```
cd _code
bash test.sh
```

或直接執行：

```
python3 distributed_training.py
```

[搜尋 PyTorch DDP 範例](https://www.google.com/search?q=PyTorch+DDP+example+code)
[搜尋分散式訓練程式碼](https://www.google.com/search?q=distributed+training+Python+example)
