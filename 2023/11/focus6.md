# 6. 渦輪碼與 LDPC

## 逼近 Shannon 極限

從 1950 到 1990 年代，通道編碼技術在效率上一直與 Shannon 極限有相當的差距。漢明碼的編碼率雖然實用，但遠未達到通道容量。這種情況在 1990 年代出現了兩次革命性的突破。

## 渦輪碼（Turbo Codes）

1993 年，Berrou、Glavieux 與 Thitimajshima 提出了渦輪碼，首次在實務上逼近了 Shannon 極限（距離僅 0.5 dB）。

渦輪碼的核心思想：
1. **兩個遞迴系統迴旋碼（RSC）並聯**
2. **交錯器**將資料順序打亂後送給第二個編碼器
3. **迭代解碼**：兩個解碼器交換軟資訊（LLR），每次迭代提升可信度

這個「渦輪」效應——兩個解碼器互相增強——正是其名稱的由來。每次迭代都像渦輪增壓一樣提升解碼效能。

## LDPC 碼（低密度奇偶檢查碼）

LDPC 碼由 Robert Gallager 在 1960 年提出，但因當時的計算能力不足而被遺忘。到 1990 年代末被 MacKay 與 Neal 重新發現後，成為另一個逼近 Shannon 極限的編碼方案。

LDPC 碼的核心：
1. **稀疏同位檢查矩陣** $\mathbf{H}$：大部分元素為 0，只有少數為 1
2. **Tanner 圖**：將碼描述為變數節點與檢查節點的二部圖
3. **信念傳播（BP）解碼**：節點之間透過邊傳遞軟資訊，迭代收斂

## 現況與應用

- LDPC 被 5G NR、Wi-Fi 6/7、DVB-S2 等標準採用作為資料通道編碼
- 渦輪碼用於 3G/4G 行動通訊（UMTS、LTE）
- 兩者都在實務中達到了距 Shannon 極限 0.1–0.5 dB 的效能

## 參考資源

- https://www.google.com/search?q=Turbo+code+Berrou+Glavieux+iterative+decoding+Shannon+limit+1993
- https://www.google.com/search?q=LDPC+low+density+parity+check+code+Gallager+MacKay+belief+propagation
- https://www.google.com/search?q=Turbo+vs+LDPC+comparison+5G+WiFi+channel+coding+standard
