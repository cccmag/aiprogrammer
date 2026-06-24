# 數位簽章實作

## 簽章的基礎

數位簽章將公開金鑰密碼學和雜湊函數結合，提供了身分認證、完整性和不可否認性。本篇文章將展示如何使用 Python 實作 RSA 和 ECDSA 簽章。

## RSA 簽章實作

使用 PyCryptodome 庫可以輕鬆實作 RSA 簽章：

```python
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# 生成金鑰對
key = RSA.generate(2048)

# 簽章
message = b"Hello, world!"
h = SHA256.new(message)
signature = pkcs1_15.new(key).sign(h)

# 驗證
h = SHA256.new(message)
try:
    pkcs1_15.new(key.publickey()).verify(h, signature)
    print("Sign valid")
except (ValueError, TypeError):
    print("Sign invalid")
```

### PSS 填充

PKCS#1 v1.5 簽章方案雖然廣泛使用，但存在已知的安全缺陷。PSS（Probabilistic Signature Scheme）是更安全的替代方案：

```python
from Crypto.Signature import pss
signature = pss.new(key).sign(h)
```

PSS 使用隨機鹽值（salt），確保每次簽章結果不同，即使對同一訊息也是如此。

## ECDSA 實作

ECDSA 使用橢圓曲線進行簽章：

```python
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

# 生成 ECC 金鑰對
key = ECC.generate(curve='P-256')

# 簽章
message = b"Hello, world!"
h = SHA256.new(message)
signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(h)

# 驗證
verifier = DSS.new(key.public_key(), 'fips-186-3')
try:
    verifier.verify(h, signature)
    print("Sign valid")
except ValueError:
    print("Sign invalid")
```

### ECDSA 的注意事項

ECDSA 要求每次簽章使用不同的隨機數 k。如果 k 被重複使用或可預測，攻擊者可以恢復私鑰。著名的案例包括：

- **Sony PlayStation 3（2010）**：使用了固定的 k，導致 ECDSA 私鑰被破解
- **Android Bitcoin 錢包（2013）**：隨機數生成器缺陷導致私鑰洩露

## Ed25519 實作

Ed25519 使用 Python 的純 Python 實作（或 libsodium 綁定）：

```python
import nacl.signing

# 生成金鑰對
key = nacl.signing.SigningKey.generate()

# 簽章
message = b"Hello, world!"
signed = key.sign(message)

# 驗證
verify_key = key.verify_key
try:
    verify_key.verify(signed)
    print("Sign valid")
except nacl.exceptions.BadSignatureError:
    print("Sign invalid")
```

Ed25519 不使用隨機數，每次簽章是確定性的——這是一個重要的安全優勢。

## 多訊息簽章

在實際應用中，我們通常簽章雜湊值而非原始訊息。這不僅提高了效率（訊息可以任意大），還能保護原始訊息不直接暴露於簽章演算法中。

### 簽章鏈

在一些場景下，我們需要對一系列相關訊息進行簽章，例如區塊鏈中的交易。簽章鏈（Signature Chain）將前一筆簽章納入當前訊息的雜湊計算中：

```python
def sign_chain(prev_signature, message, key):
    combined = prev_signature + message
    h = SHA256.new(combined)
    return pkcs1_15.new(key).sign(h)
```

## 延伸閱讀

- [PKCS#1 v2.2](https://www.google.com/search?q=PKCS+1+RSA+cryptography+standard)
- [ECDSA 隨機數安全](https://www.google.com/search?q=ECDSA+nonce+reuse+attack)
- [Ed25519 設計](https://www.google.com/search?q=Ed25519+signing+algorithm)
- [PyCryptodome 文件](https://www.google.com/search?q=PyCryptodome+digital+signature)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
