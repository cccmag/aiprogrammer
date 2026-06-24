# 檔案上傳安全

## 檔案上傳的風險

檔案上傳功能如果沒有妥善的安全措施，可能導致：
- 惡意檔案執行（Web Shell 上傳）
- 服務阻斷（超大檔案）
- 目錄穿越（覆寫系統檔案）
- XSS（透過 HTML 檔案的 script 執行）

## 副檔名驗證

### 黑名單（不安全）

```python
# 不安全：攻擊者可使用 .php5、.phtml 等
blocked_extensions = ['php', 'php3', 'php4', 'phtml']
if ext in blocked_extensions:
    raise ValueError("File type not allowed")
```

### 白名單（安全）

```python
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

## MIME 類型驗證

不僅檢查副檔名，還要驗證檔案的實際 MIME 類型：

```python
import magic

def verify_file_type(file_storage):
    # 讀取檔案頭部來判斷實際類型
    with open(file_storage.stream, 'rb') as f:
        header = f.read(2048)

    mime = magic.from_buffer(header, mime=True)

    allowed_mimes = {
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }

    if mime not in allowed_mimes:
        raise ValueError(f"File type {mime} not allowed")
```

## 檔案重新命名

不要使用使用者提供的檔案名稱：

```python
import os
import uuid
import secrets

def secure_filename(original_filename):
    # 取得副檔名
    ext = original_filename.rsplit('.', 1)[1].lower()
    # 產生安全的隨機檔案名稱
    new_filename = f"{uuid.uuid4().hex}{secrets.token_hex(8)}.{ext}"
    return new_filename
```

## 儲存位置隔離

將上傳的檔案儲存在 Web 根目錄之外，或使用 Object Storage：

```python
# Flask 範例
import os

UPLOAD_FOLDER = '/var/app/uploads'  # 不在靜態檔案目錄下
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 限制

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
```

## 執行權限控制

確保上傳目錄與檔案沒有執行權限：

```bash
# 設定目錄權限
chmod 755 /var/app/uploads

# 設定檔案權限
chmod 644 /var/app/uploads/*
```

## 圖片額外處理

對於圖片，可以重新編碼以移除潜在的惡意內容（如 polyglot 檔案）：

```python
from PIL import Image
import io

def sanitize_image(file_storage):
    try:
        image = Image.open(file_storage.stream)
        image.verify()  # 驗證是有效的圖片

        # 重新編碼圖片
        output = io.BytesIO()
        image = Image.open(file_storage.stream)
        image.save(output, format=image.format or 'PNG')
        return output.getvalue()
    except Exception as e:
        raise ValueError(f"Invalid image: {e}")
```

## 大小限制

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify(error="File too large"), 413
```

## 病毒掃描

對於高風險場景，可以使用 ClamAV 進行病毒掃描：

```python
import pyclamd

def scan_uploaded_file(filepath):
    cd = pyclamd.ClamdAgnostic()
    result = cd.scan_file(filepath)
    if result:
        raise ValueError(f"Malware detected: {result}")
    return True
```

## 完整範例

```python
import os
import uuid
import magic
from werkzeug.utils import secure_filename as werkzeug_secure

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf'}
UPLOAD_FOLDER = '/var/app/uploads'

def save_upload(file_storage):
    # 1. 檢查副檔名
    if '.' not in file_storage.filename:
        raise ValueError("No file extension")
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("File type not allowed")

    # 2. 驗證 MIME 類型
    header = file_storage.stream.read(2048)
    file_storage.stream.seek(0)
    mime = magic.from_buffer(header, mime=True)

    allowed_mimes = {'image/jpeg', 'image/png', 'image/gif', 'application/pdf'}
    if mime not in allowed_mimes:
        raise ValueError("MIME type not allowed")

    # 3. 安全的檔案名稱
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # 4. 儲存檔案
    file_storage.save(filepath)

    return filename
```

## 參考資源

- https://www.google.com/search?q=檔案上傳+安全+漏洞+防護+副檔名+MIME+2016
- https://www.google.com/search?q=Web+Shell+上傳+防護+檔案+驗證+白名單+重新命名
- https://www.google.com/search?q=圖片+安全+處理+PIL+重新編碼+polyglot+攻擊