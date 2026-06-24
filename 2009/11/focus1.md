# OAuth 1.0 與開放授權：安全認證

## OAuth 的由來

### 問題

```markdown
# 傳統的第三方訪問問題

使用者：「我想讓 XYZ 應用存取我的 Google 資料」
解決方案 1：「告訴我你的 Google 密碼」
問題：XYZ 獲得完全存取權

解決方案 2：「使用 OAuth」
好處：有限授權，可隨時撤回
```

## OAuth 1.0a 流程

```markdown
OAuth 1.0a 流程：

1. 用戶訪問 XYZ 應用
         ↓
2. XYZ 請求臨時憑證
         ↓
3. 用戶被重定向到 Google
         ↓
4. 用戶登入並授權
         ↓
5. 用戶返回 XYZ，帶著驗證碼
         ↓
6. XYZ 交換驗證碼為訪問令牌
         ↓
7. XYZ 使用令牌訪問 Google API
```

## 實作

```python
# OAuth 1.0a 簽名（簡化版）

import hmac
import hashlib
import base64
import time
import random
import urllib.parse


def oauth_signature(method, url, params, consumer_secret, token_secret=''):
    # 1. 合併參數
    all_params = sorted(params.items())
    param_str = '&'.join(f'{k}={v}' for k, v in all_params)

    # 2. 構造基礎字元串
    base_string = '&'.join([
        method.upper(),
        urllib.parse.quote(url, safe=''),
        urllib.parse.quote(param_str, safe='')
    ])

    # 3. 構造密鑰
    signing_key = f"{consumer_secret}&{token_secret}"

    # 4. HMAC-SHA1 簽名
    signature = hmac.new(
        signing_key.encode(),
        base_string.encode(),
        hashlib.sha1
    ).digest()

    return base64.b64encode(signature).decode()
```

## OAuth 2.0 的改進

```markdown
# OAuth 2.0 (2012) 簡化

# 1. 不再需要用戶簽名
# 2. 使用 HTTPS 傳輸
# 3. 多了授權碼流程
# 4. 支援多种 flow

# 應用場景：
# - Web Apps
# - Mobile Apps
# - JS Apps
```

## 結語

OAuth 是現代 API 安全的基礎，2009 年的 OAuth 1.0a 標準為後續發展奠定了基礎。

---

*本篇文章為「AI 程式人雜誌 2009 年 11 月號」焦點系列之一。*