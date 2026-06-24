# venv 與 virtualenv

## 選擇建議

- **venv**：Python 3.3+ 內建，無需額外安裝，適合大多數場景
- **virtualenv**：功能更完整，支援自訂 Python 版本，適合進階用戶
- **pyenv-virtualenv**：版本管理與虛擬環境一體，適合管理多個 Python 版本

## venv 實戰

```bash
# 建立虛擬環境
python3 -m venv myenv

# 啟動（Linux/macOS）
source myenv/bin/activate

# 啟動（Windows PowerShell）
myenv\Scripts\Activate.ps1

# 啟動（Windows CMD）
myenv\Scripts\activate.bat

# 確認環境
which python3  # 應該顯示 myenv/bin/python3

# 停用
deactivate
```

## virtualenv 實戰

```bash
# 安裝
pip install virtualenv

# 基本使用
virtualenv myenv
source myenv/bin/activate

# 使用特定 Python 版本
virtualenv -p python3.8 myenv

# 包含系統 site-packages
virtualenv --system-site-packages myenv

# 列出所有虛擬環境
ls ~/.virtualenvs
```

## pyenv-virtualenv 整合

```bash
# macOS 安裝
brew install pyenv pyenv-virtualenv

# 設定 shell
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv-virtualenv-init -)"' >> ~/.zshrc
source ~/.zshrc

# 使用流程
pyenv install 3.8.1
pyenv virtualenv 3.8.1 my-project
pyenv activate my-project
pyenv deactivate
```

## 環境管理腳本

建立一個 `env.sh` 方便切換：

```bash
#!/bin/bash
# env.sh

function myenv() {
    if [ -z "$1" ]; then
        # 列出環境
        ls ~/.venvs 2>/dev/null || echo "No environments"
        return
    fi

    case "$1" in
        create)
            python3 -m venv .venv
            source .venv/bin/activate
            ;;
        activate)
            source .venv/bin/activate
            ;;
        deactivate)
            deactivate
            ;;
    esac
}
```

## 常見問題

1. **Permission denied**：使用 `sudo` 或建立虛擬環境，不要用全域安裝
2. **找不到 python**：確認環境已啟動（prompt 前會顯示環境名稱）
3. **pip 版本過舊**：在虛擬環境中執行 `pip install --upgrade pip`

## 參考資源

- https://www.google.com/search?q=venv+virtualenv+Python+virtual+environment+tutorial+2020
- https://www.google.com/search?q=pyenv+virtualenv+Python+version+management+macOS+Linux
- https://www.google.com/search?q=Python+virtual+environment+best+practices+isolated+2020