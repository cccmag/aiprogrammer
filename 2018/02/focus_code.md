# 程式碼範例

## Git 基本操作

```python
#!/usr/bin/env python3
"""Git 基本操作範例（概念說明）"""

def demo():
    print("=" * 50)
    print("Git 基本操作說明")
    print("=" * 50)

    # 1. 初始化
    print("\n1. 初始化 Git 倉庫:")
    print("   git init")

    # 2. 設定
    print("\n2. 設定使用者資訊:")
    print("   git config --global user.name 'Your Name'")
    print("   git config --global user.email 'your@email.com'")

    # 3. 查看狀態
    print("\n3. 查看狀態:")
    print("   git status")

    # 4. 新增檔案
    print("\n4. 新增檔案到暫存區:")
    print("   git add filename.txt")
    print("   git add .")

    # 5. 提交
    print("\n5. 提交:")
    print("   git commit -m '提交訊息'")

    # 6. 查看歷史
    print("\n6. 查看提交歷史:")
    print("   git log")
    print("   git log --oneline")

    # 7. 建立分支
    print("\n7. 分支操作:")
    print("   git branch                # 列出分支")
    print("   git branch feature        # 建立分支")
    print("   git checkout feature      # 切換分支")
    print("   git checkout -b feature   # 建立並切換")

    # 8. 合併
    print("\n8. 合併分支:")
    print("   git checkout master")
    print("   git merge feature")

    # 9. 刪除分支
    print("\n9. 刪除分支:")
    print("   git branch -d feature")

    # 10. 推送
    print("\n10. 推送到遠端:")
    print("    git remote add origin <url>")
    print("    git push -u origin master")

    print("\n" + "=" * 50)
    print("Git 常用指令說明完成")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

## 分支操作

```python
#!/usr/bin/env python3
"""分支操作範例"""

def demo():
    print("=" * 50)
    print("Git 分支操作說明")
    print("=" * 50)

    branches = {
        "master": "主分支，穩定版本",
        "develop": "開發分支",
        "feature/*": "功能分支",
        "bugfix/*": "錯誤修復分支",
        "hotfix/*": "緊急修復分支",
        "release/*": "發布分支"
    }

    print("\n分支類型:")
    for branch, desc in branches.items():
        print(f"  {branch:15} - {desc}")

    print("\n" + "-" * 50)
    print("分支操作流程:")
    print("-" * 50)

    steps = [
        ("建立功能分支", "git checkout -b feature/new-feature"),
        ("開發並提交", "git add . && git commit -m 'feat: 新功能'"),
        ("推送到遠端", "git push -u origin feature/new-feature"),
        ("發起 Pull Request", "在 GitHub 上建立 PR"),
        ("Code Review", "團隊成員審查程式碼"),
        ("合併到主分支", "Merge PR in GitHub"),
        ("刪除功能分支", "git branch -d feature/new-feature")
    ]

    for i, (desc, cmd) in enumerate(steps, 1):
        print(f"\n{i}. {desc}")
        print(f"   {cmd}")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    demo()
```

## 常見問題處理

```python
#!/usr/bin/env python3
"""Git 常見問題處理"""

def demo():
    print("=" * 50)
    print("Git 常見問題處理")
    print("=" * 50)

    problems = [
        {
            "問題": "工作到一半需要臨時切換分支",
            "解決": "git stash 暫存修改"
        },
        {
            "問題": "不小心commit 到錯誤分支",
            "解決": "git reset --soft HEAD~1 恢復"
        },
        {
            "問題": "想要修改最後一次 commit",
            "解決": "git commit --amend"
        },
        {
            "問題": "合併時發生衝突",
            "解決": "手動編輯衝突後 git add && git commit"
        },
        {
            "問題": "需要取消 merge",
            "解決": "git merge --abort"
        },
        {
            "問題": "想要回復到某個版本",
            "解決": "git reset --hard <commit-id>"
        }
    ]

    for i, p in enumerate(problems, 1):
        print(f"\n問題 {i}: {p['問題']}")
        print(f"解決: {p['解決']}")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    demo()
```

## 完整演示

```python
#!/usr/bin/env python3
"""Git 操作完整演示"""

def demo():
    print("=" * 50)
    print("Git 版本控制完整演示")
    print("=" * 50)

    print("\n這個腳本用於說明 Git 的基本概念和操作。")
    print("在實際環境中，你需要使用真正的 Git 指令。")

    # 狀態流程
    print("\n" + "-" * 50)
    print("檔案狀態流程:")
    print("-" * 50)

    states = [
        ("Untracked", "新檔案，Git 未開始追蹤", "git add"),
        ("Staged", "已加入暫存區", "git commit"),
        ("Modified", "已追蹤的檔案被修改", "git add"),
        ("Committed", "已提交到本地倉庫", "已提交")
    ]

    for state, desc, action in states:
        print(f"\n{state}:")
        print(f"  說明: {desc}")
        print(f"  下一步: {action}")

    print("\n" + "-" * 50)
    print("Git Flow 示意:")
    print("-" * 50)

    print("""
    master:    A ─── B ──── C ──── D
                              ↑
                         feature/abc
                              │
                         D' ── E' ── F'
    """)

    print("=" * 50)
    print("演示完成！")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

## 練習用的 Git 腳本概念

```python
#!/usr/bin/env python3
"""練習用的概念展示"""

def demo():
    print("=" * 50)
    print("Git 練習建議")
    print("=" * 50)

    exercises = [
        ("建立測試專案", "mkdir git-practice && cd git-practice && git init"),
        ("建立第一個檔案", 'echo "Hello" > hello.txt && git add .'),
        ("提交", 'git commit -m "Initial commit"'),
        ("建立分支", "git checkout -b feature"),
        ("修改並提交", "echo 'World' >> hello.txt && git add . && git commit -m 'feat: add world'"),
        ("切回 master", "git checkout master"),
        ("合併分支", "git merge feature"),
        ("檢視歷史", "git log --oneline --graph --all"),
        ("建立衝突", "再次切到 feature，改同一行，合併到 master"),
        ("解決衝突", "編輯檔案，git add . && git commit")
    ]

    for i, (desc, cmd) in enumerate(exercises, 1):
        print(f"\n{i}. {desc}")
        print(f"   指令: {cmd}")

    print("\n" + "=" * 50)
    print("祝練習順利！")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

## 實際操作（類比）

```python
#!/usr/bin/env python3
"""實際 Git 操作示範（說明版）"""

def demo():
    print("=" * 50)
    print("實際 Git 操作流程")
    print("=" * 50)

    workflow = [
        ("1. 克隆倉庫", "git clone https://github.com/user/repo.git"),
        ("2. 進入目錄", "cd repo"),
        ("3. 建立分支", "git checkout -b feature/my-feature"),
        ("4. 開發", "编辑檔案、修改代码..."),
        ("5. 查看變更", "git status && git diff"),
        ("6. 暫存檔案", "git add changed-file.py"),
        ("7. 提交", "git commit -m 'feat: add my feature'"),
        ("8. 推送", "git push -u origin feature/my-feature"),
        ("9. 建立 PR", "在 GitHub 上建立 Pull Request"),
        ("10. Code Review", "等待團隊審查..."),
        ("11. 合併", "在 GitHub 上點擊 Merge"),
        ("12. 更新本地", "git checkout master && git pull")
    ]

    for desc, cmd in workflow:
        print(f"\n{desc}")
        print(f"   {cmd}")

    print("\n" + "=" * 50)
    print("完整流程完成！")
    print("=" * 50)

if __name__ == "__main__":
    demo()
```

if __name__ == "__main__":
    demo()