# 公開金鑰密碼學：RSA

## 金鑰分發問題

在對稱式密碼系統中，通訊雙方必須共享同一個金鑰。這引發了一個看似無解的難題：在沒有安全通道的情況下，如何安全地建立一個共享金鑰？

這個問題被稱為金鑰分發問題（Key Distribution Problem），長期困擾著密碼學家。傳統的解法需要面對面交換金鑰，或通過可信的第三方運送。這兩種方式在大規模網絡中都不實用。

## 公開金鑰密碼學的革命

1976 年，Whitfield Diffie 和 Martin Hellman 發表了里程碑論文《New Directions in Cryptography》，提出了公開金鑰密碼學（Public-Key Cryptography）的概念。其核心思想是使用兩個不同的金鑰：

- **公鑰**：公開給所有人，用於加密
- **私鑰**：由持有人秘密保管，用於解密

任何人都可以用 Bob 的公鑰加密訊息，但只有 Bob 能用他的私鑰解密。這徹底解決了金鑰分發問題。

Diffie 和 Hellman 還提出了 Diffie-Hellman 金鑰交換協議，允許雙方在不安全的通道上建立共享金鑰。DH 協議的安全性基於離散對數問題的計算困難性。

## RSA 演算法的誕生

1977 年，Ron Rivest、Adi Shamir 和 Leonard Adleman 在 MIT 提出了 RSA 演算法。RSA 是第一個實現了公開金鑰加密與數位簽章的完整方案。其名稱來自三位發明者的姓氏縮寫。

RSA 的安全性基於一個簡單的數論事實：將兩個大質數相乘很容易，但反過來——對它們的乘積進行因數分解——極其困難。

## 數論基礎

RSA 依賴於以下數論概念：

### 模運算

模運算（Modular Arithmetic）的符號 a mod n 表示 a 除以 n 的餘數。例如 17 mod 5 = 2。

### 尤拉函數

尤拉函數 φ(n) 表示小於等於 n 且與 n 互質的正整數個數。對於質數 p，φ(p) = p - 1。對於兩個質數的乘積 n = p × q，φ(n) = (p - 1)(q - 1)。

### 尤拉定理

尤拉定理聲明：如果 a 與 n 互質，則 a^φ(n) ≡ 1 (mod n)。這個定理是 RSA 正確性的理論基礎。

## RSA 演算法

### 金鑰生成

1. 選擇兩個大質數 p 和 q
2. 計算 n = p × q
3. 計算 φ(n) = (p - 1)(q - 1)
4. 選擇公鑰指數 e（1 < e < φ(n)），且 gcd(e, φ(n)) = 1。常用值為 65537
5. 計算私鑰指數 d ≡ e^(-1) (mod φ(n))

公鑰：(e, n)，私鑰：(d, n)

### 加密

將明文 m 轉換為整數，確保 m < n。計算密文 c：

```
c = m^e mod n
```

### 解密

```
m = c^d mod n
```

### 正確性證明

解密的正確性由尤拉定理保證。因為 e × d ≡ 1 (mod φ(n))，所以：

```
c^d ≡ (m^e)^d ≡ m^(ed) ≡ m^(kφ(n) + 1) ≡ m × (m^φ(n))^k ≡ m × 1^k ≡ m (mod n)
```

## 安全考量

RSA 的安全性依賴於因數分解的計算困難性。目前已知最好的因數分解演算法是 GNFS（General Number Field Sieve），其時間複雜度為次指數級。

### 金鑰長度建議

- 1024 位元：不再被認為安全
- 2048 位元：目前的最低標準
- 4096 位元：更高的安全要求

### 常見攻擊

- **選擇密文攻擊**：攻擊者可以解碼任意選擇的密文
- **低指數攻擊**：如果 e 太小（如 3）且多個接收者使用相同指數，可能被攻擊
- **共模攻擊**：如果同一 n 有兩個不同 e，攻擊者可能解密

在實際應用中，RSA 通常與 OAEP 填充方案一起使用，以抵抗選擇密文攻擊。

## RSA 的效能

RSA 的加解密速度遠慢於對稱加密。在實務上，RSA 通常用於加密對稱金鑰本身（金鑰封裝），而實際資料則使用 AES 等對稱加密方案。

這形成了混合加密系統（Hybrid Cryptosystem），結合了公開金鑰密碼學的便利性和對稱加密的效率。

## 延伸閱讀

- [Diffie-Hellman 論文 1976](https://www.google.com/search?q=Diffie+Hellman+New+Directions+in+Cryptography)
- [RSA 原始論文](https://www.google.com/search?q=RSA+paper+1978+Rivest+Shamir+Adleman)
- [RSA 數論基礎](https://www.google.com/search?q=RSA+number+theory+Euler+theorem)
- [因數分解演算法 GNFS](https://www.google.com/search?q=general+number+field+sieve)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」密碼學基礎系列之三。*
