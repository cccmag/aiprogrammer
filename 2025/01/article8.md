# 檔案讀寫與異常處理

## 檔案讀寫的完整模式

### 檔案開啟模式

```python
# 常見模式
# "r"  — 讀取（預設）
# "w"  — 寫入（覆蓋）
# "a"  — 附加（在末尾添加）
# "x"  — 獨佔建立（檔案已存在則失敗）
# "b"  — 二進位模式
# "+"  — 讀寫模式

with open("data.txt", "r+", encoding="utf-8") as f:
    content = f.read()
    f.seek(0)  # 回到檔案開頭
    f.write("新增內容\n")
```

### 二進位檔案操作

```python
# 複製圖片
with open("source.jpg", "rb") as src:
    data = src.read()

with open("copy.jpg", "wb") as dst:
    dst.write(data)
```

### 大型檔案的逐行處理

```python
def process_large_file(filename):
    """處理大型檔案（避免一次讀入記憶體）"""
    with open(filename, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            # 逐行處理
            if "ERROR" in line:
                print(f"第 {line_number} 行有錯誤：{line.strip()}")
```

## 異常處理

### try/except 的基本結構

```python
try:
    number = int(input("請輸入一個數字："))
    result = 10 / number
    print(f"10 / {number} = {result}")
except ValueError:
    print("請輸入有效的數字！")
except ZeroDivisionError:
    print("不能除以零！")
except Exception as e:
    print(f"發生未知錯誤：{e}")
```

### 完整的異常處理結構

```python
try:
    with open("config.json", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("設定檔不存在，使用預設值")
    data = '{"theme": "default"}'
except PermissionError:
    print("沒有讀取權限")
    raise  # 重新拋出異常
else:
    print("設定檔讀取成功")
finally:
    print("無論如何都會執行（例如關閉資源）")
```

### 自訂異常

```python
class InsufficientBalanceError(Exception):
    """餘額不足的自訂異常"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"餘額不足：餘額 ${balance}，需要 ${amount}")

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceError(self.balance, amount)
        self.balance -= amount
        return amount

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金額必須為正數")
        self.balance += amount

account = BankAccount("Alice", 1000)
try:
    account.withdraw(1500)
except InsufficientBalanceError as e:
    print(f"錯誤：{e}")
    print(f"當前餘額：${e.balance}")
```

## with 的進階用法：情境管理器

```python
class Timer:
    """計時器情境管理器"""
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.perf_counter() - self.start
        print(f"執行時間：{elapsed:.4f} 秒")
        return False  # 不抑制異常

with Timer():
    total = sum(range(1000000))
    print(f"總和：{total}")
```

## 實戰：安全的檔案操作

```python
import json
import os
from datetime import datetime

class TaskManager:
    """安全的任務管理工具"""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self._load()

    def _load(self):
        """從檔案載入任務"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"建立新檔案：{self.filename}")
            return []
        except json.JSONDecodeError:
            print(f"檔案損壞，備份並重新建立")
            self._backup()
            return []
        except Exception as e:
            print(f"載入錯誤：{e}")
            return []

    def _backup(self):
        """備份檔案"""
        if os.path.exists(self.filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{self.filename}.{timestamp}.bak"
            os.rename(self.filename, backup_name)
            print(f"已備份到：{backup_name}")

    def add(self, title):
        """新增任務"""
        if not title.strip():
            raise ValueError("任務不能為空白")
        self.tasks.append({
            "id": len(self.tasks) + 1,
            "title": title.strip(),
            "created": datetime.now().isoformat(),
            "done": False
        })
        self._save()

    def complete(self, task_id):
        """完成任務"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = True
                self._save()
                return
        raise KeyError(f"找不到任務 #{task_id}")

    def _save(self):
        """安全地儲存到檔案"""
        temp_file = f"{self.filename}.tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
            os.replace(temp_file, self.filename)  # 原子操作
        except Exception as e:
            print(f"儲存失敗：{e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

    def show(self):
        """顯示任務"""
        if not self.tasks:
            print("目前沒有任務")
            return
        for task in self.tasks:
            status = "✓" if task["done"] else " "
            print(f"[{status}] #{task['id']} {task['title']}")

# 使用範例
manager = TaskManager("mytasks.json")
manager.add("學習 Python")
manager.add("閱讀程式設計書籍")
manager.complete(1)
manager.show()
```

## 小結

檔案操作和異常處理是建立可靠程式的基石。好的錯誤處理不僅讓程式更穩定，也讓使用者體驗更好。記住：不是所有錯誤都需要避免，但所有錯誤都應該被妥善處理。

---

**延伸閱讀**

- [Python 官方文件 — 檔案 I/O](https://www.google.com/search?q=Python+file+IO+error+handling)
- [Python 異常處理最佳實踐](https://www.google.com/search?q=Python+exception+handling+best+practices)
