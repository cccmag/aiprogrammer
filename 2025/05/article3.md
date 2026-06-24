# JSON 解析與產生

## JSON 的歷史與地位

JSON 由 Douglas Crockford 在 2001 年規範，2006 年成為 ECMA 標準。JSON 之所以成為 Web API 的事實標準，是因為它比 XML 更簡潔、更容易解析，且與 JavaScript 完美相容。

## 使用 json 模組進行資料轉換

### 基本轉換

```python
import json

# Python 字典 → JSON 字串
data = {'name': 'Alice', 'age': 30, 'scores': [85, 92, 78]}
json_str = json.dumps(data, indent=2)
print(json_str)

# JSON 字串 → Python 字典
json_data = '{"name": "Bob", "age": 25, "active": true}'
parsed = json.loads(json_data)
print(parsed['name'])  # Bob
```

### 型別對應表

```python
# Python → JSON
{
    'string': 'hello',          # → "hello" (字串)
    'integer': 42,               # → 42 (數字)
    'float': 3.14,              # → 3.14 (數字)
    'boolean': True,             # → true (布林值)
    'none': None,                # → null (空值)
    'list': [1, 2, 3],          # → [1, 2, 3] (陣列)
    'dict': {'key': 'value'},   # → {"key": "value"} (物件)
}
```

## 進階序列化選項

```python
data = {'name': 'Alice', 'age': 30}

# 格式化輸出
print(json.dumps(data, indent=2))
print(json.dumps(data, indent=4, sort_keys=True))

# 壓縮輸出（無空白）
print(json.dumps(data, separators=(',', ':')))

# 處理非 ASCII 字元
data = {'name': '小明', 'city': '台北'}
print(json.dumps(data))
# {"name": "\u5c0f\u660e", "city": "\u53f0\u5317"}
print(json.dumps(data, ensure_ascii=False))
# {"name": "小明", "city": "台北"}
```

## JSON 串流處理

對於大型 JSON 檔案，可以使用 `ijson` 進行串流解析，避免記憶體不足。

```python
import json

# 逐行處理 JSON Lines
def process_jsonl(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                yield item

# 使用範例
for record in process_jsonl('large_data.jsonl'):
    print(record['id'], record['name'])
```

## 自訂 JSON 編碼器

```python
import json
from datetime import datetime, date
from decimal import Decimal

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.hex()
        return super().default(obj)

data = {
    'created_at': datetime.now(),
    'price': Decimal('19.99'),
    'checksum': b'\x00\x01\x02',
}
print(json.dumps(data, cls=CustomEncoder, indent=2))
```

## JSON 資料合併與轉換

```python
import json

# 合併兩個 JSON 物件
user = json.loads('{"id": 1, "name": "Alice"}')
profile = json.loads('{"age": 30, "email": "alice@example.com"}')
merged = {**user, **profile}
print(json.dumps(merged, indent=2))

# JSON 資料轉換（重構）
posts = json.loads('[{"id": 1, "title": "A", "userId": 1}, {"id": 2, "title": "B", "userId": 1}]')

# 轉換為以 id 為 key 的字典
indexed = {p['id']: p for p in posts}
print(indexed[1]['title'])
```

## JSON Schema 驗證

```python
from jsonschema import validate, ValidationError
import json

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "uniqueItems": True
        }
    },
    "required": ["id", "name", "email"]
}

data = {"id": 1, "name": "Alice", "email": "alice@example.com", "tags": ["python", "api"]}
try:
    validate(data, schema)
    print("資料驗證通過")
except ValidationError as e:
    print(f"驗證錯誤：{e.message}")
```

## 從 API 處理 JSON 的完整流程

```python
import requests
import json
from jsonschema import validate, ValidationError

API_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "completed": {"type": "boolean"}
    },
    "required": ["userId", "id", "title", "completed"]
}

def fetch_and_validate_todo(todo_id):
    response = requests.get(
        f'https://jsonplaceholder.typicode.com/todos/{todo_id}')
    response.raise_for_status()
    data = response.json()
    try:
        validate(data, API_SCHEMA)
        return data
    except ValidationError as e:
        print(f"API 回應格式錯誤：{e}")
        return None

todo = fetch_and_validate_todo(1)
if todo:
    print(f"代辦事項：{todo['title']}, 完成：{todo['completed']}")
```

---

## 延伸閱讀

- [Python json 官方文件](https://www.google.com/search?q=Python+json+module+documentation)
- [JSON Schema 官方網站](https://www.google.com/search?q=JSON+Schema+official)
- [JSON 與 XML 比較](https://www.google.com/search?q=JSON+vs+XML+comparison)
