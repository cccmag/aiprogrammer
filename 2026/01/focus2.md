# 2. Python 虛擬環境管理

## 為什麼需要虛擬環境？

Python 的全域套件安裝會導致嚴重的版本衝突。假設專案 A 需要 Django 3.2，專案 B 需要 Django 4.0，若安裝在全域環境中只能存在一個版本。這個問題在 AI 領域更為嚴峻，因為深度學習框架對版本極度敏感。虛擬環境為每個專案建立獨立的 Python 直譯器與套件目錄，從根本上解決版本衝突問題。

## 常見方案

### venv（內建）
Python 3.3 以上版本內建的虛擬環境模組，輕量且無需額外安裝。這是官方推薦的方式，適合大多數場景。

```bash
# 建立虛擬環境
python -m venv myenv

# 啟動（Linux/macOS）
source myenv/bin/activate

# 啟動（Windows）
myenv\\Scripts\\activate

# 離開
deactivate
```

### virtualenv
venv 的前身，支援 Python 2，功能更豐富，包含更快的套件安裝速度與更友善的錯誤訊息。

```bash
pip install virtualenv
virtualenv myenv -p python3.10
```

### pyenv
管理多個 Python 版本的絕佳工具，可與 virtualenv 搭配使用。在切換 Python 版本的同時建立對應的虛擬環境，對於需要測試不同 Python 版本的專案非常實用。

```bash
pyenv install 3.11.7
pyenv virtualenv 3.11.7 myproject
pyenv activate myproject
```

## 最佳實踐

- 每個專案使用獨立的虛擬環境
- 將依賴清單寫入 `requirements.txt` 或 `environment.yml`
- 虛擬環境目錄不納入版本控制（加入 `.gitignore`）
- 虛擬環境名稱建議與專案名稱一致，便於識別

## 判斷是否在虛擬環境中

```python
import sys
in_venv = sys.prefix != sys.base_prefix
print(f"在虛擬環境中: {in_venv}")
print(f"環境路徑: {sys.prefix}")
```

## 參考資源

- https://www.google.com/search?q=Python+virtual+environment+venv+virtualenv+tutorial+guide
- https://www.google.com/search?q=pyenv+virtualenv+Python+version+management+setup+workflow
- https://www.google.com/search?q=Python+venv+best+practices+requirements+gitignore
