# 雜湊函數與訊息摘要

## 什麼是雜湊函數？

雜湊函數（Hash Function）是一種將任意長度的輸入資料映射為固定長度輸出（稱為雜湊值或訊息摘要）的演算法。

密碼學雜湊函數需要具備以下性質：

**1. 抗原像性（Preimage Resistance）**：給定雜湊值 h，在計算上無法找到任何輸入 x 使得 H(x) = h。這也被稱為單向性。

**2. 抗第二原像性（Second Preimage Resistance）**：給定輸入 x₁，在計算上無法找到另一個輸入 x₂（x₂ ≠ x₁）使得 H(x₂) = H(x₁)。

**3. 抗碰撞性（Collision Resistance）**：在計算上無法找到任意兩個不同的輸入 x₁ 和 x₂ 使得 H(x₁) = H(x₂)。這比抗第二原像性更強，因為攻擊者可以自由選擇兩個輸入。

## MD5：已退役的標準

MD5（Message Digest Algorithm 5）由 Ron Rivest 於 1991 年設計，產生 128 位元的雜湊值。MD5 在很長一段時間內是最廣泛使用的雜湊函數。

然而，MD5 已被證明不安全。2004 年，中國密碼學家王小雲團隊提出了對 MD5 的有效碰撞攻擊。2008 年，研究人員成功製作了兩份簽名不同的 SSL 憑證，但它們的 MD5 雜湊值相同。從此 MD5 不再被推薦用於安全應用。

## SHA-1：逐漸退役

SHA-1（Secure Hash Algorithm 1）由 NIST 於 1995 年發布，產生 160 位元（20 位元組）的雜湊值。它在很長時期內是雜湊函數的黃金標準。

2017 年，由 Google 和 CWI Amsterdam 組成的團隊成功實現了 SHAttered 攻擊——對 SHA-1 的首次公開碰撞攻擊。他們需要 6500 CPU 年的計算量來找到碰撞，但這證明了 SHA-1 不再安全。微軟和 Google 已停止接受 SHA-1 簽章的 SSL 憑證。

## SHA-2 家族

SHA-2 是 NIST 在 2001 年發布的一系列雜湊函數，包括 SHA-224、SHA-256、SHA-384 和 SHA-512：

| 演算法 | 輸出長度 | 內部狀態 | 區塊大小 |
|:---:|:---:|:---:|:---:|
| SHA-224 | 224 bits | 256 bits | 512 bits |
| SHA-256 | 256 bits | 256 bits | 512 bits |
| SHA-384 | 384 bits | 512 bits | 1024 bits |
| SHA-512 | 512 bits | 512 bits | 1024 bits |

SHA-256 是目前最廣泛使用的雜湊函數。其內部結構基於 Merkle-Damgård 構造，壓縮函數基於 Davies-Meyer 結構。

SHA-256 的壓縮函數包含 64 輪計算，每輪使用不同的常數和邏輯函數。其設計提供了良好的混淆和擴散特性。

截至 2023 年，SHA-2 被認為是安全的。已知最有影響的攻擊是對 SHA-2 的縮減輪數版本（如 31/64 輪），但對完整 SHA-256 尚無實質威脅。

## SHA-3：新世代

2015 年，NIST 正式將 Keccak 演算法標準化為 SHA-3。與 SHA-2 不同，SHA-3 採用海綿結構（Sponge Construction），這是一種不同的設計範式。

海綿結構包含兩個階段：
1. **吸收（Absorb）**：將輸入區塊 XOR 到內部狀態中，然後應用置換函數
2. **擠壓（Squeeze）**：從內部狀態中提取輸出區塊

SHA-3 的優勢在於其對抗長度擴展攻擊的內在抵抗力，這使它在某些場景（如 HMAC 的替代方案 KMAC）中更安全。

SHA-3 家族包括 SHA3-224、SHA3-256、SHA3-384 和 SHA3-512，以及兩個可擴展輸出函數 SHAKE128 和 SHAKE256。

## 雜湊函數的應用

雜湊函數在密碼學和計算機科學中有廣泛應用：

- **密碼存儲**：儲存密碼的雜湊值而非明文
- **資料完整性**：驗證檔案或訊息是否被篡改
- **數位簽章**：簽章雜湊值而非原始訊息
- **訊息認證碼**：結合金鑰實現認證（HMAC）
- **區塊鏈**：區塊鏈的核心構建塊
- **Git**：使用 SHA-1 識別提交和物件
- **Merkle Tree**：高效驗證大資料集的完整性

## 延伸閱讀

- [Hash Function 基礎](https://www.google.com/search?q=cryptographic+hash+function+properties)
- [SHA-1 SHAttered 攻擊](https://www.google.com/search?q=SHAttered+SHA1+collision)
- [SHA-3 Keccak](https://www.google.com/search?q=SHA3+Keccak+sponge+construction)
- [王小雲 MD5 碰撞攻擊](https://www.google.com/search?q=Wang+Xiaoyun+MD5+collision)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」密碼學基礎系列之五。*
