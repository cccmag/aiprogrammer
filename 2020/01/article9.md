# 跨平台環境建置

## 主要挑戰

- 路徑分隔符（Windows `\` vs Unix `/`）
- 環境變數名稱差異
- 原生擴充編譯相依
- 換行符號（CRLF vs LF）

## 使用 Docker 確保一致性

Docker 可以在任何平台上提供一致的 Linux 環境：

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
# 建置與執行
docker build -t myapp .
docker run myapp
```

## 使用 Poetry/Pipenv

這些工具自動處理跨平台差異：

```bash
# 在 macOS 建置
poetry lock
poetry export -f requirements.txt --without-hashes > requirements.txt

# 在 Linux 使用相同檔案建置
pip install -r requirements.txt
```

## 路徑處理

```python
from pathlib import Path
import os

# 正確處理跨平台路徑
data_dir = Path(__file__).parent / "data"
config_path = data_dir / "config.json"

# 使用 os.path（自動處理）
config_path = os.path.join(os.path.dirname(__file__), "data", "config.json")
```

## 環境變數

```python
import os

# 跨平台環境變數讀取
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
```

## 原生擴充

Windows 上需要 Visual Studio Build Tools：

```bash
# Windows
pip install numpy  # 會自動下載預編譯 wheel

# macOS/Linux
pip install numpy
```

## CI/CD 跨平台測試

GitHub Actions：

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.7, 3.8]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v1
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest
```

## 參考資源

- https://www.google.com/search?q=Python+cross+platform+environment+Windows+macOS+Linux+2020
- https://www.google.com/search?q=Python+Docker+cross+platform+development+2020
- https://www.google.com/search?q=Python+path+handling+cross+platform+compatibility