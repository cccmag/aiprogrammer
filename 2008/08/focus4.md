# 資源壓縮與合併

## Gzip 壓縮

### 伺服器配置

```apache
# Apache .htaccess
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE text/javascript
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/json
</IfModule>
```

### Nginx 配置

```nginx
# Nginx 配置
gzip on;
gzip_types text/css application/javascript application/json;
gzip_comp_level 6;
```

## JavaScript/CSS 合併

### 合併策略

```python
# 合併 CSS
def merge_css(filepaths, output_path):
    """合併多個 CSS 檔案"""
    content = []
    for path in filepaths:
        with open(path, 'r') as f:
            content.append(f.read())
    with open(output_path, 'w') as f:
        f.write('\n'.join(content))
```

### 預處理器

```python
# 使用 Less 編譯
# lessc style.less style.css
```

## 圖片優化

### 工具

```python
image_optimization = {
    'jpeg': 'jpegoptim, mozjpeg',
    'png': 'pngquant, optipng',
    'svg': 'svgo',
    'gif': 'gifsicle'
}
```

### 自動化

```python
# 自動化圖片優化腳本
import os
import subprocess

def optimize_images(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            subprocess.run(['jpegoptim', '--strip-all', filename])
        elif filename.endswith('.png'):
            subprocess.run(['pngquant', '--force', filename])
```

## 結論

壓縮和合併是減少 HTTP 請求和傳輸大小的有效方法。

---

**延伸閱讀**

- [資源壓縮與合併](https://www.google.com/search?q=minify+javascript+css+tools)