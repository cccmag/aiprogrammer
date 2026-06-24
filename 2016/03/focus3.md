# 3. 密碼學基礎

## 密碼學的任務

密碼學是保護資訊安全的數學基礎，主要解決三個問題：

**機密性**：只有授權的人員能讀取訊息內容

**完整性**：確保訊息在傳輸過程中未被篡改

**身份驗證**：確認訊息來源或身份的真實性

## 對稱加密

對稱加密使用相同的金鑰進行加密與解密。速度較快，適合大量資料加密。

### 常見演算法

**AES（Advanced Encryption Standard）**：目前最廣泛使用的對稱加密標準。金鑰長度可達 256 位元，是美國政府核准的加密標準。

**DES / 3DES**：老舊的標準，DES 的金鑰長度只有 56 位元，已可被暴力破解。3DES 只是簡單地套用三次 DES，安全性仍不足。

**ChaCha20**：現代流加密，特別適合行動裝置使用。

### 使用範例（Python）

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(32)  # 256-bit key
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(b"Secret message")

# 輸出 ciphertext 和 tag
```

## 非對稱加密

非對稱加密使用一對金鑰：公鑰與私鑰。用公鑰加密的資料只能用私鑰解密，反之亦然。

### RSA

最廣泛使用的非對稱加密演算法。基於大數分解的數學難題。金鑰長度通常為 2048 或 4096 位元。

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

key = RSA.generate(2048)
cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(b"Secret message")
```

### 用途

- 金鑰交換：用非對稱加密協商對稱金鑰
- 數位簽章：確認訊息來源與完整性
- 安全通訊：雙方交換公鑰後用對稱加密通訊

## 雜湊函數

雜湊函數將任意長度的輸入轉換為固定長度的輸出，且無法從輸出反推輸入。主要用於資料完整性驗證與密碼儲存。

### 常見演算法

**SHA-256**：SHA-2 系列的一員，輸出 256 位元。目前最廣泛使用的安全雜湊標準。

**SHA-1**：較舊的標準，已發現碰撞攻擊，不建議用於安全場景。

**MD5**：輸出 128 位元，已被發現有嚴重漏洞，只適合非安全性用途（如檔案完整性檢查）。

**bcrypt**：專為密碼雜湊設計，內建鹽值與可調的工作因數，適合儲存密碼。

### 使用範例

```python
import hashlib

password = "mysecretpassword"
# 不建議：直接雜湊（容易被彩虹表攻擊）
h1 = hashlib.md5(password.encode()).hexdigest()

# 建議：使用 bcrypt
import bcrypt
salt = bcrypt.gensalt()
h2 = bcrypt.hashpw(password.encode(), salt)
```

## 數位簽章

數位簽章結合非對稱加密與雜湊，提供身份驗證與完整性保護。

```python
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

message = b"Send $100 to Alice"
h = SHA256.new(message)
signature = pkcs1_15.new(key).sign(h)
```

## 數位憑證與 PKI

公開金鑰基礎建設（PKI）解決了「如何確認公鑰屬於聲稱的人」的問題。

**數位憑證**：由可信的憑證授權中心（CA）簽發，綁定公鑰與身份資訊。

**TLS/SSL**：使用數位憑證與 PKI 實現安全 HTTPS 連線。

## 金鑰管理

密碼學最大的挑戰往往不是演算法本身，而是金鑰管理：

- 金鑰必須安全儲存
- 金鑰必須安全分發
- 過期的金鑰需要妥善銷毀
- 需要備份機制防止金鑰遺失

## 參考資源

- https://www.google.com/search?q=密碼學+AES+RSA+SHA+對稱+非對稱+加密+基礎+2016
- https://www.google.com/search?q=bcrypt+密碼+雜湊+鹽值+安全+儲存+最佳實踐
- https://www.google.com/search?q=TLS+PKI+數位憑證+CA+公開金鑰+基礎建設+原理