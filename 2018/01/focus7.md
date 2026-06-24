# Python 3.6 生態系總覽

## 簡介

Python 3.6 發布後，生態系快速成熟。眾多熱門套件已全面支援 Python 3.6，本篇介紹 2018 年 1 月最具價值的 Python 3.6 生態系工具與套件。

## 核心工具

### pip 與 virtualenv

```bash
pip install virtualenv
python -m venv myenv
source myenv/bin/activate
pip install --upgrade pip
```

### poetry（新一代套件管理）

```bash
pip install poetry
poetry init
poetry add requests
poetry install
```

## Web 開發

### Django 2.1

```bash
pip install Django>=2.1
django-admin startproject mysite
```

### Flask 1.1

```bash
pip install Flask>=1.1
```

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

app.run()
```

### FastAPI

```bash
pip install fastapi uvicorn
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

## 資料科學

### NumPy

```bash
pip install numpy
```

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)  # [2, 4, 6, 8, 10]
```

### Pandas

```bash
pip install pandas
```

```python
import pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
print(df.describe())
```

### Matplotlib

```bash
pip install matplotlib
```

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])
plt.savefig("plot.png")
```

## 機器學習

### TensorFlow

```bash
pip install tensorflow>=1.5
```

```python
import tensorflow as tf

hello = tf.constant("Hello, TensorFlow!")
sess = tf.Session()
print(sess.run(hello))
```

### Keras

```python
import keras

model = keras.Sequential([
    keras.layers.Dense(10, activation='relu', input_shape=(784,)),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy')
```

### PyTorch

```bash
pip install torch
```

```python
import torch

x = torch.rand(5, 3)
print(x)
```

## 異步程式設計

### aiohttp

```bash
pip install aiohttp
```

```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### aiomysql

```bash
pip install aiomysql
```

## 測試

### pytest

```bash
pip install pytest
```

```python
def test_example():
    assert 1 + 1 == 2
```

```bash
pytest test_example.py
```

### tox

```bash
pip install tox
```

```ini
[tox]
envlist = py36,py37
```

## 程式碼品質

### black（格式化）

```bash
pip install black
black your_module.py
```

### flake8（Lint）

```bash
pip install flake8
flake8 your_module.py
```

### mypy（型別檢查）

```bash
pip install mypy
mypy your_module.py
```

## 開發環境

### Jupyter Notebook

```bash
pip install jupyter notebook
jupyter notebook
```

### IPython

```bash
pip install ipython
ipython
```

## 部署工具

### gunicorn

```bash
pip install gunicorn
gunicorn -w 4 app:app
```

### uvicorn

```bash
pip install uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
```

### docker

```dockerfile
FROM python:3.6-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 推荐的 requirements.txt

```
# 核心
numpy>=1.14
pandas>=0.22
matplotlib>=2.2

# 機器學習
# tensorflow>=1.5
# keras>=2.1

# Web
# fastapi>=0.3
# uvicorn>=0.4

# 工具
pytest>=3.5
black>=18.0
mypy>=0.6
```

## 總結

Python 3.6 生態系已相當成熟，從 Web 開發到資料科學、機器學習，都有豐富的支援。建議新專案使用 Python 3.6 或更新版本，以獲得最佳的工具鏈支援。