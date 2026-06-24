# HMAC 與金鑰推導

## 為什麼需要 MAC？

在安全通訊中，加密只能保證機密性，無法保證完整性——攻擊者可以篡改密文而不被發現。訊息認證碼（Message Authentication Code, MAC）正是解決這一問題的工具。

MAC 使用共享金鑰對訊息產生一個認證標籤（Tag）。接收者使用相同的金鑰驗證標籤，確保訊息在傳輸中未被篡改。

## HMAC 的設計

HMAC（Hash-based MAC）由 Mihir Bellare、Ran Canetti 和 Hugo Krawczyk 於 1996 年提出，是將雜湊函數轉化為 MAC 的標準方法。其設計理念是使用雜湊函數（如 SHA-256）作為黑盒子，構造安全的 MAC。

HMAC 的計算公式：

```
HMAC(K, m) = H((K' ⊕ opad) || H((K' ⊕ ipad) || m))
```

其中：
- K' 是經由填充或雜湊處理後的金鑰
- ipad 是 0x36 重複形成的位元組序列
- opad 是 0x5C 重複形成的位元組序列
- || 表示串接

### 內外填充的用意

HMAC 使用兩個不同的填充值（ipad 和 opad）來產生兩個不同的金鑰衍生值。這種設計確保了：

1. **金鑰分離**：內層和外層使用不同的金鑰衍生值
2. **長度擴展攻擊防護**：內層雜湊值的輸出作為外層的輸入，防止了 Merkle-Damgård 雜湊函數的長度擴展攻擊

### HMAC 的安全性

如果底層雜湊函數是安全的，HMAC 被認為是安全的 MAC。具體而言，HMAC 的安全性依賴於：
- 底層雜湊函數的抗碰撞性
- 金鑰的不可預測性

對於 HMAC-SHA256，安全強度為 min(256, 金鑰長度)。

## 金鑭推導函數 (KDF)

金鑰推導函數（Key Derivation Function, KDF）從主金鑰或密碼中派生出一組安全金鑰。

### HKDF

HKDF（HMAC-based KDF）由 HMAC 的設計者提出，包含兩個階段：

**提取（Extract）**：將不均勻的密碼材料轉換為偽隨機金鑰（PRK）

```
PRK = HMAC(salt, IKM)
```

**擴展（Expand）**：使用 PRK 產生所需長度的多個金鑰

```
T(0) = 空字串
T(i) = HMAC(PRK, T(i-1) || info || i)
OKM = T(1) || T(2) || ... || T(n)
```

HKDF 廣泛用於 TLS 1.3、IPSec 和 WireGuard 等協議中。

### 密碼雜湊

密碼雜湊（Password Hashing）是 KDF 的一種特殊形式，用於安全儲存密碼。與一般的 KDF 不同，密碼雜湊需要設計成計算密集型，以抵抗暴力破解。

常用的密碼雜湊方案：
- **bcrypt**：基於 Blowfish 密碼，自適應（可增加迭代次數）
- **scrypt**：記憶體密集型，抵抗 ASIC 攻擊
- **Argon2**：2015 年 Password Hashing Competition 的獲勝者，提供三種變體

## MAC 與數位簽章的區別

| 特性 | MAC | 數位簽章 |
|:---|:---|:---|
| 金鑰類型 | 對稱金鑰 | 公鑰與私鑰 |
| 不可否認性 | 無 | 有 |
| 計算效率 | 高 | 低 |
| 金鑰分發 | 需要安全通道 | 公鑰可公開 |

## 延伸閱讀

- [HMAC RFC 2104](https://www.google.com/search?q=HMAC+RFC+2104)
- [HKDF RFC 5869](https://www.google.com/search?q=HKDF+RFC+5869)
- [Password Hashing Competition](https://www.google.com/search?q=password+hashing+competition+Argon2)
- [bcrypt vs scrypt vs Argon2](https://www.google.com/search?q=bcrypt+scrypt+Argon2+comparison)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
