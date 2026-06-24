# uv：超高速 Python 套件管理

## 前言

uv 是由 Astral 公司（Rust Python 工具鏈的幕後團隊）開發的超高速 Python 套件管理器。它用 Rust 編寫，安裝速度比 pip 快 10-100 倍，記憶體佔用也更少。

## uv 的誕生背景

### 傳統工具的瓶頸

pip 和其他傳統 Python 工具在處理大型專案時常遇到效能問題：

```
工具比較：
────────────────────────────────

pip：    依賴解析慢，大型專案可能需要幾分鐘
poetry： 功能豐富，但速度較慢
pipenv： 環境管理優秀，但有時不穩定

uv：
  ├── 安裝速度：比 pip 快 10-100 倍
  ├── 依賴解析：智慧且快速
  ├── 記憶體佔用：顯著較低
  └── 跨平台：支援所有主流平台
```

## 安裝和基本使用

### 安裝 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv
```

### 基本指令

```bash
# 安裝套件
uv pip install requests
uv pip install "requests>=2.25"
uv pip install -r requirements.txt

# 創建虛擬環境
uv venv myproject
uv venv myproject --python 3.8

# 啟動環境
source myproject/bin/activate

# 同步依賴
uv pip sync requirements.txt

# 凍出依賴
uv pip freeze > requirements.txt
```

## 與現有專案整合

### requirements.txt 的無縫接軌

```bash
# 從現有的 requirements.txt 安裝
uv pip install -r requirements.txt

# 如果有 Pipfile
uv pip install pipenv

# 如果有 pyproject.toml
uv pip install poetry
```

### 建立新專案

```bash
# 建立新專案（使用互動式引導）
uv init myproject

# 建立只含依賴的專案
uv init --lib myproject

# 在現有目錄初始化
uv init
```

## uv 的核心功能

### 快速安裝

```bash
# 測量效能
time uv pip install flask

# vs pip
time pip install flask
```

### 依賴管理

```bash
# 安裝時自動更新 pip 和 setuptools
uv pip install --upgrade pip setuptools wheel

# 指定版本
uv pip install "django>=3.2,<4.0"

# 安裝多個套件
uv pip install requests flask sqlalchemy
```

### 虛擬環境管理

```bash
# 建立環境
uv venv myenv

# 指定 Python 版本
uv venv myenv --python 3.8
uv venv myenv --python 3.9
uv venv myenv --python 3.10

# 快速啟動
source myenv/bin/activate

# 清理
uv venv myenv --quiet
```

## 使用 Python 版本管理

uv 內建 Python 版本管理功能：

```bash
# 安裝 Python
uv python install 3.8
uv python install 3.9
uv python install 3.10

# 列出已安裝的 Python
uv python list

# 在專案中使用特定版本
uv venv myenv --python 3.8
```

## 與 GitHub Actions 整合

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      
      - name: Set up Python
        run: uv python install 3.8
      
      - name: Install dependencies
        run: uv pip install --python 3.8 -r requirements.txt
      
      - name: Run tests
        run: pytest
```

## uv 的設計理念

### Rust 的威力

uv 使用 Rust 編寫，這帶來了：

```
Rust 带來的優勢：
────────────────────────────────

1. 記憶體安全：沒有 GC 暫停
2. 併發：充分利用多核心
3. 效能：接近 C 的執行速度
4. 小的二進位制：分發方便
```

### 與現有工具的相容性

uv 並非要取代 pip，而是提供一個更快的替代方案：

- 完全相容 requirements.txt 格式
- 可以與 pip 混合使用
- 逐步遷移，風險低

## 未來展望

uv 的發展方向：

```
即將到來的功能：
────────────────────────────────

1. uv publish：發布套件到 PyPI
2. uv run：在不預先安裝的情況下執行腳本
3. 更好的 IDE 整合
4. 更多的平台支援
```

## 延伸閱讀

- [uv 官方網站](https://www.google.com/search?q=uv+Python+package+manager+astral)
- [uv GitHub 倉庫](https://www.google.com/search?q=uv+GitHub+repository+Rust+Python)
- [Astral 公司](https://www.google.com/search?q=Astral+Python+tools+Rust)
- [Python 套件管理器比較](https://www.google.com/search?q=Python+package+manager+comparison+2020)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」文章集錦之一。*