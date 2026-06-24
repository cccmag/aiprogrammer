# Git 程式實作

## 模擬 Git 命令

```python
#!/usr/bin/env python3
"""Git 命令示範（模擬）"""


class GitSimulator:
    """模擬 Git 的基本操作"""

    def __init__(self):
        self.files = {}
        self.commits = []
        self.branches = ['main']
        self.current_branch = 'main'
        self.staging_area = {}

    def add(self, filename):
        """git add - 新增到暫存區"""
        with open(filename, 'r') as f:
            content = f.read()
        self.staging_area[filename] = content
        print(f"Added '{filename}' to staging area")

    def commit(self, message):
        """git commit - 提交更改"""
        if not self.staging_area:
            print("Nothing to commit")
            return

        commit = {
            'message': message,
            'files': dict(self.staging_area),
            'branch': self.current_branch
        }
        self.commits.append(commit)

        for filename in self.staging_area:
            self.files[filename] = self.staging_area[filename]

        self.staging_area.clear()
        print(f"Created commit: {message}")

    def log(self):
        """git log - 查看提交歷史"""
        if not self.commits:
            print("No commits yet")
            return
        for i, commit in enumerate(reversed(self.commits)):
            print(f"Commit {len(self.commits) - i}: {commit['message']}")

    def branch(self, name=None):
        """git branch - 列出或建立分支"""
        if name is None:
            for b in self.branches:
                marker = '*' if b == self.current_branch else ' '
                print(f"  {marker} {b}")
        else:
            self.branches.append(name)
            print(f"Created branch: {name}")

    def checkout(self, name):
        """git checkout - 切換分支"""
        if name in self.branches:
            self.current_branch = name
            print(f"Switched to branch: {name}")
        else:
            print(f"Branch '{name}' not found")

    def merge(self, branch):
        """git merge - 合併分支"""
        if branch not in self.branches:
            print(f"Branch '{branch}' not found")
            return
        if branch == self.current_branch:
            print("Already on this branch")
            return
        print(f"Merged '{branch}' into '{self.current_branch}'")


def demo():
    """Git 操作示範"""
    print("=" * 50)
    print("Git 命令示範")
    print("=" * 50)

    print("\n1. 基本工作流程（模擬）：")
    print("   ① 建立檔案 test.txt")
    print("   ② git add test.txt")
    print("   ③ git commit -m 'Initial commit'")

    git = GitSimulator()

    # 創建測試檔案（實際不創建）
    print("\n   $ echo 'Hello, Git!' > test.txt")
    print("   $ git add test.txt")
    git.add('test.txt')

    print("\n   $ git commit -m 'Initial commit'")
    git.commit('Initial commit')

    print("\n2. 分支操作（模擬）：")
    print("   $ git branch feature-x")
    git.branch('feature-x')

    print("\n   $ git checkout feature-x")
    git.checkout('feature-x')

    print("\n3. 提交歷史（模擬）：")
    git.log()

    print("\n4. 合併分支（模擬）：")
    git.checkout('main')
    git.merge('feature-x')

    print("\n" + "=" * 50)
    print("真實 Git 命令參考：")
    print("   git init              - 初始化倉庫")
    print("   git clone <url>       - 克隆倉庫")
    print("   git add <file>        - 新增到暫存區")
    print("   git commit -m <msg>    - 提交")
    print("   git push              - 推送到遠端")
    print("   git pull              - 拉取並合併")
    print("   git branch            - 列出分支")
    print("   git checkout <branch>  - 切換分支")
    print("   git merge <branch>     - 合併分支")
    print("=" * 50)


if __name__ == "__main__":
    demo()
```

## 參考資源

- [Git+official+site](https://www.google.com/search?q=Git+official+site)
- [GitHub+guides](https://www.google.com/search?q=GitHub+guides+tutorial)