"""
TDD 與 BDD 實戰示範 - 任務管理系統

本範例展示如何以 TDD 方式開發一個簡單的任務管理系統。
"""
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

class TaskManagerDemo:
    @staticmethod
    def run_tests():
        print("=== TDD Task Manager Demo ===\n")
        
        tests_passed = 0
        tests_total = 0
        
        def test(name, condition):
            nonlocal tests_passed, tests_total
            tests_total += 1
            if condition:
                tests_passed += 1
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name}")
        
        manager = TaskManager()
        
        print("Creating tasks...")
        t1 = manager.create_task("完成報告", "必須在週五前完成")
        t2 = manager.create_task("開會", "與團隊討論進度")
        t3 = manager.create_task("回覆郵件")
        
        test("Created task has id", t1.id is not None)
        test("Task title is set", t1.title == "完成報告")
        test("Task description is set", t1.description == "必須在週五前完成")
        test("New task is not completed", t1.completed == False)
        
        print("\nCompleting tasks...")
        manager.complete_task(t1.id)
        
        test("Task marked as completed", t1.completed == True)
        
        print("\nFiltering tasks...")
        completed = manager.list_completed()
        pending = manager.list_pending()
        
        test("One task completed", len(completed) == 1)
        test("Two tasks pending", len(pending) == 2)
        test("Completed task is correct", completed[0].title == "完成報告")
        
        print("\n=== Test Summary ===")
        print(f"Tests: {tests_passed}/{tests_total}")
        
        if tests_passed == tests_total:
            print("\n=== Task Summary ===")
            print(f"Total: {len(manager.list_all())}, Completed: {len(completed)}, Pending: {len(pending)}")
            print("\nAll tests passed!")
            return True
        else:
            print(f"\n{tests_total - tests_passed} tests failed!")
            return False

def demo():
    success = TaskManagerDemo.run_tests()
    exit(0 if success else 1)

if __name__ == "__main__":
    demo()