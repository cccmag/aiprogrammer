# 數位簽章與憑證

## 什麼是數位簽章？

數位簽章（Digital Signature）是公開金鑰密碼學的關鍵應用之一，用於驗證數位訊息的真實性和完整性。一個安全的數位簽章方案應滿足：

- **身分認證**：證明簽章者的身分
- **完整性**：確保訊息未被篡改
- **不可否認性**：簽章者無法否認曾簽署該訊息

## 簽章流程

數位簽章的基本流程如下：

### 簽章（由發送者執行）

1. 計算訊息的雜湊值 h = H(m)
2. 使用私鑰對雜湊值進行簽章 s = Sign(sk, h)
3. 發送 (m, s) 對

### 驗證（由接收者執行）

1. 計算訊息的雜湊值 h = H(m)
2. 使用公鑰驗證簽章 Verify(pk, h, s)

如果雜湊匹配且簽章有效，接收者可以確信訊息確實來自宣稱的發送者且未被篡改。

## RSA 簽章

RSA 可以用於數位簽章。簽章生成相當於用私鑰對雜湊值進行「解密」操作：

```
s = h^d mod n
```

驗證時，用公鑰對簽章進行「加密」操作：

```
h' = s^e mod n
```

如果 h' = h，簽章有效。

在實務中，RSA 簽章通常使用 PSS（Probabilistic Signature Scheme）填充，以提供更高的安全性。

## ECDSA 簽章

橢圓曲線數位簽章演算法（ECDSA）是 ECC 版本的簽章方案。其安全性基於 ECDLP。

ECDSA 的簽章由兩個整數 (r, s) 組成。簽章生成的關鍵步驟是選擇隨機數 k，計算點 k × G 並取其 x 座標作為 r，然後計算 s = k^(-1)(hash + d × r)。

ECDSA 的隨機數 k 必須保持機密且從不重複使用。如果 k 被洩露，攻擊者可以恢復私鑰。2010 年，Sony PlayStation 3 就是因為使用了固定的 k 值而導致 ECDSA 私鑰被破解。

## EdDSA 與 Ed25519

EdDSA（Edwards-curve Digital Signature Algorithm）是基於 Twisted Edwards 曲線的現代簽章方案。其最廣泛的實作是 Ed25519（使用 Curve25519）。

Ed25519 的優勢：
- 高效能：比 ECDSA 更快
- 安全性：避免了 ECDSA 的隨機數生成缺陷
- 無專利限制：完全公開

## 憑證與 PKI

數位憑證（Digital Certificate）將公鑰與實體身分綁定。最常用的標準是 X.509。

X.509 憑證包含以下資訊：
- **版本號**：目前主要使用 v3
- **序號**：憑證的唯一標識
- **簽章演算法**：用於簽署憑證的演算法
- **發行者**：頒發憑證的 CA（憑證機構）
- **有效期**：開始和結束日期
- **主體**：憑證持有者
- **公鑰資訊**：公鑰和對應的演算法
- **延伸欄位**：可選的 v3 延伸

## 憑證鏈

憑證鏈（Certificate Chain）是信任傳遞的基礎結構。頂層是根 CA（Root CA），其憑證是自簽名的。中間 CA 由根 CA 簽名，最終的實體憑證由中間 CA 簽名。

```
Root CA (自簽名)
  └─ 簽發 Intermediate CA 1
       └─ 簽發 網站憑證
```

瀏覽器和作業系統內建了受信任的根 CA 列表。當你訪問 HTTPS 網站時，瀏覽器會驗證憑證鏈，直到找到一個受信任的根 CA。

## Let's Encrypt 與自動化

Let's Encrypt 是一個免費、自動化的 CA，使用 ACME（Automatic Certificate Management Environment）協議。它在 2023 年已簽發超過 3 億份憑證，極大地推動了 HTTPS 的普及。

ACME 協議通過驗證對域名的控制權來自動頒發憑證，無需人工審核。這大幅降低了 HTTPS 的部署門檻。

## 延伸閱讀

- [Digital Signature 標準](https://www.google.com/search?q=digital+signature+algorithm+DSS)
- [ECDSA 說明](https://www.google.com/search?q=ECDSA+how+it+works)
- [Ed25519 介紹](https://www.google.com/search?q=Ed25519+digital+signature)
- [X.509 憑證格式](https://www.google.com/search?q=X.509+certificate+format)
- [Let's Encrypt](https://www.google.com/search?q=Let%27s+Encrypt+ACME)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」密碼學基礎系列之六。*
