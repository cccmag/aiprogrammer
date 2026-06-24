# Git Hooks 自動化

## 什麼是 Git Hooks

Git Hooks 是在特定事件發生時自動執行的腳本，存放在 `.git/hooks/` 目錄中。

### Hook 類型

**用戶端 Hooks**：
- `pre-commit`：提交前執行（檢查程式碼風格）
- `commit-msg`：檢查提交訊息格式
- `pre-push`：推送前執行（執行測試）

**伺服器端 Hooks**：
- `pre-receive`：接收推送前
- `post-receive`：接收推送後

## 建立 Hook

```bash
# 進入 hooks 目錄
cd .git/hooks/

# 建立 pre-commit hook
cat > pre-commit << 'EOF'
#!/bin/bash
echo "執行提交前檢查..."
# 檢查是否有暫存的 Python 語法錯誤
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$'); do
    python3 -m py_compile "$file" 2>&1
    if [ $? -ne 0 ]; then
        echo "語法錯誤：$file"
        exit 1
    fi
done
echo "檢查通過！"
EOF

chmod +x pre-commit
```

## Python 實作 Hook 管理器

```python
import os
import stat

def install_hook(name, script):
    path = f".git/hooks/{name}"
    with open(path, "w") as f:
        f.write(script)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
    print(f"安裝 {name} 完成")

pre_commit = """#!/usr/bin/env python3
import subprocess, sys
result = subprocess.run(
    ["git", "diff", "--cached", "--name-only"],
    capture_output=True, text=True)
for f in result.stdout.strip().split("\\n"):
    if f.endswith(".py"):
        r = subprocess.run(["python3", "-m",
            "py_compile", f], capture_output=True)
        if r.returncode != 0:
            print(f"語法錯誤：{f}"); sys.exit(1)
print("檢查通過！")
"""

install_hook("pre-commit", pre_commit)
```

更多 Git Hooks 請參考 https://www.google.com/search?q=Git+Hooks+自動化+教學。
