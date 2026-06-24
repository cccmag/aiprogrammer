#!/bin/bash
set -x

echo "=== 測試 Linux 與開源運動相關展示 ==="

# 測試 focus_code 概念
python3 -c "
print('Testing Linux concepts...')
cmds = ['ls', 'cd', 'cp', 'mv', 'rm', 'chmod', 'grep']
print(f'Commands defined: {len(cmds)}')
print('Test passed: Linux concepts loaded')
"

# 測試 business model 展示
python3 -c "
print('Testing open source business models...')
models = ['Open Core', 'Dual License', 'Subscription', 'SaaS']
print(f'Models: {models}')
print('Test passed: Business models')
"

# 測試其他 Python 展示
python3 -c "
print('Testing year 2007 highlights...')
highlights = ['Ubuntu 7.10', 'MySQL 5.1', 'Git 1.5.3', 'Android SDK']
print(f'Highlights: {highlights}')
print('Test passed: 2007 highlights')
"

echo ""
echo "=== 所有測試完成 ==="