#!/usr/bin/env python3
"""Git 版本控制操作演示"""

def demo():
    print("=" * 50)
    print("Git 版本控制操作演示")
    print("=" * 50)

    print("\n=== 1. 基本操作流程 ===")
    print("git init              - 初始化倉庫")
    print("git clone <url>       - 克隆倉庫")
    print("git status            - 查看狀態")
    print("git add <file>        - 新增到暫存區")
    print("git commit -m '<msg>' - 提交")

    print("\n=== 2. 分支操作 ===")
    print("git branch            - 列出分支")
    print("git branch <name>     - 建立分支")
    print("git checkout <branch> - 切換分支")
    print("git checkout -b <new> - 建立並切換")
    print("git merge <branch>    - 合併分支")
    print("git branch -d <name>  - 刪除分支")

    print("\n=== 3. 同步操作 ===")
    print("git push              - 推送到遠端")
    print("git pull              - 拉取並合併")
    print("git fetch             - 只獲取不下載")
    print("git remote -v         - 查看遠端")

    print("\n=== 4. 查看歷史 ===")
    print("git log               - 提交歷史")
    print("git log --oneline     - 精簡格式")
    print("git log --graph       - 圖形顯示")
    print("git diff              - 查看變更")

    print("\n=== 5. 復原操作 ===")
    print("git restore <file>    - 恢復檔案")
    print("git reset --soft HEAD~1  - 取消提交")
    print("git revert <commit>   - 反轉提交")
    print("git stash             - 暫存修改")

    print("\n" + "=" * 50)
    print("Git 操作演示完成！")
    print("=" * 50)

if __name__ == "__main__":
    demo()