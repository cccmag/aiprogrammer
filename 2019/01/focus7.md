# 7. 遷移與相容性

## 從 Python 3.6 遷移到 3.7

Python 3.7 的相容性大多良好，但有一些需要注意的破壞性改變。本章節幫助開發者順利遷移。

## 破壞性改變

### async/await 成為保留關鍵字

```python
# Python 3.5 之前可以這樣使用
# async = 1  # SyntaxError in Python 3.7+
```

### collections.abc 匯入

```python
# 舊寫法（Python 3.6）
from collections import Mapping, MutableMapping

# 新寫法（Python 3.7+）
from collections.abc import Mapping, MutableMapping
```

### numpy 型態別名移除

```python
# numpy 使用者需要注意
import numpy as np

# Python 3.7+ 需要使用標準類型
arr = np.array([1, 2, 3])
# arr.dtype 可以是 np.int64，但不是 np.int
```

## 向後相容策略

### __future__ 匯入

```python
from __future__ import annotations
# 允許使用尚未成為預設的語法
```

### 依賴版本檢查

```python
import sys

if sys.version_info < (3, 7):
    raise RuntimeError("需要 Python 3.7 或更高版本")
```

### 環境偵測

```python
import sys
import platform

def check_python_version():
    print(f"Python 版本：{sys.version}")
    print(f"平台：{platform.platform()}")
    print(f"實作：{platform.python_implementation()}")

    if sys.version_info >= (3, 7):
        print("✓ 版本相容")
    else:
        print("✗ 需要升級到 Python 3.7+")

check_python_version()
```

## 測試策略

### 自動化測試

```bash
# 執行測試
python -m pytest tests/

# 版本特定測試
python -m pytest tests/ -v
```

### CI/CD 整合

```yaml
# .github/workflows/test.yml
name: Test
runs-on: ubuntu-latest
strategy:
  matrix:
    python-version: [3.6, 3.7, 3.8]
steps:
  - uses: actions/checkout@v2
  - name: Setup Python
    uses: actions/setup-python@v2
    with:
      python-version: ${{ matrix.python-version }}
  - name: Run tests
    run: |
      pip install -r requirements.txt
      pytest tests/
```

## 遷移檢查清單

1. 更新 requirements.txt 中的 Python 版本要求
2. 檢查第三方套件是否支援 Python 3.7
3. 執行完整測試確保功能正常
4. 檢視 DeprecationWarning
5. 更新 Dockerfile 與部署腳本

## 常見問題

### ImportError

```python
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping  # 向後相容
```

### SyntaxError

```python
# 檢查是否有使用 async 作為變數名
import ast
import sys

code = "async = 1"
try:
    ast.parse(code)
except SyntaxError as e:
    print(f"語法錯誤：{e}")
```

## 參考資源

- https://www.google.com/search?q=Python+3.6+to+3.7+migration+guide+breaking+changes+2019
- https://www.google.com/search?q=Python+3.7+compatibility+collections.abc+numpy+deprecation
- https://www.google.com/search?q=Python+migration+testing+CI+CD+best+practices+2019