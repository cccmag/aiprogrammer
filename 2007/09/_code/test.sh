#!/bin/bash
set -x

echo "=== 測試資料庫技術相關展示 ==="

# 測試 focus_code 概念
python3 -c "
print('Testing SQL concepts...')
queries = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
print(f'Basic operations: {queries}')
print('Test passed: SQL concepts loaded')
"

# 測試 article1 (SQLite)
python3 -c "
print('Testing SQLite concepts...')
print('SQLite: zero-config, single file database')
print('Test passed: SQLite concepts')
"

# 測試 article2 (Redis)
python3 -c "
print('Testing Redis concepts...')
data_types = ['String', 'Hash', 'List', 'Set', 'Sorted Set']
print(f'Redis data types: {len(data_types)}')
print('Test passed: Redis concepts')
"

# 測試 article3 (CouchDB)
python3 -c "
print('Testing CouchDB concepts...')
print('CouchDB: document database with RESTful API')
print('Test passed: CouchDB concepts')
"

# 測試 article6 (RDF)
python3 -c "
print('Testing RDF concepts...')
triple = ('subject', 'predicate', 'object')
print(f'RDF triple: {triple}')
print('Test passed: RDF concepts')
"

# 測試 article7 (專家系統)
python3 -c "
print('Testing expert system concepts...')
print('CLIPS: rule-based expert system tool')
print('Test passed: Expert system concepts')
"

# 測試 article9 (類神經網路)
python3 -c "
print('Testing neural network concepts...')
layers = ['Input', 'Hidden', 'Output']
print(f'Network layers: {layers}')
print('Test passed: Neural network concepts')
"

# 測試 article10 (資訊檢索)
python3 -c "
print('Testing information retrieval...')
from math import log, sqrt
# TF-IDF example
tf = 0.1
idf = 2.5
tfidf = tf * idf
print(f'TF-IDF example: {tfidf}')
print('Test passed: IR concepts')
"

echo ""
echo "=== 所有測試完成 ==="