# 2. 虛擬環境管理

## 為什麼需要虛擬環境？

虛擬環境是 Python 開發的基礎設施。它讓每個專案擁有獨立的套件安裝空間，避免全域 Python 環境被汙染。假設專案 A 需要 Django 2.2，專案 B 需要 Django 3.0，若沒有虛擬環境，安裝新版本會破壞舊專案的相依性。

## venv：標準庫內建

Python 3.3 之後，`venv` 是內建的虛擬環境模組，無需額外安裝。

```bash
# 建立虛擬環境
python3 -m venv myenv

# 啟動（Linux/macOS）
source myenv/bin/activate

# 啟動（Windows）
# myenv\Scripts\activate.bat

# 確認環境
which python3  # 應顯示 myenv/bin/python3
pip --version  # 應顯示 myenv 中的 pip

# 停用
deactivate
```

## virtualenv：更強大的選擇

virtualenv 提供了 venv 沒有的功能：
- 可指定 Python 版本（不限定於已安裝的版本）
- 更好的相容性（某些 edge cases）
- 較快的建立速度

```bash
# 安裝
pip install virtualenv

# 建立（使用特定 Python 版本）
virtualenv -p python3.8 myenv

# 包含系統已安裝的套件
virtualenv --system-site-packages myenv

# 建立時指定 site-packages 位置
virtualenv --extra-search-dir=/path/to/packages myenv
```

## pyenv-virtualenv：版本與環境一體管理

pyenv 是 Python 版本管理器，結合 pyenv-virtualenv 可以同時管理 Python 版本與虛擬環境。

```bash
# 安裝 pyenv 與 pyenv-virtualenv
brew install pyenv pyenv-virtualenv

# 加入 shell 設定
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv-virtualenv-init -)"' >> ~/.zshrc
source ~/.zshrc

# 安裝 Python 版本
pyenv install 3.7.6
pyenv install 3.8.1

# 建立虛擬環境
pyenv virtualenv 3.8.1 my-project

# 啟用（在目錄中自動啟用）
pyenv local my-project

# 手動啟用/停用
pyenv activate my-project
pyenv deactivate
```

## 環境變數與 .gitignore

虛擬環境目錄應加入 `.gitignore`：

```
# .gitignore
venv/
.venv/
env/
.env
myenv/
```

建議將環境依賴匯出到檔案中：

```bash
# 匯出環境套件
pip freeze > requirements.txt

# 或使用 pipreqs（只匯入實際使用的套件）
pip install pipreqs
pipreqs . --force
```

## 使用虛擬環境的最佳實踐

1. **為每個專案建立獨立環境**：不要多個專案共享同一環境
2. **記錄 Python 版本**：在 `.python-version` 或 `runtime.txt` 中記錄
3. **定期更新依賴**：使用 `pip list --outdated` 檢查更新
4. **測試環境重現**：刪除環境後用 requirements.txt 重建，確認一切正常

## 參考資源

- https://www.google.com/search?q=Python+venv+virtualenv+virtual+environment+tutorial+2020
- https://www.google.com/search?q=pyenv+virtualenv+Python+version+management+workflow+2020
- https://www.google.com/search?q=Python+virtual+environment+best+practices+requirements+isolation