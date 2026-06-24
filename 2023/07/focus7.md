# 密碼協議與安全通訊

## 什麼是密碼協議？

密碼協議（Cryptographic Protocol）是定義如何在兩方或多方之間安全地交換資訊的規則集合。協議將多個密碼學原語（加密、簽章、雜湊等）組合成一個完整的通訊框架。

安全通訊協議需要滿足以下目標：
- **機密性**：只有授權方可以讀取訊息內容
- **完整性**：確保訊息在傳輸中未被篡改
- **認證**：確認通訊對方的真實身分
- **不可否認性**：防止發送者否認發送過訊息

## Diffie-Hellman 金鑰交換

Diffie-Hellman（DH）金鑰交換協議由 Whitfield Diffie 和 Martin Hellman 於 1976 年提出。它允許雙方在不安全的通道上建立一個共享的秘密金鑰。

### 協議流程

1. 雙方協議使用一個大質數 p 和一個原根 g
2. Alice 選擇私密隨機數 a，計算 A = g^a mod p 並發送給 Bob
3. Bob 選擇私密隨機數 b，計算 B = g^b mod p 並發送給 Alice
4. Alice 計算共享金鑰 K = B^a mod p = g^(ab) mod p
5. Bob 計算共享金鑰 K = A^b mod p = g^(ab) mod p

雙方得到了相同的金鑰 K。即使攻擊者攔截了 g、p、A 和 B，也無法在合理時間內計算出 K，因為這需要解決離散對數問題。

### 中間人攻擊

傳統 DH 協議對中間人攻擊（MITM）是脆弱的。攻擊者 Mallory 可以攔截雙方的通訊，分別與 Alice 和 Bob 建立 DH 金鑰。為了解決這個問題，DH 需要與數位簽章或憑證結合使用——即認證的 DH（authenticated DH）。

### ECDHE

橢圓曲線版本的 Diffie-Hellman（ECDHE）使用 ECC 代替模指數運算。ECDHE 在 TLS 1.3 中是預設的金鑰交換方案，提供前向安全性（Forward Secrecy）：

即使伺服器的長期私鑰在未來被洩露，攻擊者仍然無法解密過去記錄的通訊內容。

## TLS 協定

TLS（Transport Layer Security）是保護網際網路通訊最廣泛使用的安全協定。

### TLS 握手

TLS 握手的目標是在客戶端和伺服器之間建立安全通道：

1. **ClientHello**：客戶端發送支援的 TLS 版本、密碼套件列表和隨機數
2. **ServerHello**：伺服器選擇 TLS 版本、密碼套件和隨機數
3. **伺服器憑證**：伺服器發送其 X.509 憑證
4. **金鑰交換**：客戶端和伺服器執行 ECDHE 或 DH 金鑰交換
5. **完成**：雙方確認握手完成，開始加密通訊

### TLS 1.3 的改進

TLS 1.3（2018 年發布）相比 TLS 1.2 有重大改進：

- **減少握手延遲**：1-RTT（一次往返）完成握手，0-RTT 可恢復會話
- **移除不安全選項**：移除了所有不安全的密碼套件
- **前向安全性**：所有金鑰交換都必須提供前向安全性
- **簡化密碼套件**：只有 5 個密碼套件

### 密碼套件

密碼套件（Cipher Suite）是一組演算法的組合。TLS 1.3 的密碼套件格式為：

```
TLS_AES_128_GCM_SHA256
```

這表示使用 AES-128-GCM 進行加密和認證，SHA256 用於金鑰推導。

## IPSec

IPSec（Internet Protocol Security）是在 IP 層提供安全通訊的協議套件。與在傳輸層運作的 TLS 不同，IPSec 加密整個 IP 封包。

IPSec 支援兩種模式：
- **傳輸模式**：只加密負載（payload），保留 IP 標頭
- **隧道模式**：加密整個 IP 封包，封裝在新 IP 封包中

## Signal 協議

Signal 協議（由 Open Whisper Systems 開發）是用於即時通訊的現代密碼協議。它結合了以下技術：

- **X3DH**：擴展的三重 Diffie-Hellman 金鑰協商
- **雙棘輪演算法**：提供端到端加密和前向安全性
- **預先金鑰**：支援非同步通訊

Signal 協議被 WhatsApp、Signal 和 Google Messages 等應用使用。

## 延伸閱讀

- [Diffie-Hellman 金鑰交換](https://www.google.com/search?q=Diffie+Hellman+key+exchange+protocol)
- [TLS 1.3 規範](https://www.google.com/search?q=TLS+1.3+RFC+8446)
- [Signal Protocol](https://www.google.com/search?q=Signal+protocol+double+ratchet)
- [IPSec 介紹](https://www.google.com/search?q=IPSec+VPN+security)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」密碼學基礎系列之七。*
