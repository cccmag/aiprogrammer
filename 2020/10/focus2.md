# virtualenv 與 conda：Python 環境隔離方案

## 為什麼需要環境隔離？

### 情境問題

假設你有兩個專案：

```bash
# 專案 A 需要 Django 2.2
# 專案 B 需要 Django 3.1

# 如果安裝在同一個環境會發生什麼？
$ pip install django==2.2
$ pip install django==3.1
# Django 3.1 會覆蓋 2.2
# 專案 A 可能無法正常運作！
```

### 環境隔離的解決方案

```
未隔離：                    隔離後：
┌──────────────────────┐   ┌─────────────┐  ┌─────────────┐
│  系統 Python         │   │  環境 A     │  │  環境 B     │
│  Django 3.1          │   │  Django 2.2 │  │  Django 3.1 │
│  requests 2.24       │   │  requests   │  │  numpy      │
│  numpy 1.19          │   │  (其他套件) │  │  (其他套件) │
└──────────────────────┘   └─────────────┘  └─────────────┘
```

每個專案都有自己獨立的 Python 環境，互不干擾。

## virtualenv

### 建立和使用

virtualenv 是 Python 官方推薦的環境隔離工具：

```bash
# 安裝 virtualenv
pip install virtualenv

# 建立虛擬環境
python -m venv myproject-env

# 啟動虛擬環境
# Linux/macOS:
source myproject-env/bin/activate

# Windows:
myproject-env\Scripts\activate

# 停用虛擬環境
deactivate
```

### 工作原理

virtualenv 透過建立一個獨立的 Python 副本來實現環境隔離：

```
myproject-env/
├── bin/           # 可執行檔（python, pip）
├── include/       # C 標頭檔
├── lib/           # Python 函式庫副本
│   └── python3.8/
│       └── site-packages/  # 這個環境的套件
└── pyvenv.cfg     # 環境配置
```

### virtualenvwrapper

virtualenvwrapper 是一個 virtualenv 的擴展，簡化了環境管理：

```bash
# 安裝
pip install virtualenvwrapper

# 建立環境（自動在工作目錄管理）
mkvirtualenv myproject

# 切換環境
workon myproject

# 停用
deactivate

# 列出所有環境
lsvirtualenv

# 刪除環境
rmvirtualenv myproject
```

## conda

### conda 的獨特之處

conda 不僅能管理 Python 套件，還能管理其他語言和系統庫：

```bash
# 建立 conda 環境
conda create --name myproject python=3.8

# 啟動環境
conda activate myproject

# 安裝 Python 套件
conda install numpy pandas

# 安裝非 Python 套件
conda install cmake boost

# 導出環境配置
conda env export > environment.yml

# 從配置檔建立環境
conda env create -f environment.yml
```

### conda 與 pip 的比較

| 特性 | pip | conda |
|------|-----|-------|
| 套件類型 | Python 套件 | 任何語言/系統庫 |
| 環境隔離 | 需要 virtualenv | 原生支援 |
| 依賴解析 | 較弱（新版本改進） | 更嚴格 |
| 預設頻道 | PyPI | conda-forge/Anaconda |
| 記憶體使用 | 較少 | 較多 |

### conda 環境檔案

```yaml
# environment.yml
name: myproject
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.8
  - numpy=1.19
  - pandas=1.1
  - pip
  - pip:
    - some-pip-only-package
```

## Pipenv 與 Poetry

### Pipenv：統一管理

Pipenv 試圖同時管理環境和依賴：

```bash
# 安裝
pip install pipenv

# 建立專案（自動建立虛擬環境）
pipenv install requests

# 進入 shell
pipenv shell

# 安裝開發依賴
pipenv install --dev pytest

# 鎖定依賴
pipenv lock

# 執行腳本（不使用 shell）
pipenv run python main.py
```

### Poetry：現代 Python 打包

Poetry 提供了現代化的 Python 專案管理：

```bash
# 安裝
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# 建立新專案
poetry new myproject
cd myproject

# 新增依賴
poetry add requests
poetry add --dev pytest

# 安裝依賴
poetry install

# 鎖定版本
poetry lock

# 更新依賴
poetry update
```

## 選擇適合的工具

### 建議

**新手**：從 `python -m venv` 開始，這是 Python 3.3+ 的內建功能

**資料科學家**：考慮使用 conda，特別是需要安裝非 Python 依賴時

**現代化專案**：Pipenv 或 Poetry 提供了更好的開發體驗

**大規模專案**：虛擬環境 + requirements.txt 仍然是穩定的選擇

## 延伸閱讀

- [Python venv 模組文件](https://www.google.com/search?q=Python+venv+module+documentation)
- [virtualenv 使用指南](https://www.google.com/search?q=virtualenv+Python+tutorial)
- [conda vs pip comparison](https://www.google.com/search?q=conda+vs+pip+Python+comparison)
- [Pipenv 使用指南](https://www.google.com/search?q=Pipenv+Python+dependency+management)
- [Poetry 官方文件](https://www.google.com/search?q=Poetry+Python+packaging+tool)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」歷史回顧系列之一。*