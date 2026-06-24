# 程式碼說明 — 資訊理論示範腳本

## 功能概述

`_code/info_theory.py` 是一個單一檔案的全方位資訊理論示範腳本，使用 Python 標準函式庫即可執行。腳本涵蓋四個核心主題：熵計算、Huffman 編碼、通道容量分析與漢明碼編解碼。

## demo() 函數說明

`demo()` 函數依序執行以下四個展示項目：

### 1. 熵的計算
展示如何從機率分布計算 Shannon 熵，以及每個符號的自資訊。使用範例機率分布 [0.5, 0.25, 0.125, 0.125] 來說明：當符號發生機率越低，其自資訊量越大。

```python
>>> entropy([0.5, 0.25, 0.125, 0.125])
1.75
```

### 2. Huffman 編碼
對字串 "ABBCCCDDDDEEEEE" 建立 Huffman 編碼樹，輸出編碼表與壓縮後的位元串，並計算壓縮比。當字元頻率不均勻時，Huffman 編碼可以顯著降低平均編碼長度。

### 3. BSC 通道容量
計算二元對稱通道在不同錯誤率下的通道容量。當錯誤率 p=0 時容量為 1（完美通道），p=0.5 時容量為 0（純隨機通道）。展示 Shannon 通道編碼定理的核心概念。

### 4. 漢明碼 (7,4) 編解碼
展示漢明碼的編碼、錯誤注入與糾錯解碼的完整流程。將 4 個資料位元編碼為 7 個位元，在第 4 位注入錯誤後，解碼器能自動偵測並修正該錯誤。

## 執行方式

```bash
cd _code
python3 info_theory.py
```

或使用測試腳本：

```bash
cd _code
bash test.sh
```

## 輸出範例

```
[1] 熵的計算
  機率分布: [0.5, 0.25, 0.125, 0.125]
  熵 H = 1.7500 bits

[2] Huffman 編碼
  編碼表: {'C': '01', 'D': '10', 'E': '11', 'A': '000', 'B': '001'}
  壓縮比: 27.50%

[3] BSC 通道容量
  錯誤率 p=0.10, 容量 C=0.5310 bits/use

[4] 漢明碼 (7,4)
  原始: [1, 0, 1, 1] → 糾錯後: [1, 0, 1, 1] 正確
```

## 參考資源

- https://www.google.com/search?q=Python+entropy+calculation+Shannon+information+theory+script
- https://www.google.com/search?q=Python+Huffman+coding+implementation+heapq+priority+queue
- https://www.google.com/search?q=Python+channel+capacity+BSC+binary+symmetric+channel+computation
- https://www.google.com/search?q=Python+Hamming+code+7+4+encode+decode+error+correction+implementation
