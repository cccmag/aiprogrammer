# 程式碼範例：Git 版本控制示範

本期的所有程式碼範例集中在 `_code/git_demo.py` 中，透過單一 Python 腳本展示 Git 的核心概念。

## 執行方式

```bash
cd _code
python3 git_demo.py
```

## 範例涵蓋內容

`git_demo.py` 中的 `demo()` 函數依序展示：

1. **初始化儲存庫** — 使用 `git init` 建立新專案
2. **建立與提交檔案** — add 和 commit 操作
3. **檢視提交歷史** — `git log` 的使用
4. **分支操作** — 建立和切換分支
5. **合併操作** — 將分支合併回主線

## 輸出範例

執行後會看到類似以下的輸出：

```
=== Git 版本控制示範 ===
✓ git init 完成
✓ 首次提交完成
✓ 提交歷史:
e7a2f1c Initial commit
✓ 分支與提交完成
✓ 合併完成
✓ 最終提交圖:
*   a1b2c3d Merge branch 'feature'
|\
| * e5f6g7h Add feature file
|/
* e7a2f1c Initial commit
```

## 技術實作

範例使用 Python 的 `subprocess` 模組直接呼叫系統中的 Git 指令，並在臨時目錄中操作，執行完畢後自動清理。這種做法展示了如何用 Python 程式化控制 Git。

## 程式碼結構

```python
# git_demo.py 主要結構
def run_git(args, cwd):
    # 封裝 subprocess 呼叫 Git 命令
    
def demo():
    # 1. git init → 建立新儲存庫
    # 2. add + commit → 首次提交
    # 3. git log → 檢視歷史
    # 4. branch → 建立功能分支
    # 5. merge → 合併回主線
    # 6. 清理暫存目錄

if __name__ == "__main__":
    demo()
```

詳細程式碼說明請參考 [article10.md](article10.md) 用 Python 操作 Git。

更多 Python Git 整合請查閱 https://www.google.com/search?q=Python+Git+subprocess+教學。

## 自行擴充

讀者可以修改 `git_demo.py`，加入更多 Git 操作，例如：

- 模擬合併衝突
- 示範 rebase 流程
- 操作遠端儲存庫
- 展示 .gitignore 效果
