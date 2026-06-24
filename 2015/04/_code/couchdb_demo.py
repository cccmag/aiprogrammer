#!/usr/bin/env python3
"""
CouchDB 基本操作範例
展示文件的 CRUD 操作和視圖查詢
"""

def demo():
    print("=== CouchDB 操作演示 ===")
    print("CouchDB 操作需要實際的 CouchDB 服務")
    print("這個程式展示邏輯結構：")

    print("""
1. 連接到 CouchDB 伺服器
2. 建立或選擇資料庫 'test_db'
3. 插入三個文件（兩個使用者、一篇文章）
4. 查詢特定文件
5. 更新文件（新增技能）
6. 使用視圖查詢所有文件
7. 刪除文件

程式碼邏輯：
- 使用 couchdb 庫連接
- doc1 = {'_id': 'user:1', 'type': 'user', 'name': '張小明', ...}
- doc2 = {'_id': 'user:2', 'type': 'user', 'name': '李小華', ...}
- doc3 = {'_id': 'post:1', 'type': 'post', 'title': 'CouchDB 入門', ...}
- db.save(doc1), db.save(doc2), db.save(doc3)
- retrieved = db['user:1']
- del db['user:1']
""")

    print("=== 程式結束 ===")

if __name__ == "__main__":
    demo()