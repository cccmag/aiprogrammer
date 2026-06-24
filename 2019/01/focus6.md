# 6. 開發工具鏈

## Python 開發工具生態系

Python 3.7 時代的開發工具鏈已相當成熟。從編輯器到除錯工具，從測試框架到部署系統，Python 提供了完整的開發體驗。

## IDE 與編輯器

### Visual Studio Code

```bash
# 安裝 Python 擴充
code --install-extension ms-python.python

# 設定 Python 路徑
# Ctrl+Shift+P -> Python: Select Interpreter
```

### PyCharm

PyCharm 專業版提供：
- 即時型態檢查
- 遠端除錯
- Django/Flask 支援
- 資料庫整合

### Jupyter Notebook/Lab

```bash
pip install jupyterlab
jupyter lab
```

## 除錯工具

### breakpoint()

Python 3.7 引入了 `breakpoint()` 函數：

```python
def buggy_function(x):
    result = x * 2
    breakpoint()  # Python 3.7+ 使用方便
    return result
```

### pdb 基本指令

```
pdb 指令：
- n (next): 執行下一行
- s (step): 進入函數
- c (continue): 繼續執行
- p (print): 顯示變數
- l (list): 顯示周圍程式碼
```

### ipdb

```bash
pip install ipdb

import ipdb
ipdb.set_trace()
```

## 測試框架

### pytest

```bash
pip install pytest
pytest tests/
```

```python
# test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"
```

### unittest

```python
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()
```

## 程式碼品質工具

### Black 格式化

```bash
pip install black
black my_project.py
```

### mypy 型態檢查

```bash
pip install mypy
mypy my_project.py
```

### flake8 程式碼檢查

```bash
pip install flake8
flake8 my_project.py
```

## 環境管理

### venv

```bash
python3 -m venv myenv
source myenv/bin/activate  # Linux/macOS
myenv\Scripts\activate     # Windows
```

### pipenv

```bash
pip install pipenv
pipenv install requests
pipenv shell
```

## 虛擬環境範例

```python
# check_env.py
import sys
import os

def demo():
    print("Python 版本：", sys.version)
    print("目前環境：", "虛擬環境" if sys.prefix != sys.base_prefix else "全域環境")
    print("環境路徑：", sys.prefix)

if __name__ == "__main__":
    demo()
```

## 參考資源

- https://www.google.com/search?q=Python+development+tools+2019+IDE+VSCode+PyCharm+Debugger
- https://www.google.com/search?q=Python+testing+pytest+unittest+tutorial+2019
- https://www.google.com/search?q=Python+code+quality+black+mypy+flake8+2019+best+practices