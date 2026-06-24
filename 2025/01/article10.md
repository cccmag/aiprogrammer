# 小專案：建立命令列工具

## 前言

在本系列的最後一篇文章中，我們將整合所學的所有知識，建立一個完整的命令列工具。這個專案將展示如何從需求分析到實作部署的完整流程。

## 專案規劃：密碼管理器

我們將建立一個簡單的密碼管理器，支援：

1. 產生安全的隨機密碼
2. 儲存服務名稱與密碼
3. 檢視已儲存的密碼
4. 搜尋特定服務的密碼

## 專案結構

```
password_manager/
├── __init__.py
├── generator.py
├── storage.py
├── cli.py
└── main.py
```

## 步驟一：密碼產生器

```python
# generator.py
import random
import string

class PasswordGenerator:
    """密碼產生器"""

    def __init__(self, length=16):
        self.length = length

    def generate(self, use_upper=True, use_lower=True,
                 use_digits=True, use_symbols=True):
        """產生隨機密碼"""
        chars = ""
        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation

        if not chars:
            raise ValueError("至少需要選擇一種字元類型")

        password = ''.join(random.choice(chars) for _ in range(self.length))
        return password

    def generate_pin(self, length=6):
        """產生純數字 PIN 碼"""
        return ''.join(random.choice(string.digits) for _ in range(length))

    def generate_readable(self, words=4):
        """產生可讀的密碼短語"""
        word_list = ["apple", "blue", "chair", "dance", "eagle",
                     "fancy", "green", "happy", "input", "joker"]
        return '-'.join(random.choice(word_list) for _ in range(words))
```

## 步驟二：資料儲存

```python
# storage.py
import json
import os
from cryptography.fernet import Fernet

class PasswordStorage:
    """密碼儲存管理器"""

    def __init__(self, filename="passwords.json"):
        self.filename = filename
        self.key_file = ".secret.key"
        self._load_key()
        self.passwords = self._load()

    def _load_key(self):
        """載入或產生加密金鑰"""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)

    def _load(self):
        """從檔案載入密碼"""
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                encrypted = f.read()
            if encrypted:
                decrypted = self.cipher.decrypt(encrypted.encode())
                return json.loads(decrypted)
        except Exception as e:
            print(f"載入錯誤：{e}")
        return {}

    def _save(self):
        """儲存密碼到檔案"""
        data = json.dumps(self.passwords, ensure_ascii=False)
        encrypted = self.cipher.encrypt(data.encode())
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(encrypted.decode())

    def add(self, service, username, password):
        """新增密碼"""
        if service not in self.passwords:
            self.passwords[service] = []
        self.passwords[service].append({
            "username": username,
            "password": password
        })
        self._save()
        print(f"已儲存 {service} 的登入資訊")

    def get(self, service):
        """取得特定服務的密碼"""
        return self.passwords.get(service, [])

    def list_services(self):
        """列出所有服務"""
        return list(self.passwords.keys())

    def search(self, query):
        """搜尋服務"""
        return [s for s in self.passwords if query.lower() in s.lower()]

    def delete(self, service, index=None):
        """刪除密碼"""
        if service not in self.passwords:
            print(f"找不到 {service}")
            return
        if index is None:
            del self.passwords[service]
        else:
            entries = self.passwords[service]
            if 0 <= index < len(entries):
                del entries[index]
                if not entries:
                    del self.passwords[service]
        self._save()
        print(f"已刪除 {service} 的登入資訊")
```

## 步驟三：命令列介面

```python
# cli.py
import argparse
from .generator import PasswordGenerator
from .storage import PasswordStorage

def setup_parser():
    """設定命令列參數解析器"""
    parser = argparse.ArgumentParser(
        description="密碼管理器 — 產生與儲存安全密碼",
        epilog="使用範例：python -m password_manager generate -l 20"
    )

    subparsers = parser.add_subparsers(dest="command")

    # generate 子命令
    gen_parser = subparsers.add_parser("generate", help="產生密碼")
    gen_parser.add_argument("-l", "--length", type=int, default=16,
                           help="密碼長度（預設：16）")
    gen_parser.add_argument("--no-symbols", action="store_true",
                           help="不包含特殊字元")

    # add 子命令
    add_parser = subparsers.add_parser("add", help="新增密碼")
    add_parser.add_argument("service", help="服務名稱")
    add_parser.add_argument("-u", "--username", required=True, help="使用者名稱")
    add_parser.add_argument("-p", "--password", help="密碼（留空則自動產生）")

    # get 子命令
    get_parser = subparsers.add_parser("get", help="取得密碼")
    get_parser.add_argument("service", help="服務名稱")

    # list 子命令
    subparsers.add_parser("list", help="列出所有服務")

    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜尋服務")
    search_parser.add_argument("query", help="搜尋關鍵字")

    return parser
```

## 步驟四：主程式

```python
# main.py
from .cli import setup_parser
from .generator import PasswordGenerator
from .storage import PasswordStorage

def main():
    parser = setup_parser()
    args = parser.parse_args()

    gen = PasswordGenerator()
    storage = PasswordStorage()

    if args.command == "generate":
        password = gen.generate(length=args.length,
                               use_symbols=not args.no_symbols)
        print(f"產生的密碼：{password}")
        print(f"密碼長度：{len(password)}")

    elif args.command == "add":
        password = args.password
        if not password:
            password = gen.generate()
            print(f"自動產生的密碼：{password}")
        storage.add(args.service, args.username, password)

    elif args.command == "get":
        entries = storage.get(args.service)
        if not entries:
            print(f"找不到 {args.service} 的資訊")
        else:
            print(f"=== {args.service} ===")
            for i, entry in enumerate(entries):
                print(f"  [{i}] 使用者：{entry['username']}")
                print(f"      密碼：{entry['password']}")

    elif args.command == "list":
        services = storage.list_services()
        if not services:
            print("目前沒有儲存任何密碼")
        else:
            print("=== 已儲存的服務 ===")
            for s in services:
                count = len(storage.get(s))
                print(f"  {s} ({count} 筆)")

    elif args.command == "search":
        results = storage.search(args.query)
        if not results:
            print(f"找不到包含「{args.query}」的服務")
        else:
            print("=== 搜尋結果 ===")
            for s in results:
                print(f"  {s}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

## 執行與測試

```bash
# 產生密碼
python -m password_manager generate -l 20

# 新增密碼
python -m password_manager add github -u myaccount -p MySecret123!

# 取得密碼
python -m password_manager get github

# 列出所有服務
python -m password_manager list

# 搜尋
python -m password_manager search github
```

## 專案總結

這個密碼管理器專案涵蓋了本系列的多個主題：

- **模組化設計**：將功能拆分到不同檔案
- **輸入處理**：使用 argparse 處理命令列參數
- **加密儲存**：使用 cryptography 套件加密敏感資料
- **錯誤處理**：處理各種邊界情況
- **使用者體驗**：提供清晰的輸出訊息

## 下一步學習方向

完成這個專案後，你可以繼續探索：

1. **圖形化介面**：使用 tkinter 或 PyQt 建立桌面應用
2. **網路功能**：使用 Flask 建立 Web API
3. **資料庫**：使用 SQLite 替代 JSON 儲存
4. **測試**：為每個模組編寫單元測試
5. **發布**：打包成 PyPI 套件供他人使用

## 小結

從變數到完整專案，你已經完成了 Python 程式設計的基礎學習。最重要的是繼續練習——試著自己構思一個小專案並實作出來。每一次的實作都會讓你的程式設計能力更上一層樓。

---

**延伸閱讀**

- [Python argparse 教學](https://www.google.com/search?q=Python+argparse+tutorial)
- [Python 專案打包指南](https://www.google.com/search?q=Python+packaging+tutorial)
- [密碼安全性最佳實踐](https://www.google.com/search?q=password+security+best+practices)
