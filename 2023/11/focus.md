# 主題總覽：資訊理論與編碼

資訊理論是通訊科學的基石，由 Claude Shannon 在 1948 年的經典論文《A Mathematical Theory of Communication》中開創。這門學科研究資訊的量化、儲存與傳輸，為現代數位通訊、資料壓縮與錯誤修正提供了嚴謹的數學框架。

## 核心問題

1. **資訊如何度量？** Shannon 將資訊定義為「不確定性的減少」，並提出熵（Entropy）作為資訊量的量化指標。一個事件發生的機率越低，其攜帶的資訊量就越大。這個直觀的想法後來成為整個資訊理論的出發點。

2. **資料可以壓縮到多小？** 來源編碼定理（Source Coding Theorem）給出了無失真壓縮的理論極限：任何編碼方案的位元率不能低於來源的熵。Huffman 編碼與算術編碼就是在逼近這個極限。

3. **通道可以傳輸多快？** 通道編碼定理（Channel Coding Theorem）指出，在一個有噪通道上，只要傳輸速率低於通道容量，就一定存在某種編碼方式可以實現任意低的錯誤率。這是一個存在性定理，實際的通道編碼（如漢明碼、LDPC、渦輪碼）就是在努力實踐這個理想。

4. **失真壓縮的極限在哪裡？** 率失真理論（Rate-Distortion Theory）回答了在有損壓縮場景下，給定失真容忍度時的最小傳輸速率。

## 學習路徑

建議從 focus1 到 focus7 逐步建立理論基礎，再透過 article1 到 article10 深入了解各主題的實作細節。程式碼範例集中在 `_code/info_theory.py`，涵蓋熵計算、Huffman 編碼、通道容量與漢明碼。

## 本期結構

- focus1–7：主題深入探討，從熵到率失真理論
- article1–5：壓縮編碼實戰（Huffman、算術編碼、LZW）
- article6–10：通道編碼與進階主題（BSC、漢明碼、Viterbi、LDPC）
- _code/info_theory.py：整合資訊理論示範腳本

## 參考資源

- https://www.google.com/search?q=Shannon+information+theory+1948+mathematical+theory+communication
- https://www.google.com/search?q=information+theory+source+channel+coding+theorem+tutorial
- https://www.google.com/search?q=entropy+Huffman+LDPC+channel+capacity+rate+distortion+guide
