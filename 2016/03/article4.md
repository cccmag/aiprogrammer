# 密碼雜湊與儲存

## 密碼儲存的基本原則

**千萬不要儲存明文密碼！** 這是最重要的安全原則。即使資料庫被竊取，只要密碼有正確雜湊，攻擊者短期內也無法使用這些密碼。

## 為什麼不應該用 MD5 或 SHA-1

MD5 和 SHA-1 是快速雜湊函數，專為高速運算設計。這對效能有好處，但對密碼儲存來說是災難：

- 現代顯示卡每秒可計算數十億次 MD5
- 攻擊者可快速產生「彩虹表」破解常見密碼
- 相同密碼產生相同雜湊，相同密碼的使用者會有相同雜湊

## 密碼雜湊函數

### bcrypt

專為密碼設計的雜湊函數，內建鹽值與可配置的工作因數：

```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# 使用
hashed = hash_password("MyS3cure!Pass")
verify_password("MyS3cure!Pass", hashed)  # True
verify_password("wrong", hashed)  # False
```

### scrypt

設計來了對抗硬體暴力破解的記憶體-hard 函數：

```python
import hashlib

password = b"my password"
salt = b"random_salt"
key = hashlib.scrypt(password, salt=salt, n=16384, r=8, p=1, maxmem=32*1024*1024, dklen=32)
```

### Argon2

2015 年 Password Hashing Competition 的冠軍，結合了記憶體-hard 與計算-hard 的特性：

```python
import argon2

ph = argon2.PasswordHasher()
hashed = ph.hash("my password")
ph.verify(hashed, "my password")
```

## 鹽值（Salt）

鹽值是附加在密碼上的隨機資料，用於確保相同密碼產生不同的雜湊：

```python
import os
import bcrypt

def hash_password(password):
    salt = os.urandom(16)  # 128 位元隨機鹽值
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return salt + hashed  # 儲存時包含鹽值

def verify_password(password, stored):
    salt = stored[:16]  # 取回鹽值
    hashed = stored[16:]
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

bcrypt 會自動處理鹽值，上例僅用於說明原理。

## 工作因數（Work Factor）

工作因數控制計算需要的時間。工作因數增加一倍，計算時間大約增加一倍。

```python
# bcrypt 工作因數測試
import bcrypt
import time

for rounds in [10, 11, 12, 13, 14]:
    start = time.time()
    bcrypt.hashpw(b"password", bcrypt.gensalt(rounds=rounds))
    elapsed = time.time() - start
    print(f"rounds={rounds}: {elapsed:.3f}s")
```

建議設定使得每次雜湊計算需要 200-500ms。這樣對正常使用者的登入體驗影響不大，但會讓暴力破解變得不切實際。

## 密碼強度檢查

```python
import re

def check_password_strength(password):
    errors = []

    if len(password) < 12:
        errors.append("密碼長度至少需要 12 個字元")

    if not re.search(r"[a-z]", password):
        errors.append("需要包含小寫字母")
    if not re.search(r"[A-Z]", password):
        errors.append("需要包含大寫字母")
    if not re.search(r"\d", password):
        errors.append("需要包含數字")
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;':\",./<>?\\`~]", password):
        errors.append("需要包含特殊符號")

    common = ['password', '12345678', 'qwerty', 'abc123', 'letmein']
    if password.lower() in common or password.lower().replace('o', '0').replace('i', '1') in common:
        errors.append("密碼太過常見")

    return errors if errors else None
```

## 常見錯誤

### 錯誤 1：只雜湊一次

```python
# 不安全：直接 MD5
hashlib.md5(password.encode()).hexdigest()

# 建議：使用 bcrypt/scrypt/argon2
bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### 錯誤 2：使用對稱加密

```python
# 不安全：金鑰可能洩露
cipher = AES.new(key, AES.MODE_CBC)
ciphertext = cipher.encrypt(password)
```

### 錯誤 3：忘記更新演算法

```python
# 當需要升級時（如發現 bcrypt 的弱點），重新雜湊密碼
def upgrade_password(old_hash, password):
    if verify_password(password, old_hash):
        new_hash = hash_password(password)
        store(new_hash)
```

## 參考資源

- https://www.google.com/search?q=密碼+雜湊+bcrypt+scrypt+Argon2+儲存+安全+2016
- https://www.google.com/search?q=密碼+鹽值+Salt+bcrypt+工作因數+強度+驗證
- https://www.google.com/search?q=MD5+SHA1+不適合+密碼+儲存+暴力破解+彩虹表