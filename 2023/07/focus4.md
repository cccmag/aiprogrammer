# 橢圓曲線密碼學 ECC

## 從 RSA 到 ECC

RSA 的安全性依賴於大整數因數分解的困難性，這需要非常大的金鑰（2048 位元以上）才能保證安全。隨著行動裝置和物聯網設備的普及，更高效能的公開金鑰方案成為迫切需求。

橢圓曲線密碼學（Elliptic Curve Cryptography, ECC）在 1985 年由 Neal Koblitz 和 Victor Miller 獨立提出。ECC 能夠以更短的金鑰提供與 RSA 相當的安全性，這使其在資源受限的環境中具有顯著優勢。

## 安全性比較

| 安全強度 (bits) | RSA 金鑰長度 | ECC 金鑰長度 |
|:---:|:---:|:---:|
| 80 | 1024 | 160 |
| 112 | 2048 | 224 |
| 128 | 3072 | 256 |
| 256 | 15360 | 512 |

一個 256 位元的 ECC 金鑰提供的安全性相當於 3072 位元的 RSA 金鑰。這意味著 ECC 的計算量更小、金鑰更短、頻寬消耗更低。

## 橢圓曲線的數學

橢圓曲線（Elliptic Curve）是由以下方程式定義的點的集合：

```
y² = x³ + ax + b
```

其中 4a³ + 27b² ≠ 0，以確保曲線沒有奇點（自交或尖點）。

在密碼學中，我們通常使用有限域上的橢圓曲線，即座標取自有限域 GF(p) 或 GF(2^m)。

### 點的加法

橢圓曲線上的點構成一個阿貝爾群。點加法（Point Addition）的幾何定義如下：

給定曲線上的兩個點 P 和 Q，通過 P 和 Q 畫一條直線，該直線與曲線交於第三個點 R'，然後 R' 關於 x 軸的鏡像即為 P + Q 的結果。

### 純量乘法

純量乘法（Scalar Multiplication）是點加法重複應用的結果：

```
k × P = P + P + ... + P (k 次)
```

ECC 的安全性基於橢圓曲線離散對數問題（ECDLP）：給定點 P 和點 Q = k × P，在計算上無法在合理時間內找到整數 k。ECDLP 被認為比整數因數分解和傳統離散對數問題更難。

## ECDH：金鑰交換

橢圓曲線 Diffie-Hellman（ECDH）是傳統 Diffie-Hellman 的 ECC 版本：

1. Alice 生成私鑰 d_A 和公鑰 Q_A = d_A × G
2. Bob 生成私鑰 d_B 和公鑰 Q_B = d_B × G
3. Alice 計算共享密鑰 S = d_A × Q_B
4. Bob 計算共享密鑰 S = d_B × Q_A

雙方得到相同的共享密鑰，因為 d_A × (d_B × G) = d_B × (d_A × G)。

## ECDSA：數位簽章

橢圓曲線數位簽章演算法（ECDSA）是 ECC 版本的 DSA。簽章過程如下：

**簽章生成**：
1. 選擇隨機整數 k
2. 計算 R = k × G，取 r = R_x mod n
3. 計算 s = k^(-1)(hash(m) + d × r) mod n
4. 簽章為 (r, s)

**簽章驗證**：
1. 計算 w = s^(-1) mod n
2. 計算 u1 = hash(m) × w mod n, u2 = r × w mod n
3. 計算 P = u1 × G + u2 × Q
4. 如果 P_x ≡ r (mod n)，簽章有效

## 標準曲線

NIST 定義了一組標準的橢圓曲線參數，包括 P-256、P-384 和 P-521（對應不同安全級別）。此外，Curve25519（用於 X25519 金鑰交換）和 Ed25519（用於 EdDSA 簽章）因其高效能和安全性而日益流行。

Curve25519 由 Daniel J. Bernstein 設計，使用蒙哥馬利曲線形式，避免了一些專利問題，並在設計上考慮了側信道攻擊的防護。

## ECC 的應用

ECC 廣泛應用於現代安全協議中：

- **TLS**：支持 ECDHE 金鑰交換
- **SSH**：支持 Ed25519 和金鑰交換
- **加密貨幣**：比特幣和以太坊使用 secp256k1 曲線
- **智慧卡與 IoT**：ECC 的短金鑰特性使其成為嵌入式設備的理想選擇

## 量子威脅

與 RSA 一樣，ECC 也受到量子電腦的威脅。Shor 演算法可以在多項式時間內解決 ECDLP，這意味著大規模量子電腦將徹底打破 ECC 的安全性。後量子密碼學正在開發能夠抵抗量子攻擊的替代方案。

## 延伸閱讀

- [Elliptic Curve Cryptography 介紹](https://www.google.com/search?q=elliptic+curve+cryptography+introduction)
- [ECDH 金鑰交換](https://www.google.com/search?q=ECDH+key+exchange)
- [ECDSA 數位簽章](https://www.google.com/search?q=ECDSA+digital+signature)
- [Curve25519 設計](https://www.google.com/search?q=Curve25519+Bernstein)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」密碼學基礎系列之四。*
