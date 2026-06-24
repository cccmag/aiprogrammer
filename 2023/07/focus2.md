# 對稱式加密：AES 與 DES

## 對稱式密碼學概述

對稱式加密（Symmetric Encryption）是指加密與解密使用相同金鑰的密碼系統。其優勢在於效率高、適合大量資料加密，但金鑰分發與管理是主要挑戰。

對稱式加密分為兩大類：串流密碼（Stream Cipher）與區塊密碼（Block Cipher）。串流密碼逐位元加密，適合即時通訊；區塊密碼將明文分成固定大小的區塊逐塊加密，是當今最主流的對稱加密形式。

## 混淆與擴散

Claude Shannon 在其 1949 年的論文中提出了兩個密碼設計的基本原則：

**混淆（Confusion）**：使密文與金鑰之間的統計關係盡可能複雜。即使攻擊者知道密文的統計特性，也無法推斷出金鑰的資訊。在現代區塊密碼中，S-box（替代盒）主要負責提供混淆。

**擴散（Diffusion）**：將明文的統計結構擴散到密文中。改變明文中的一個位元，應導致密文中大約一半的位元發生變化——這被稱為雪崩效應（Avalanche Effect）。置換操作（Permutation）主要負責提供擴散。

## Feistel 網路

許多區塊密碼採用 Feistel 網路結構，由 Horst Feistel 在 IBM 設計 Lucifer 密碼時提出。其運作方式如下：

1. 將資料區塊分為左右兩半（L₀, R₀）
2. 每輪使用輪函數 F 和子金鑰 Kᵢ 處理右半部
3. 將結果與左半部進行 XOR，然後交換左右半部

```
Lᵢ = Rᵢ₋₁
Rᵢ = Lᵢ₋₁ ⊕ F(Rᵢ₋₁, Kᵢ)
```

Feistel 網路的美妙之處在於：無論輪函數 F 是否可逆，解密過程都與加密相同（只需反序使用子金鑰）。這大大簡化了硬體實作。

## DES：資料加密標準

DES（Data Encryption Standard）由 IBM 在 1970 年代開發，1977 年被 NBS（現 NIST）採納為美國聯邦標準。

DES 使用 56 位元金鑰加密 64 位元區塊，採用 16 輪 Feistel 網路結構。每輪包含擴展置換、S-box 替代和 P-box 置換等步驟。

雖然 DES 在當時是革命性的，但 56 位元的金鑰長度在現代計算能力面前已不再安全。1998 年，EFF（電子前線基金會）設計的 Deep Crack 機器在 56 小時內破解了 DES。1999 年，分散式計算專案在 22 小時內破解了 DES。

3DES（Triple DES）是 DES 的強化版本，使用三個 DES 金鑰進行加密-解密-加密（EDE）序列，有效金鑰長度達到 112 或 168 位元。然而 3DES 速度較慢，且 64 位元區塊大小使其易受分組碰撞攻擊。

## AES：高級加密標準

1997 年，NIST 公開徵求新的加密標準以取代 DES。經過五年的評選，2001 年，Rijndael 演算法（由比利時密碼學家 Joan Daemen 和 Vincent Rijmen 設計）被選為 AES。

AES 的關鍵規格：
- 區塊大小：128 位元（固定）
- 金鑰長度：128、192 或 256 位元
- 輪數：10（128 位元金鑰）、12（192 位元）、14（256 位元）

AES 採用 SPN（Substitution-Permutation Network）結構，而非 Feistel 網路。每輪包含四個步驟：

1. **SubBytes**：使用 S-box 對每個位元組進行非線性替代
2. **ShiftRows**：對狀態矩陣的行進行循環移位
3. **MixColumns**：對狀態矩陣的列進行混合運算
4. **AddRoundKey**：將狀態矩陣與輪金鑰進行 XOR

與 Feistel 網路不同，AES 的每個步驟都是可逆的，這使得解密需要反序執行反向操作。AES 的設計充分利用了現代 CPU 的並行處理能力，在軟體和硬體實現中都有出色表現。

## AES 的安全性

截至目前，AES 仍然被認為是安全的。已知最有效的攻擊是旁路攻擊（Side-Channel Attack），而非對演算法本身的密碼分析。AES-128 的安全強度被估計為約 126 位元，遠高於 DES 的 56 位元。

## 實作考量

在實務上，區塊密碼需要搭配操作模式（Mode of Operation）使用：

- **ECB**：最簡單但最不安全，相同明文區塊產生相同密文
- **CBC**：引入前一個密文區塊作為反饋
- **CTR**：將區塊密碼轉換為串流密碼，支援並行加密
- **GCM**：結合加密與認證，提供最強的安全性

## 延伸閱讀

- [Shannon 混淆與擴散原則](https://www.google.com/search?q=Shannon+confusion+diffusion)
- [Feistel Cipher Structure](https://www.google.com/search?q=Feistel+network+cipher)
- [AES 標準文件](https://www.google.com/search?q=AES+FIPS+197+standard)
- [區塊密碼操作模式](https://www.google.com/search?q=block+cipher+mode+of+operation)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」密碼學基礎系列之二。*
