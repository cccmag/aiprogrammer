# 開源專案的維護之道

## 前言

開源專案的維護不僅僅是寫程式碼，更涉及社群建設、版本管理、文件撰寫等多方面工作。本文探討如何有效地維護一個開源專案。

## 開始一個開源專案

### 選擇授權

```python
licenses = {
    'MIT': '寬鬆，適合大多數專案',
    'Apache 2.0': '包含專利授權，適合大公司參與',
    'GPL v3': '要求衍生作品也開源',
    'LGPL': '允許商業使用，適合函式庫',
    'AGPL': '最嚴格，連網路使用也要求開源',
}

def choose_license(project_type, commercial_use=False):
    if project_type == 'library':
        return 'LGPL' if commercial_use else 'MIT'
    elif project_type == 'server':
        return 'AGPL'
    else:
        return 'MIT'
```

## README 的重要性

```markdown
# 好的 README 包含：

## 特色
- 功能列表

## 快速開始
- 安裝步驟
- 基本用法
- 程式碼範例

## 文件
- 詳細 API 文檔
- 教學和指南

## 貢獻
- 開發指南
- CODE_OF_CONDUCT

## 授權
- 授權條款
```

## 程式碼規範

### 風格指南

```python
# Python: PEP 8
# JavaScript: Airbnb Style Guide
# Rust: rustfmt

style_check_tools = {
    'python': ['flake8', 'pylint', 'black'],
    'javascript': ['eslint', 'prettier'],
    'rust': ['rustfmt', 'clippy'],
}
```

### Linting 配置

```json
// .eslintrc.json
{
    "extends": "airbnb-base",
    "rules": {
        "no-unused-vars": "warn",
        "semi": ["error", "always"]
    }
}
```

## 自動化測試

### 測試框架

```python
# pytest
import pytest

def test_add():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -1) == -2

# Mock
from unittest.mock import Mock

def test_api_call(monkeypatch):
    def mock_get(*args, **kwargs):
        return {'data': 'test'}

    monkeypatch.setattr(requests, 'get', mock_get)
    result = fetch_data()
    assert result == {'data': 'test'}
```

### CI/CD 整合

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest
    - name: Lint
      run: flake8
```

## 版本管理

### 語義化版本

```python
def bump_version(current_version, release_type):
    major, minor, patch = map(int, current_version.split('.'))

    if release_type == 'major':
        return f"{major + 1}.0.0"
    elif release_type == 'minor':
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"

# Semantic Versioning 2.0.0
# MAJOR.MINOR.PATCH
# MAJOR: 不相容的 API 改變
# MINOR: 向後相容的功能新增
# PATCH: 向後相容的錯誤修復
```

### CHANGELOG

```markdown
# Changelog

## [1.0.0] - 2026-06-01

### Added
- 新功能 A
- 新功能 B

### Changed
- 改變了 X 的行為

### Deprecated
- Y 被廢棄，使用 Z 替代

### Fixed
- 修復了 Bug #123

### Security
- 安全更新
```

## 文件撰寫

### API 文件

```python
def calculate_stats(data, method='mean'):
    """
    計算資料集的統計量。

    Args:
        data: 輸入資料，應為數值列表
        method: 統計方法，'mean'、'median' 或 'mode'

    Returns:
        float: 計算結果

    Raises:
        ValueError: 當 method 無效或 data 為空時

    Example:
        >>> calculate_stats([1, 2, 3, 4, 5])
        3.0
        >>> calculate_stats([1, 2, 3, 4, 5], method='median')
        3.0
    """
    if not data:
        raise ValueError("Data cannot be empty")
    if method == 'mean':
        return sum(data) / len(data)
    # ...
```

### 文件生成工具

```python
doc_tools = {
    'Python': 'Sphinx, pdoc',
    'JavaScript': 'JSDoc, ESDoc',
    'Rust': 'rustdoc',
}
```

## 社群建設

### CODE_OF_CONDUCT

```markdown
# CODE_OF_CONDUCT

## 我們的承諾
- 尊重和包容
- 專業和友善
- 不接受騷擾

## 執行
違反此準則的行為可通過 [聯繫方式] 向社群團隊報告。

## 感謝
靈感來自 Contributor Covenant
```

### Issue 和 PR 模板

```markdown
## Issue 模板
### Bug 報告
- 描述問題
- 重現步驟
- 預期行為
- 實際行為
- 環境資訊

### 功能請求
- 描述功能
- 使用場景
- 可能的實現方式
```

## 發布管理

### GitHub Releases

```bash
# 標籤版本
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0

# 生成發行說明
# GitHub 會自動根據 commit 歷史生成
```

### Package Registry

```python
# PyPI 发布
# 1. 準備 package
# 2. 建立 .pypirc
# 3. 建構發布
python -m build
twine upload dist/*

# npm 发布
# 1. 登入 npm
# 2. 發布
npm publish
```

## 小結

開源專案維護是一項全面的工作，涉及技術、溝通和專案管理等多方面能力。通過良好的文件、自動化測試、清晰的社群指南和持續的維護，您可以建立一個繁榮的開源專案。

---

**延伸閱讀**

- [Open Source Guide](https://www.google.com/search?q=GitHub+open+source+guides)
- [Maintainer's Guide](https://www.google.com/search?q=open+source+maintainer+guide)
- [Community Building](https://www.google.com/search?q=open+source+community+building)