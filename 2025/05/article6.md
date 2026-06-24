# POST、PUT、DELETE 實作

## CRUD 操作的完整流程

CRUD（Create、Read、Update、Delete）是 Web API 最常見的操作模式。本文將完整實作一個任務管理 API。

## 建立資源（POST）

POST 方法用於建立新資源。每次 POST 請求應建立一個新的資源實例。

### FastAPI 實作

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

tasks_db = []
next_id = 1

@app.post("/tasks/", response_model=TaskResponse, status_code=201)
def create_task(task: Task):
    global next_id
    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }
    tasks_db.append(new_task)
    next_id += 1
    return new_task
```

### requests 呼叫

```python
import requests

new_task = {
    "title": "學習 FastAPI",
    "description": "完成 POST/PUT/DELETE 實作",
    "completed": False
}
resp = requests.post("http://localhost:8000/tasks/", json=new_task)
print(resp.status_code)  # 201
print(resp.json())
```

## 讀取資源（GET）

```python
@app.get("/tasks/", response_model=List[TaskResponse])
def list_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="任務不存在")
```

## 完整更新資源（PUT）

PUT 用於完整更新資源，客戶端需要提供資源的所有欄位。

```python
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            tasks_db[i] = {
                "id": task_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
            return tasks_db[i]
    raise HTTPException(status_code=404, detail="任務不存在")
```

### PUT 的冪等性

```python
# 第一次 PUT
resp1 = requests.put("http://localhost:8000/tasks/1",
    json={"title": "完成任務", "description": "已更新", "completed": True})
print(resp1.status_code)  # 200

# 第二次 PUT（相同資料）
resp2 = requests.put("http://localhost:8000/tasks/1",
    json={"title": "完成任務", "description": "已更新", "completed": True})
print(resp2.status_code)  # 200，結果與第一次相同
```

## 部分更新資源（PATCH）

PATCH 用於部分更新，客戶端只需提供要修改的欄位。

```python
from pydantic import BaseModel

class TaskPatch(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(task_id: int, patch: TaskPatch):
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            update_data = patch.model_dump(exclude_unset=True)
            tasks_db[i].update(update_data)
            return tasks_db[i]
    raise HTTPException(status_code=404, detail="任務不存在")
```

```python
# 只更新 completed 欄位
resp = requests.patch("http://localhost:8000/tasks/1",
    json={"completed": True})
print(resp.json())
```

## 刪除資源（DELETE）

```python
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="任務不存在")
```

```python
resp = requests.delete("http://localhost:8000/tasks/1")
print(resp.status_code)  # 204
```

## 完整 CRUD 範例

```python
import requests

BASE = "http://localhost:8000"

# 建立多個任務
for i in range(1, 4):
    resp = requests.post(f"{BASE}/tasks/",
        json={"title": f"任務 {i}", "description": f"第 {i} 個任務"})
    print(f"Created: {resp.json()}")

# 列出所有任務
resp = requests.get(f"{BASE}/tasks/")
print(f"All tasks: {resp.json()}")

# 更新任務
resp = requests.put(f"{BASE}/tasks/1",
    json={"title": "已完成任務", "description": "已更新", "completed": True})
print(f"Updated: {resp.json()}")

# 部分更新
resp = requests.patch(f"{BASE}/tasks/2",
    json={"completed": True})
print(f"Patched: {resp.json()}")

# 刪除任務
resp = requests.delete(f"{BASE}/tasks/3")
print(f"Deleted status: {resp.status_code}")

# 確認結果
resp = requests.get(f"{BASE}/tasks/")
print(f"Final: {resp.json()}")
```

## 使用 FastAPI TestClient 測試

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_crud():
    # 建立
    resp = client.post("/tasks/", json={"title": "測試"})
    assert resp.status_code == 201
    task_id = resp.json()["id"]

    # 讀取
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "測試"

    # 更新
    resp = client.put(f"/tasks/{task_id}",
        json={"title": "更新", "description": "", "completed": True})
    assert resp.status_code == 200
    assert resp.json()["completed"] == True

    # 刪除
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204
```

---

## 延伸閱讀

- [HTTP PUT vs POST](https://www.google.com/search?q=HTTP+PUT+vs+POST+difference)
- [HTTP PATCH 方法](https://www.google.com/search?q=HTTP+PATCH+method+RFC)
- [RESTful CRUD 最佳實踐](https://www.google.com/search?q=RESTful+CRUD+best+practices)
