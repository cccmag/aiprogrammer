# Amazon S3：雲端儲存的商業化

## 前言

2007 年，Amazon S3（Simple Storage Service）已商業化運營一年多，成為雲端運算的代表作之一。

## S3 的核心概念

```python
# boto（AWS Python SDK）使用 S3
import boto

conn = boto.connect_s3('AWS_KEY', 'AWS_SECRET')
bucket = conn.create_bucket('my-app-bucket')

# 上傳檔案
key = bucket.new_key('documents/report.pdf')
key.set_contents_from_filename('report.pdf')

# 下載檔案
key.get_contents_to_filename('download.pdf')

# 設定存取權限
key.set_acl('public-read')
```

## S3 的影響

S3 的「按使用量付費」模式開創了雲端儲存的新商業模式。

## 結語

Amazon S3 的成功奠定了雲端運算的基礎設施模式。

---

## 延伸閱讀

- [Amazon+S3+2007](https://www.google.com/search?q=Amazon+S3+2007)
- [AWS+cloud+storage+pricing](https://www.google.com/search?q=AWS+cloud+storage+pricing)

---