# Diffie-Hellman 金鑰交換

## 革命性的想法

在 Diffie 和 Hellman 發表 1976 年的論文之前，密碼學界普遍認為金鑰分發問題是無解的。如果沒有事先共享的金鑰，兩方如何在不安全的通道上建立一個共享金鑰？這聽起來像是先有雞還是先有蛋的問題。

Diffie 和 Hellman 的天才之處在於，他們認識到某些數學問題具有不對稱性——正向計算容易，逆向計算困難。利用這種不對稱性，可以讓雙方在不安全的通道上取得共享的秘密。

## 彩色顏料類比

理解 DH 金鑰交換的最佳方式是使用彩色顏料類比：

1. Alice 和 Bob 公開協議使用一種共同的顏料（黃色）
2. Alice 選擇私密顏色（紅色），混合黃色得到橙色，發送給 Bob
3. Bob 選擇私密顏色（藍色），混合黃色得到綠色，發送給 Alice
4. Alice 將自己的私密顏色（紅色）混入 Bob 發送的綠色中，得到棕色
5. Bob 將自己的私密顏色（藍色）混入 Alice 發送的橙色中，得到棕色

兩者得到的棕色是相同的！而攻擊者看到的是橙色和綠色，但無法在不區分混合顏料的情況下得到棕色。

這個類比對應的數學操作是——混合顏料難以分離，就像離散對數難以計算一樣。

## 離散對數問題

離散對數問題（Discrete Logarithm Problem, DLP）定義如下：

給定一個質數 p、一個原根 g 和一個值 A = g^a mod p，計算 a。

正向計算（已知 a 求 A）很容易——使用快速模指數。逆向計算（已知 A 求 a）卻極其困難——沒有已知的多項式時間演算法。

DLP 被認為是計算困難問題。目前最快的演算法（指數積分法、數域篩法）也是次指數時間的。

## DH 的數學細節

完整的 DH 金鑰交換數學描述：

1. 公開參數：大質數 p 和原根 g
2. Alice 選擇 a（私密），計算 A = g^a mod p
3. Bob 選擇 b（私密），計算 B = g^b mod p
4. Alice 計算 K = B^a mod p = (g^b)^a mod p = g^(ab) mod p
5. Bob 計算 K = A^b mod p = (g^a)^b mod p = g^(ab) mod p

### 原根（Primitive Root）

g 是模 p 的原根，意味著 g 的冪次可以生成模 p 的所有非零餘數：

```
{g^0, g^1, g^2, ..., g^(p-2)} ≡ {1, 2, ..., p-1} (mod p)
```

這確保了金鑰空間的均勻性。

## 安全性分析

DH 的安全性依賴於計算 Diffie-Hellman 問題（Computational Diffie-Hellman, CDH）的困難性：

給定 g、g^a、g^b，計算 g^(ab)。

CDH 問題不比離散對數問題更難——如果 DLP 被解決，CDH 自動被解決。目前普遍認為 CDH 與 DLP 等價。

### 中間人攻擊

未經認證的 DH 協議對中間人攻擊（MITM）完全開放：

```
Alice ←→ Mallory ←→ Bob
```

Mallory 分別與 Alice 和 Bob 建立 DH 金鑰，然後轉發所有訊息。Alice 和 Bob 都以為他們在直接通訊。

解決方案是使用數位簽章對 DH 的公開值進行簽章——這是 TLS 中 ECDHE 的標準做法。

## 前向安全性

前向安全性（Forward Secrecy）是 DH 協議的一個關鍵優勢。如果你使用 DH 交換金鑰後立即丟棄私密值 a 和 b，即使長期金鑰在未來被洩露，過去通訊的內容也無法被解密。

在 TLS 中，使用 DHE（基於 DH）或 ECDHE（基於 ECC）的密碼套件提供前向安全性。靜態 RSA 密碼套件（其中會話金鑰使用伺服器公鑰加密）不提供前向安全性。

## 延伸閱讀

- [Diffie-Hellman 原始論文](https://www.google.com/search?q=Diffie+Hellman+New+Directions+in+Cryptography+1976)
- [離散對數問題](https://www.google.com/search?q=discrete+logarithm+problem)
- [前向安全性](https://www.google.com/search?q=forward+secrecy+TLS)
- [中間人攻擊](https://www.google.com/search?q=man+in+the+middle+attack+Diffie+Hellman)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
