# PyPI 私人套件

## 為什麼需要私人套件？

當多個專案共享相同程式碼，或有不能公開的商業邏輯時，需要私人套件。

## 使用私有 PyPI

### 1. 設定 pip

```bash
# pip.conf
[global]
index-url = https://my-private-pypi.com/simple
trusted-host = my-private-pypi.com
```

### 2. 安裝私人套件

```bash
pip install my-private-package

# 或明確指定來源
pip install --index-url=https://my-private-pypi.com/simple my-package
```

### 3. 使用 .pypirc

```ini
# ~/.pypirc
[distutils]
index-servers = pypi, mypypi

[mypypi]
repository = https://my-private-pypi.com/simple
username = myuser
password = mypassword
```

## 從 Git 安裝

```bash
# 公開 repository
pip install git+https://github.com/user/repo.git

# 私人 repository（需要 token）
pip install git+https://TOKEN@github.com/user/repo.git

# 特定分支/標籤
pip install git+https://github.com/user/repo.git@main
pip install git+https://github.com/user/repo.git@v1.0.0
```

## 簡單的私人套件伺服器

### 1. pypiserver

```bash
pip install pypiserver

# 啟動伺服器
pypi-server -p 8080 ./packages &

# 上傳套件
pip install twine
python setup.py sdist upload -r mypypi
```

### 2. DevPI

```bash
pip install devpi
devpi-server &
devpi use http://localhost:3141
devpi login root
devpi package index myindex
```

## 發布私人套件

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="my-package",
    version="0.1.0",
    packages=find_packages(),
)
```

```bash
# 建置與發布
python setup.py sdist bdist_wheel
twine upload --repository mypypi dist/*
```

## 參考資源

- https://www.google.com/search?q=private+PyPI+Python+package+server+tutorial+2020
- https://www.google.com/search?q=install+private+GitHub+package+pip+token+2020
- https://www.google.com/search?q=pypiserver+devpi+private+Python+package+hosting