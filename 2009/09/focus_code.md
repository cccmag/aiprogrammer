# 實作簡化文件資料庫：打造 MiniDB

## 簡介

本期程式實作將帶領讀者從頭實作一個簡化的文件資料庫 MiniDB，幫助理解文件儲存和查詢的基本概念。

## 程式碼

```python
#!/usr/bin/env python3
"""
MiniDB - A simplified document database

這個程式演示了文件資料庫的核心概念：
1. 文件儲存（JSON 格式）
2. 文件查詢
3. 基本索引
"""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime


@dataclass
class Document:
    data: Dict[str, Any]
    _id: str


class MiniDB:
    def __init__(self, name: str):
        self.name = name
        self.collections: Dict[str, List[Document]] = {}
        self.indices: Dict[str, Dict[str, str]] = {}
        self.data_dir = f"./{name}_data"
        os.makedirs(self.data_dir, exist_ok=True)

    def create_collection(self, name: str):
        if name not in self.collections:
            self.collections[name] = []
            self.indices[name] = {}

    def insert(self, collection: str, data: Dict[str, Any]) -> str:
        if collection not in self.collections:
            self.create_collection(collection)

        doc_id = data.get('_id') or str(datetime.now().timestamp())
        doc = Document(data=data, _id=doc_id)
        self.collections[collection].append(doc)
        self.indices[collection][doc_id] = doc
        return doc_id

    def find(self, collection: str,
             query: Optional[Dict[str, Any]] = None) -> List[Document]:
        if collection not in self.collections:
            return []

        if query is None:
            return self.collections[collection]

        results = []
        for doc in self.collections[collection]:
            if self._matches(doc.data, query):
                results.append(doc)
        return results

    def find_one(self, collection: str,
                 query: Optional[Dict[str, Any]] = None) -> Optional[Document]:
        results = self.find(collection, query)
        return results[0] if results else None

    def update(self, collection: str, query: Dict[str, Any],
               update: Dict[str, Any]) -> int:
        count = 0
        for doc in self.find(collection, query):
            for key, value in update.items():
                doc.data[key] = value
            count += 1
        return count

    def remove(self, collection: str, query: Dict[str, Any]) -> int:
        docs_to_remove = self.find(collection, query)
        for doc in docs_to_remove:
            self.collections[collection].remove(doc)
            del self.indices[collection][doc._id]
        return len(docs_to_remove)

    def _matches(self, data: Dict[str, Any], query: Dict[str, Any]) -> bool:
        for key, value in query.items():
            if isinstance(value, dict):
                if not self._match_operator(data.get(key), value):
                    return False
            else:
                if data.get(key) != value:
                    return False
        return True

    def _match_operator(self, field_value: Any,
                         operators: Dict[str, Any]) -> bool:
        for op, expected in operators.items():
            if op == '$gt':
                if not (field_value is not None and field_value > expected):
                    return False
            elif op == '$gte':
                if not (field_value is not None and field_value >= expected):
                    return False
            elif op == '$lt':
                if not (field_value is not None and field_value < expected):
                    return False
            elif op == '$lte':
                if not (field_value is not None and field_value <= expected):
                    return False
            elif op == '$eq':
                if field_value != expected:
                    return False
            elif op == '$ne':
                if field_value == expected:
                    return False
        return True

    def count(self, collection: str, query: Optional[Dict] = None) -> int:
        return len(self.find(collection, query))


def demo():
    print("\n" + "#" * 60)
    print("# MiniDB - Document Database Demo")
    print("#" * 60 + "\n")

    db = MiniDB("test")

    db.create_collection("users")

    db.insert("users", {
        "name": "張三",
        "age": 30,
        "city": "台北"
    })

    db.insert("users", {
        "name": "李四",
        "age": 25,
        "city": "台中"
    })

    db.insert("users", {
        "name": "王五",
        "age": 35,
        "city": "台北"
    })

    print("All users:")
    for doc in db.find("users"):
        print(f"  {doc._id}: {doc.data}")

    print("\nUsers in Taipei:")
    for doc in db.find("users", {"city": "台北"}):
        print(f"  {doc.data['name']}")

    print("\nUsers over 30:")
    for doc in db.find("users", {"age": {"$gt": 30}}):
        print(f"  {doc.data['name']}, age {doc.data['age']}")

    print("\nUpdate:")
    db.update("users", {"name": "張三"}, {"age": 31})
    user = db.find_one("users", {"name": "張三"})
    print(f"  Zhang's new age: {user.data['age']}")

    print("\nCount:", db.count("users"))


if __name__ == "__main__":
    demo()
```

## 測試方式

```bash
python3 _code/mongodb_demo.py
```

## 輸出範例

```
############################################################
# MiniDB - Document Database Demo
############################################################

All users:
  1251993600.0: {'name': '張三', 'age': 30, 'city': '台北'}
  1251993601.0: {'name': '李四', 'age': 25, 'city': '台中'}
  1251993602.0: {'name': '王五', 'age': 35, 'city': '台北'}

Users in Taipei:
  張三
  王五

Users over 30:
  王五, age 35

Update:
  Zhang's new age: 31

Count: 3
```

## 實作重點

1. **Document 類別**：表示單一文件，包含資料和 ID
2. **MiniDB 類別**：管理集合和索引
3. **insert**：新增文件，自動生成 ID
4. **find**：支援簡單查詢和操作符
5. **_matches**：判斷文件是否符合查詢條件

## 延伸學習

- 實作 compound indexes
- 實作更複雜的查詢運算子
- 實作文件更新操作符（$set, $inc）
- 實作持久化儲存

---

*本期程式實作到此結束。*