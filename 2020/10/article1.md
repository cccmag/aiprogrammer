# pipenv 與 Poetry：新一代 Python 套件管理

## 前言

Python 的依賴管理工具經歷了從 easy_install 到 pip 的演變，而 Pipenv 和 Poetry 的出現，則代表了新一代 Python 套件管理的趨勢。它們將環境管理、依賴管理和專案打包統一起來，提供了更現代化的開發體驗。

## Pipenv

### Pipfile 的革命

Pipenv 使用 Pipfile 和 Pipfile.lock 來管理依賴，這比 requirements.txt 更加現代：

```toml
# Pipfile（TOML 格式）
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = ">=2.25.0"
flask = "~=1.1.0"
numpy = "*"

[dev-packages]
pytest = "*"
black = "*"

[requires]
python_version = "3.8"
```

### Pipenv 核心指令

```bash
# 安裝依賴
pipenv install                    # 安裝 Pipfile 中的依賴
pipenv install requests          # 安裝單個套件
pipenv install --dev pytest      # 安裝開發依賴

# 環境管理
pipenv shell                      # 進入虛擬環境的 shell
pipenv run python main.py        # 直接執行（不需要啟動 shell）
pipenv --python 3.8              # 指定 Python 版本

# 依賴更新
pipenv update                    # 更新所有依賴
pipenv update requests           # 更新單個套件

# 安全檢查
pipenv check                     # 檢查安全漏洞

# 圖形化依賴
pipenv graph                     # 顯示依賴圖
```

### Pipfile.lock 的作用

```json
{
    "_meta": {
        "hash": {"sha256": "..."},
        "pipfile-spec": 6,
        "requires": {"python_version": "3.8"},
        "sources": [...]
    },
    "default": {
        "requests": {
            "version": "==2.25.1",
            "hashes": ["sha256:...", "..."],
            "index": "pypi"
        }
    },
    "develop": {
        "pytest": {
            "version": "==6.2.2",
            ...
        }
    }
}
```

## Poetry

### pyproject.toml 的標準化

Poetry 使用 pyproject.toml（PEP 517/518 標準）：

```toml
[tool.poetry]
name = "my-awesome-project"
version = "0.1.0"
description = "An awesome Python project"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
requests = ">=2.25.0"
flask = {version = "~=1.1.0", optional = true}
numpy = "*"

[tool.poetry.dev-dependencies]
pytest = "^6.0"
black = "^20.8"
mypy = "^0.800"

[tool.poetry.extras]
web = ["flask"]

[tool.poetry.scripts]
myapp = "myapp.cli:main"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Poetry 核心指令

```bash
# 初始化
poetry new myproject              # 建立新專案
poetry init                       # 在現有目錄初始化

# 依賴管理
poetry add requests              # 新增依賴
poetry add --dev pytest          # 新增開發依賴
poetry add "flask>=1.1"          # 指定版本

# 安裝
poetry install                   # 安裝所有依賴
poetry install --no-dev         # 只安裝生產依賴

# 更新
poetry update                    # 更新所有依賴
poetry update requests           # 更新單個套件

# 鎖定和發布
poetry lock                      # 鎖定版本
poetry publish                   # 發布到 PyPI
poetry build                     # 建構 distribution
```

### 環境管理

```bash
poetry shell                      # 啟動 shell
poetry run python main.py        # 直接執行

# 使用虛擬環境路徑
poetry env info                  # 顯示環境資訊
poetry env use python3.9         # 指定 Python 版本
```

### 建構和發布

```bash
# 建構 distribution
poetry build

# 發布到 PyPI
poetry publish

# 發布到私有倉庫
poetry publish --repo myrepo
```

## 比較與選擇

### 功能比較

| 功能 | pip | Pipenv | Poetry |
|------|-----|--------|--------|
| 環境隔離 | 需要 venv | 自動 | 自動 |
| 依賴鎖定 | pip freeze | Pipfile.lock | poetry.lock |
| 格式標準 | requirements.txt | Pipfile (TOML) | pyproject.toml |
| 專案打包 | 手動 | 手動 | 原生支援 |
| 依賴解析 | 一般 | 嚴格 | 嚴格 |
| 學習曲線 | 低 | 中 | 中 |

### 選擇建議

**選擇 pip + venv**：
- 簡單腳本和小型專案
- 已有 requirements.txt 的老專案
- 需要最大相容性

**選擇 Pipenv**：
- 想要統一的環境和依賴管理
- 喜歡 Pipfile 的語法
- 需要與 Django/Flask 整合

**選擇 Poetry**：
- 發布開源套件到 PyPI
- 需要完整的專案管理
- 想要現代化的開發體驗

## 延伸閱讀

- [Pipenv 官方文件](https://www.google.com/search?q=Pipenv+Python+official+documentation)
- [Poetry 官方文件](https://www.google.com/search?q=Poetry+Python+official+documentation)
- [Python Packaging User Guide](https://www.google.com/search?q=Python+Packaging+User+Guide+PyPA)
- [pipenv vs poetry comparison](https://www.google.com/search?q=pipenv+vs+poetry+2020)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」文章集錦之一。*