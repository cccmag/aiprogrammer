# 雲端儲存客戶端實作

## 概述

本程式實作了一個 S3 風格的雲端儲存 API，模擬了基本的儲存桶操作和檔案管理功能。

## 核心類別

### CloudStorage

主要的儲存客戶端類別，提供以下方法：

| 方法 | 說明 |
|------|------|
| `create_bucket(name)` | 建立新的儲存桶 |
| `upload_file(bucket, key, content)` | 上傳檔案到指定桶 |
| `download_file(bucket, key)` | 下載指定檔案 |
| `list_buckets()` | 列出所有儲存桶 |
| `list_files(bucket)` | 列出桶內所有檔案 |

## 資料結構

### 儲存桶結構

```python
self.buckets = {
    'bucket_name': {
        'file_key': {
            'content': '檔案內容',
            'hash': 'sha256_hash',
            'timestamp': 1234567890
        }
    }
}
```

### 內容雜湊

使用 SHA-256 計算內容指紋，確保資料完整性。

## 使用範例

```python
storage = CloudStorage()

# 建立儲存桶
storage.create_bucket('my-bucket')

# 上傳檔案
storage.upload_file('my-bucket', 'docs/readme.txt', 'Hello Cloud')

# 列出檔案
files = storage.list_files('my-bucket')

# 下載檔案
content = storage.download_file('my-bucket', 'docs/readme.txt')
```

## 與真實 S3 的差異

| 功能 | 模擬實作 | 真實 S3 |
|------|----------|---------|
| 認證 | 無 | IAM, Access Keys |
| 權限 | 無 | ACL, Bucket Policy |
| 多區域 | 無 | 全球分布 |
| 生命週期 | 無 | 支援 |
| 錯誤處理 | 簡單 | 完整 |

## 執行方式

```bash
python3 cloud_storage.py
```

## 延伸閱讀

- [boto3+S3+python](https://www.google.com/search?q=boto3+S3+python)
- [Amazon+S3+API](https://www.google.com/search?q=Amazon+S3+API)

---