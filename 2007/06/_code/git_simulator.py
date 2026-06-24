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

    def branch(self, name):
        ref_file = os.path.join(self.refs_dir, name)
        current = self.commits[-1] if self.commits else None
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
    print(f'   已新增 README.md')
    print()

    print('3. 提交變更')
    commit_id = git.commit('Initial commit', {'README.md': file_id})
    print(f'   提交完成 (commit: {commit_id[:7]}...)')
    print()

    print('4. 查看歷史')
    git.log()

    print('5. 建立分支')
    git.branch('feature')
    print('   已建立 feature 分支')

if __name__ == '__main__':
    demo()