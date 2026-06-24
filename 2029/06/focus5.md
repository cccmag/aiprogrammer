# 協作工作區設計（2024-2029）

## 共享心智的數位空間

協作工作區（Collaborative Workspace）是人類與 AI 共同完成複雜任務的數位環境，從程式碼編輯器到設計工作室，形式多樣。

### 協作工作區的三大支柱

```python
class CollaborativeWorkspace:
    def __init__(self):
        self.shared_context = SharedContext()
        self.turn_manager = TurnManager()
        self.artifact_store = ArtifactStore()
```

#### 1. 共享上下文

人類與 AI 共同維護一個可編輯、可追溯的共享心智模型：

```python
class SharedContext:
    def __init__(self):
        self.beliefs: dict[str, any] = {}
        self.history: list[dict] = []

    def update(self, source: str, key: str, value: any):
        self.beliefs[key] = {"value": value, "source": source, "time": time.time()}
        self.history.append({"source": source, "key": key, "value": value})

    def resolve_conflict(self, key: str) -> any:
        entries = [e for e in self.history if e["key"] == key]
        if len(entries) < 2:
            return entries[-1]["value"] if entries else None
        latest_human = [e for e in entries if e["source"] == "human"]
        return latest_human[-1]["value"] if latest_human else entries[-1]["value"]
```

參見：[共享心智模型](https://www.google.com/search?q=shared+mental+model+human+AI+collaboration)

#### 2. 輪流管理

協作工作區需要明確的輪換機制：

```python
class TurnManager:
    def __init__(self):
        self.turn: str = "human"
        self.lock: bool = False

    def request_turn(self, agent: str) -> bool:
        if not self.lock:
            self.turn = agent
            self.lock = True
            return True
        return False

    def release_turn(self):
        self.lock = False
        self.turn = "free"

    def alternate(self):
        self.turn = "ai" if self.turn == "human" else "human"

    def suggest_next(self, human_active: bool) -> str:
        if human_active:
            return "human" if self.turn == "human" else "waiting"
        return "ai" if not self.lock else "busy"
```

#### 3. 產出管理

協作過程中產生的各種產出（程式碼、文件、設計稿）需要版本管理：

```python
class ArtifactStore:
    def __init__(self):
        self.artifacts: dict[str, list[dict]] = {}

    def commit(self, name: str, content: str, author: str):
        if name not in self.artifacts:
            self.artifacts[name] = []
        version = len(self.artifacts[name]) + 1
        self.artifacts[name].append({
            "version": version, "content": content,
            "author": author, "time": time.time()
        })
        return version

    def diff(self, name: str, v1: int, v2: int) -> str:
        versions = self.artifacts.get(name, [])
        if v1 < 1 or v2 > len(versions):
            return "版本不存在"
        a, b = versions[v1-1]["content"], versions[v2-1]["content"]
        return f"差異（{name} v{v1} → v{v2}）：\n  {self._simple_diff(a, b)}"

    def _simple_diff(self, a: str, b: str) -> str:
        if a == b: return "無變更"
        return f"長度 {len(a)} → {len(b)}"
```

### 協作模式範例

```python
def design_sprint():
    ws = CollaborativeWorkspace()
    # 人類提出需求
    ws.shared_context.update("human", "task", "設計登入頁面")
    # AI 產生初稿
    ws.turn_manager.request_turn("ai")
    ws.artifact_store.commit("login_page", "<form>...</form>", "ai")
    ws.turn_manager.release_turn()
    # 人類修改
    ws.turn_manager.request_turn("human")
    ws.artifact_store.commit("login_page", "<form improved>...</form>", "human")
    ws.turn_manager.release_turn()
    return ws
```

### 設計模式

| 模式 | 描述 | 適用情境 |
|------|------|----------|
| **並行協作** | 人類和 AI 同時工作在不同部分 | 大型專案 |
| **迭代精煉** | AI 產生，人類修改，循環進行 | 創意設計 |
| **監督執行** | AI 執行，人類監督 | 自動化任務 |
| **角色分工** | 人類負責決策，AI 負責執行 | 資料分析 |

參見：
- [協作編輯器設計](https://www.google.com/search?q=collaborative+editor+design+human+AI)
- [即時協作架構](https://www.google.com/search?q=real+time+collaboration+architecture+AI)
- [AI 輔助工作流程](https://www.google.com/search?q=AI+assisted+workflow+design)

## 結語

協作工作區的核心設計原則是：讓人類與 AI 各自發揮所長，並在交界面做到無縫切換。

---

*本篇文章為「AI 程式人雜誌 2026 年 9 月號」人機協作介面設計系列之五。*
