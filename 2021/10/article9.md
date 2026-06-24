# 靜態分析工具與程式碼風格

## 為何需要靜態分析？

靜態分析在不執行程式的情況下檢查程式碼，能發現：
- 潛在錯誤
- 風格問題
- 安全漏洞
- 類型錯誤

Python 有許多優秀的靜態分析工具。

## Black：程式碼格式化

Black 是「不容置疑的」格式化工具：

```bash
pip install black
black my_module.py
```

特點：
- 幾乎不需要配置
- 產生一致的风格
- 不可調的格式決策

配置 `pyproject.toml`：

```toml
[tool.black]
line-length = 88
target-version = ['py39']
```

## Flake8：風格檢查

Flake8 結合了 pyflakes、pycodestyle、mccabe：

```bash
pip install flake8
flake8 my_module.py
```

常見選項：
- `--ignore=E501`：忽略行過長警告
- `--select=E,F,W`：選擇檢查類別

## isort：匯入排序

統一 import 語句順序：

```bash
pip install isort
isort my_module.py
```

配置 `pyproject.toml`：

```toml
[tool.isort]
profile = "black"
```

## Bandit：安全掃描

發現常見安全問題：

```bash
pip install bandit
bandit -r my_project/
```

檢測的問題包括：
- SQL 注入風險
- 使用 eval()
- 硬編碼密碼
- 不安全的 random

## mypy：類型檢查

如前所述，mypy 提供靜態類型檢查：

```bash
pip install mypy
mypy --strict my_module.py
```

## 整合到 pre-commit

使用 pre-commit鉤子自動化：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 21.10b0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 4.1.1
    hooks:
      - id: flake8
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

## CI 中的靜態檢查

```yaml
- name: Lint
  run: |
    flake8 my_module.py
    mypy my_module.py
    bandit -r my_module.py
```

## 結論

靜態分析工具讓你在不執行測試的情況下發現問題。將它們整合到開發流程中，能及早發現問題並保持程式碼品質。