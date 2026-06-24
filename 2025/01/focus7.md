# 從程式到解決方案：實戰演練

## 前言

到目前為止，我們已經學習了 Python 的各種基礎知識。現在，讓我們將這些知識整合起來，完成一個真正有用的專案。實戰是學習程式設計最好的方式。

## 專案：待辦事項管理工具

我們將建立一個命令列待辦事項管理工具，支援新增、檢視、完成和刪除待辦事項。

### 需求分析

1. 新增待辦事項
2. 檢視所有待辦事項
3. 標記事項為已完成
4. 刪除待辦事項
5. 將資料持久化儲存到檔案

### 實作步驟

#### 步驟一：資料結構設計

```python
# 每個待辦事項使用字典表示
# {
#   "id": 1,
#   "title": "購買食材",
#   "done": False
# }

# 所有事項使用列表儲存
todos = []
```

#### 步驟二：基本功能

```python
def add_todo(todos, title):
    """新增待辦事項"""
    todo = {
        "id": len(todos) + 1,
        "title": title,
        "done": False
    }
    todos.append(todo)
    print(f"已新增：{title}")

def list_todos(todos):
    """列出所有待辦事項"""
    if not todos:
        print("目前沒有待辦事項")
        return

    print("\n=== 待辦事項清單 ===")
    for todo in todos:
        status = "✓" if todo["done"] else " "
        print(f"[{status}] {todo['id']}. {todo['title']}")
    print()

def complete_todo(todos, todo_id):
    """標記事項為已完成"""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            print(f"已完成：{todo['title']}")
            return
    print(f"找不到 id = {todo_id} 的事項")

def delete_todo(todos, todo_id):
    """刪除待辦事項"""
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(i)
            print(f"已刪除：{removed['title']}")
            return
    print(f"找不到 id = {todo_id} 的事項")
```

#### 步驟三：檔案持久化

```python
import json

def save_todos(todos, filename="todos.json"):
    """儲存待辦事項到檔案"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
    print("已儲存！")

def load_todos(filename="todos.json"):
    """從檔案載入待辦事項"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
```

#### 步驟四：命令列介面

```python
def show_menu():
    """顯示選單"""
    print("\n=== 待辦事項管理工具 ===")
    print("1. 檢視所有事項")
    print("2. 新增事項")
    print("3. 完成事項")
    print("4. 刪除事項")
    print("5. 儲存並離開")
    return input("請選擇操作 (1-5)：")

def main():
    """主程式"""
    todos = load_todos()

    while True:
        choice = show_menu()

        if choice == "1":
            list_todos(todos)

        elif choice == "2":
            title = input("請輸入待辦事項：")
            if title.strip():
                add_todo(todos, title)
            else:
                print("事項內容不能為空")

        elif choice == "3":
            list_todos(todos)
            try:
                todo_id = int(input("請輸入要完成的事項編號："))
                complete_todo(todos, todo_id)
            except ValueError:
                print("請輸入有效的編號")

        elif choice == "4":
            list_todos(todos)
            try:
                todo_id = int(input("請輸入要刪除的事項編號："))
                delete_todo(todos, todo_id)
            except ValueError:
                print("請輸入有效的編號")

        elif choice == "5":
            save_todos(todos)
            print("感謝使用！")
            break

        else:
            print("無效的選擇，請重新輸入")

if __name__ == "__main__":
    main()
```

## 執行測試

```python
# 快速測試功能
def test_todo_app():
    todos = []
    add_todo(todos, "購買食材")
    add_todo(todos, "撰寫報告")
    add_todo(todos, "運動30分鐘")
    list_todos(todos)
    complete_todo(todos, 2)
    list_todos(todos)
    delete_todo(todos, 1)
    list_todos(todos)

test_todo_app()
```

## 學習重點回顧

這個專案涵蓋了本系列的所有主題：

| 主題 | 應用 |
|------|------|
| 變數與型別 | 字串、整數、布林、列表、字典 |
| 流程控制 | if/else 條件判斷、while 迴圈 |
| 函數定義 | 參數、回傳值、模組化設計 |
| 字串操作 | f-string 格式化、輸入輸出 |
| 檔案操作 | JSON 序列化、錯誤處理 |
| 資料結構 | 列表儲存集合、字典表示單一項目 |

## 小結

從學習語法到建立完整的應用程式，你已經走了很長的一段路。再次強調：最好的學習方式是動手寫程式。試著修改上面的程式，加入更多功能，例如設定優先級、截止日期、分類標籤等。每一次的修改和嘗試，都會讓你對程式設計的理解更加深入。

---

**延伸閱讀**

- [Python JSON 模組](https://www.google.com/search?q=Python+json+module+tutorial)
- [命令列工具開發實戰](https://www.google.com/search?q=Python+command+line+tool+tutorial)
