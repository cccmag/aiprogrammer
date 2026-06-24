# SHA 系列雜湊函數

## 雜湊函數的演進

雜湊函數的歷史始於 1979 年 Ralph Merkle 和 Ivan Damgård 獨立提出的 Merkle-Damgård 構造。這個構造將任意長度的輸入轉換為固定長度的輸出，是許多經典雜湊函數的基礎。

## Merkle-Damgård 構造

Merkle-Damgård 構造的核心思想是迭代壓縮：

1. 將輸入訊息分割為固定大小的區塊
2. 若最後一個區塊不足，進行填充（Padding）
3. 從初始向量 IV 開始，逐區塊應用壓縮函數
4. 最終輸出為雜湊值

這種構造的安全性依賴於壓縮函數的抗碰撞性：如果壓縮函數是抗碰撞的，那麼整個雜湊函數也是抗碰撞的。

## MD4 與 MD5

MD4 由 Ron Rivest 於 1990 年設計，是 MD 系列的開端。它速度快，但很快就出現了安全漏洞。

MD5（1991 年）是 MD4 的強化版本，增加了第四輪計算並改進了非線性函數。然而，2004 年王小雲團隊提出了高效的 MD5 碰撞攻擊，從此 MD5 被視為不安全。

## SHA-0 與 SHA-1

SHA-0（1993 年）由 NIST 發布，但在發布後不久就發現了未公開的缺陷。NIST 隨後發布了修正版本 SHA-1（1995 年）。

SHA-1 產生 160 位元輸出，使用 80 輪計算。它的設計借鑒了 MD4，但加入了擴展的訊息排程和更複雜的輪函數。

2017 年的 SHAttered 攻擊是 SHA-1 的轉折點。Google 和 CWI 團隊展示了如何生成兩個具有相同 SHA-1 雜湊值的不同 PDF 檔案。這次攻擊耗費了 9×10^18 次 SHA-1 計算——大約 6500 CPU 年——但只花費了約 11 萬美元的雲端計算費用。

## SHA-2 的內部結構

SHA-256 的壓縮函數包含 64 輪（SHA-512 為 80 輪）。每輪使用 6 個邏輯函數：

```
Ch(x, y, z) = (x & y) ^ (~x & z)
Maj(x, y, z) = (x & y) ^ (x & z) ^ (y & z)
∑0(x) = ROTR²(x) ^ ROTR¹³(x) ^ ROTR²²(x)
∑1(x) = ROTR⁶(x) ^ ROTR¹¹(x) ^ ROTR²⁵(x)
σ0(x) = ROTR⁷(x) ^ ROTR¹⁸(x) ^ SHR³(x)
σ1(x) = ROTR¹⁷(x) ^ ROTR¹⁹(x) ^ SHR¹⁰(x)
```

SHA-256 使用 64 個不同的常數 K₀ - K₆₃，這些常數是前 64 個質數立方根的小數部分的前 32 位元。

## SHA-3 與海綿結構

SHA-3（Keccak）採用與 SHA-2 完全不同的設計——海綿結構（Sponge Construction）。海綿結構包含：

- **狀態**：b 位元的內部狀態，分為 c（容量）和 r（位元率）兩部分
- **置換函數**：對狀態進行疊代置換

SHA-3 的置換函數 Keccak-f[b] 包含多輪，每輪包含 5 個步驟：θ、ρ、π、χ、ι。

海綿結構的優勢：
- 抵抗長度擴展攻擊
- 可以產生可變長度的輸出（SHAKE128、SHAKE256）
- 設計安全邊界更加清晰

## 雜湊函數的選擇

截至 2023 年，以下是推薦的雜湊函數：

| 用途 | 推薦方案 |
|:---|:---|
| 一般用途 | SHA-256 |
| 高效 64 位元平台 | SHA-512 |
| 新系統設計 | SHA3-256 或 BLAKE2 |
| 密碼雜湊 | bcrypt、scrypt、Argon2 |
| 金鑰推導 | HKDF |

## 延伸閱讀

- [Merkle-Damgård 構造](https://www.google.com/search?q=Merkle+Damgard+construction)
- [SHA-2 規範](https://www.google.com/search?q=SHA-2+FIPS+180+standard)
- [SHA-3 標準](https://www.google.com/search?q=SHA-3+FIPS+202+standard)
- [SHAttered 攻擊細節](https://www.google.com/search?q=SHAttered+attack+SHA1)
- [海綿結構](https://www.google.com/search?q=sponge+construction+Keccak)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
