# pyenv 與 virtualenv

## 安裝 pyenv

pyenv 讓你在同一台機器上安裝與切換多個 Python 版本，是 AI 專案中處理不同框架 Python 版本需求的利器。

```bash
# macOS
brew install pyenv

# Linux
curl https://pyenv.run | bash

# 加入 shell 設定（zsh）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 重新載入設定
source ~/.zshrc
```

## 基本操作

```bash
# 查看可安裝的 Python 版本
pyenv install --list

# 安裝指定版本
pyenv install 3.11.7

# 設定全域 Python 版本（所有 shell 的預設版本）
pyenv global 3.11.7

# 設定專案本地版本（在目錄中寫入 .python-version）
cd myproject
pyenv local 3.10.12
```

## pyenv-virtualenv 整合

pyenv-virtualenv 是 pyenv 的外掛，讓虛擬環境管理與 Python 版本管理統一。

```bash
# 安裝外掛（macOS）
brew install pyenv-virtualenv

# 建立虛擬環境（基於特定 Python 版本）
pyenv virtualenv 3.11.7 myenv

# 啟用虛擬環境
pyenv activate myenv

# 離開虛擬環境
pyenv deactivate

# 設定目錄自動啟用（進入目錄自動切換）
pyenv local myenv
```

## 使用場景

假設你同時維護兩個 AI 專案：專案 A 需要 Python 3.10 與 TensorFlow 2.13，專案 B 需要 Python 3.11 與 PyTorch 2.1。使用 pyenv 可以輕鬆切換：

```bash
# 專案 A
cd project_a
pyenv local 3.10.12
python -m venv .venv
source .venv/bin/activate
pip install tensorflow==2.13

# 專案 B
cd project_b
pyenv local 3.11.7
python -m venv .venv
source .venv/bin/activate
pip install torch==2.1.0
```

## 參考資源

- https://www.google.com/search?q=pyenv+virtualenv+Python+version+management+tutorial+2026
- https://www.google.com/search?q=pyenv+install+multiple+Python+versions+switch+guide
- https://www.google.com/search?q=pyenv+virtualenv+plugin+workflow+best+practices
