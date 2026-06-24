# 合併衝突解決

## 衝突的產生

當多人同時修改同一個檔案的同一個區域時，Git 無法自動決定哪個版本是正確的，就會產生合併衝突。

### 衝突情境

假設兩位開發者同時修改 `app.py`：

```python
# Alice 的版本
def greet():
    return "Hello from Alice"

# Bob 的版本
def greet():
    return "Hello from Bob"
```

當 Bob 先推送，Alice 要推送時就會遇到衝突。

### 解決衝突的步驟

```bash
# 拉取最新變更
git pull origin main

# Git 顯示衝突訊息
# CONFLICT in app.py

# 檢視衝突檔案
git status

# 手動編輯解決衝突
# <<<<<<< HEAD 與 ======= 之間是當前版本
# ======= 與 >>>>>>> branch 之間是進來的版本

# 完成後標記為已解決
git add app.py
git commit
```

### 衝突解決策略

1. **直接編輯**：手動選擇保留哪些內容
2. **合併工具**：使用 vimdiff、meld 等工具
3. **策略選擇**：
   - `git merge --ours`：保留當前版本
   - `git merge --theirs`：保留進來的版本
   - `git merge --squash`：壓縮合併

### Python 模擬衝突處理

```python
class ConflictResolver:
    def __init__(self):
        self.local = ""
        self.remote = ""
    
    def resolve_with_marker(self, filename, local, remote):
        merged = (
            f"<<<<<<< HEAD\n{local}"
            f"=======\n{remote}"
            f">>>>>>> incoming\n"
        )
        print(f"衝突檔案：{filename}")
        print("請手動編輯解決衝突")
        return merged
    
    def auto_resolve(self, strategy="ours"):
        if strategy == "ours":
            return self.local
        elif strategy == "theirs":
            return self.remote
        return f"{self.local}\n# merged\n{self.remote}"

resolver = ConflictResolver()
resolver.local = "print('local')"
resolver.remote = "print('remote')"
result = resolver.resolve_with_marker("test.py", 
    resolver.local, resolver.remote)
print(result)
```

更多衝突解決技巧請參考 https://www.google.com/search?q=Git+merge+conflict+解決方法。
