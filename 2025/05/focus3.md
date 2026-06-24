# JSON 資料處理

## JSON 格式簡介

JSON（JavaScript Object Notation）是一種輕量級的資料交換格式。雖然源自 JavaScript，但目前已成為跨語言、跨平台的通用資料格式，是 Web API 最常用的資料交換媒介。

### JSON 語法

JSON 使用兩種基本結構：物件（Object）和陣列（Array）。

```json
{
  "name": "Alice",
  "age": 30,
  "is_active": true,
  "skills": ["Python", "JavaScript"],
  "address": {
    "city": "台北",
    "zip": "100"
  },
  "score": null
}
```

### JSON 資料型別

| JSON 型別 | 範例 | Python 對應型別 |
|-----------|------|----------------|
| 字串 | `"hello"` | `str` |
| 數字 | `42`, `3.14` | `int`, `float` |
| 布林值 | `true`, `false` | `bool` |
| 陣列 | `[1, 2, 3]` | `list` |
| 物件 | `{"key": "val"}` | `dict` |
| null | `null` | `None` |

## Python 的 json 模組

Python 標準函式庫提供了 `json` 模組來處理 JSON 資料。

### 序列化（Python → JSON）

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "is_active": True,
    "skills": ["Python", "JavaScript"],
    "score": None
}

# 轉換為 JSON 字串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)
```

輸出：

```json
{
  "name": "Alice",
  "age": 30,
  "is_active": true,
  "skills": ["Python", "JavaScript"],
  "score": null
}
```

### 反序列化（JSON → Python）

```python
json_str = '{"name": "Alice", "age": 30, "is_active": true}'
data = json.loads(json_str)
print(data['name'])  # Alice
print(type(data))    # <class 'dict'>
```

### 檔案讀寫

```python
# 寫入 JSON 檔案
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 讀取 JSON 檔案
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
```

## 進階序列化

### 處理自訂物件

```python
from datetime import datetime
import json

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'無法序列化 {type(obj)}')

now = datetime.now()
data = {'event': 'meeting', 'time': now}
json_str = json.dumps(data, default=custom_serializer)
print(json_str)
```

### 使用自訂編碼器

```python
from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {'time': datetime.now()}
json_str = json.dumps(data, cls=DateTimeEncoder)
```

## JSON 資料驗證

### 使用 try-except 驗證

```python
def safe_parse(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f'JSON 解析錯誤：{e}')
        return None

invalid_json = '{"name": "Alice", age: 30}'  # age 缺少引號
safe_parse(invalid_json)
```

### 使用 jsonschema 驗證

```python
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "required": ["name", "email"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "age": {"type": "integer", "minimum": 0}
    }
}

data = {"name": "Alice", "email": "alice@example.com", "age": 30}
try:
    validate(data, schema)
    print('驗證通過')
except ValidationError as e:
    print(f'驗證失敗：{e.message}')
```

## API 回應中的 JSON 處理

```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
data = response.json()

# 提取特定欄位
print(f"ID: {data['id']}")
print(f"Title: {data['title']}")
print(f"Body: {data['body']}")

# 處理巢狀結構
posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
titles = [post['title'] for post in posts[:3]]
```

## JSON Lines 格式

JSON Lines（`.jsonl`）每行一個 JSON 物件，適合處理大量資料：

```python
import json

data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]

# 寫入
with open('data.jsonl', 'w') as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

# 讀取
with open('data.jsonl', 'r') as f:
    for line in f:
        item = json.loads(line.strip())
        print(item['name'])
```

---

## 延伸閱讀

- [JSON 官方網站](https://www.google.com/search?q=JSON+official+website)
- [Python json 模組文件](https://www.google.com/search?q=Python+json+module)
- [JSON Schema 規範](https://www.google.com/search?q=JSON+Schema+specification)
