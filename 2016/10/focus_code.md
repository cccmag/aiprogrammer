# 程式實作：TDD 與 BDD 實戰範例

## 簡介

本實作展示如何使用 TDD 與 BDD 方式開發一個簡單的任務管理系統。完整程式碼在 `_code/tdd_bdd_demo.py`。

## 專案需求

建立一個任務管理系統，支援：
- 建立任務
- 標記任務完成
- 列出所有任務
- 過濾已完成/未完成的任務

## TDD 開發過程

### 第一階段：需求分析與測試

```python
# test_task_manager.py
import pytest
from task_manager import TaskManager, Task

def test_create_task():
    manager = TaskManager()
    task = manager.create_task("完成報告", "必須在週五前完成")
    assert task.title == "完成報告"
    assert task.completed == False

def test_complete_task():
    manager = TaskManager()
    task = manager.create_task("測試任務")
    manager.complete_task(task.id)
    assert task.completed == True

def test_list_all_tasks():
    manager = TaskManager()
    manager.create_task("任務一")
    manager.create_task("任務二")
    assert len(manager.list_all()) == 2

def test_filter_completed():
    manager = TaskManager()
    t1 = manager.create_task("已完成任務")
    manager.complete_task(t1.id)
    manager.create_task("未完成任務")
    completed = manager.list_completed()
    assert len(completed) == 1
    assert completed[0].title == "已完成任務"
```

### 第二階段：實作（Green）

```python
# task_manager.py
from dataclasses import dataclass, field
from typing import List
from datetime import datetime
import uuid

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
    
    def create_task(self, title: str, description: str = "") -> Task:
        task = Task(
            id=str(uuid.uuid4())[:8],
            title=title,
            description=description
        )
        self.tasks.append(task)
        return task
    
    def complete_task(self, task_id: str) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                return True
        return False
    
    def list_all(self) -> List[Task]:
        return self.tasks.copy()
    
    def list_completed(self) -> List[Task]:
        return [t for t in self.tasks if t.completed]
    
    def list_pending(self) -> List[Task]:
        return [t for t in self.tasks if not t.completed]
```

## BDD 行為描述

```python
# test_bdd_behavior.py
from behave import given, when, then
from task_manager import TaskManager

@given('我有一個任務管理器')
def step_have_manager(context):
    context.manager = TaskManager()

@when('我建立一個任務 "{title}"')
def step_create_task(context, title):
    context.task = context.manager.create_task(title)

@then('任務應該存在於系統中')
def step_task_exists(context):
    all_tasks = context.manager.list_all()
    assert any(t.title == context.task.title for t in all_tasks)

@when('我完成這個任務')
def step_complete_task(context):
    context.manager.complete_task(context.task.id)

@then('任務應該被標記為完成')
def step_task_completed(context):
    assert context.task.completed == True
```

## 測試執行

```bash
cd _code
python3 tdd_bdd_demo.py
```

## 延伸練習

1. **加入截止日期**：為任務新增 due_date 欄位與逾期檢查
2. **優先順序**：支援任務優先順序（高/中/低）
3. **分類功能**：支援任務分類與標籤
4. **持久化**：將任務儲存至檔案或資料庫
5. **Web API**：使用 Flask 將任務管理系統 RESTful 化

## 預期輸出

```
=== TDD Task Manager Demo ===

Test: create_task - PASSED
Test: complete_task - PASSED
Test: list_all_tasks - PASSED
Test: filter_completed - PASSED
Test: filter_pending - PASSED

All tests passed! ✓

=== Task Summary ===
Total: 3, Completed: 1, Pending: 2
```

## 相關資源

- [pytest 文檔](https://www.google.com/search?q=pytest+tutorial+2016)
- [behave BDD 文檔](https://www.google.com/search?q=behave+BDD+tutorial)
- [TDD 實踐指南](https://www.google.com/search?q=test+driven+development+python+example)