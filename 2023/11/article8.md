# 捲積碼與 Viterbi 解碼

## 狀態機編碼

區塊碼（如漢明碼）將資料分成固定大小的區塊，每個區塊獨立編碼。捲積碼（Convolutional Code）則不同：它使用滑動視窗的方式，讓編碼具有記憶效應，當前的輸出不僅取決於當前的輸入，還取決於前幾個輸入位元。

## 編碼器結構

一個典型的 (2,1,2) 捲積碼編碼器包含一個 2 級移位暫存器，每個輸入位元產生 2 個輸出位元：

```
輸入 → [D0] → [D1]
        ↓      ↓
        ⊕ ←────┘ → 輸出 1
        ↓
        ⊕ → 輸出 2
```

編碼器的狀態由暫存器內容決定（共 $2^k$ 種狀態，$k$ 為約束長度）。

## Viterbi 演算法

Viterbi 演算法由 Andrew Viterbi 在 1967 年提出，它使用動態規劃在網格圖（Trellis）上尋找最可能的路徑，即最大似然序列解碼（MLSD）。

### 演算法步驟

1. **初始化**：從狀態 0 開始，設定累積路徑成本為 0
2. **遞迴**：對每個時間步：
   a. 計算每個狀態轉移的分支成本（接收位元與預期位元的漢明距離）
   b. 對每個目標狀態，從所有進入路徑中選擇累積成本最小的
   c. 儲存倖存路徑
3. **回溯**：從最終狀態沿倖存路徑回溯，得到解碼結果

## Python 實作（簡化版）

```python
def viterbi_decode(received, next_state, output, memory):
    n_states = 1 << (len(received) // 2)
    path_cost = {s: float('inf') for s in range(n_states)}
    path_cost[0] = 0
    survivor = {s: [] for s in range(n_states)}

    for t in range(0, len(received), 2):
        inp = received[t:t+2]
        new_cost = {s: float('inf') for s in range(n_states)}
        new_survivor = {s: [] for s in range(n_states)}
        for s in range(n_states):
            for bit in [0, 1]:
                ns, out = next_state[s][bit], output[s][bit]
                cost = path_cost[s] + sum(a ^ b for a, b in zip(inp, out))
                if cost < new_cost[ns]:
                    new_cost[ns] = cost
                    new_survivor[ns] = survivor[s] + [bit]
        path_cost, survivor = new_cost, new_survivor

    best_state = min(path_cost, key=path_cost.get)
    return survivor[best_state]
```

## 應用

Viterbi 解碼廣泛應用於：
- 數位通訊（GSM、LTE、Wi-Fi）
- 衛星通訊
- 語音辨識（HMM 解碼）
- 磁碟儲存系統的讀取通道

## 參考資源

- https://www.google.com/search?q=convolutional+code+encoder+shift+register+state+trellis+diagram+structure
- https://www.google.com/search?q=Viterbi+algorithm+maximum+likelihood+sequence+decoding+dynamic+programming+trellis
- https://www.google.com/search?q=Viterbi+decoding+Python+implementation+convolutional+code+example+tutorial
