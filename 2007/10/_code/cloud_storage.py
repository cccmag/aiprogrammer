#!/usr/bin/env python3
"""雲端儲存客戶端實作 - S3 風格 API 模擬"""

import json
import hashlib
import time

class CloudStorage:
    def __init__(self):
        self.buckets = {}

    def create_bucket(self, bucket_name):
        if bucket_name in self.buckets:
            return {'error': 'Bucket already exists'}
        self.buckets[bucket_name] = {}
        return {'bucket': bucket_name, 'created': True}

    def upload_file(self, bucket_name, key, content):
        if bucket_name not in self.buckets:
            return {'error': 'Bucket not found'}

        content_hash = hashlib.sha256(content.encode()).hexdigest()
        self.buckets[bucket_name][key] = {
            'content': content,
            'hash': content_hash,
            'timestamp': time.time()
        }
        return {'key': key, 'hash': content_hash}

    def download_file(self, bucket_name, key):
        if bucket_name not in self.buckets:
            return {'error': 'Bucket not found'}
        if key not in self.buckets[bucket_name]:
            return {'error': 'Key not found'}

        return self.buckets[bucket_name][key]

    def list_buckets(self):
        return list(self.buckets.keys())

    def list_files(self, bucket_name):
        if bucket_name not in self.buckets:
            return []
        return list(self.buckets[bucket_name].keys())

def demo():
    print('雲端儲存 API 演示')
    print('=' * 40)

    storage = CloudStorage()

    print('\n1. 建立儲存桶')
    result = storage.create_bucket('my-bucket')
    print(f'   {result}')

    print('\n2. 上傳檔案')
    result = storage.upload_file('my-bucket', 'documents/readme.txt', 'Hello Cloud')
    print(f'   {result}')

    print('\n3. 列出檔案')
    files = storage.list_files('my-bucket')
    print(f'   {files}')

    print('\n4. 下載檔案')
    result = storage.download_file('my-bucket', 'documents/readme.txt')
    print(f'   {result}')

if __name__ == '__main__':
    demo()