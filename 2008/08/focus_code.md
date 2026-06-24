# 效能優化程式實作

## Gzip 壓縮

```python
import gzip
import io

def compress_content(content):
    """壓縮內容"""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(content.encode('utf-8'))
    return buf.getvalue()

def decompress_content(compressed):
    """解壓縮內容"""
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as f:
        return f.read().decode('utf-8')
```

## 快取示範

```python
import time
from functools import wraps

def memoize(expire=300):
    """記憶化裝飾器"""
    cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            key = (func.__name__, args)
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < expire:
                    return result
            result = func(*args)
            cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

@memoize(expire=3600)
def expensive_operation(n):
    """昂貴的運算"""
    return sum(range(n))
```

## 資源合併

```python
def merge_files(filepaths):
    """合併多個檔案"""
    contents = []
    for path in filepaths:
        with open(path, 'r') as f:
            contents.append(f.read())
    return '\n'.join(contents)
```

## 圖片優化提示

```python
# 圖片優化建議（概念）
image_optimization_tips = [
    '使用 JPEG 而非 PNG（對於照片）',
    '使用 PNG8 而非 PNG24（對於圖示）',
    '壓縮圖片至 80% 品質',
    '使用 CSS Sprite 合併小圖',
    '延遲載入非必要圖片'
]
```

## 參考資源

- [YSlow+rules](https://www.google.com/search?q=YSlow+14+rules)
- [Web+performance+optimization](https://www.google.com/search?q=web+performance+optimization+tools)