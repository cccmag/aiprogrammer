# 有限狀態機與 FSM 設計模式

## 前言

FSM（Finite State Machine）設計模式是一種將物件行為分解為離散狀態的軟體設計方法。這種模式廣泛應用於嵌入式系統、網路協議、遊戲開發和工作流程引擎等領域。

## FSM 設計模式基礎

### 基本結構

```python
from abc import ABC, abstractmethod
from enum import Enum, auto


class State(ABC):
    @abstractmethod
    def enter(self, context):
        pass

    @abstractmethod
    def exit(self, context):
        pass

    @abstractmethod
    def execute(self, context):
        pass


class Context:
    def __init__(self, initial_state):
        self._state = initial_state
        self._state.enter(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state.exit(self)
        self._state = new_state
        self._state.enter(self)

    def request(self):
        self._state.execute(self)


class ConcreteStateA(State):
    def enter(self, context):
        print("Entering State A")

    def exit(self, context):
        print("Exiting State A")

    def execute(self, context):
        print("Executing State A")
        context.state = ConcreteStateB()


class ConcreteStateB(State):
    def enter(self, context):
        print("Entering State B")

    def exit(self, context):
        print("Exiting State B")

    def execute(self, context):
        print("Executing State B")
        context.state = ConcreteStateA()


def fsm_demo():
    context = Context(ConcreteStateA())
    for _ in range(3):
        context.request()

fsm_demo()
```

## FSM 的實現方式

### 1. 表驅動 FSM

```python
class TableDrivenFSM:
    def __init__(self, state_table, initial_state):
        self.state_table = state_table
        self.current_state = initial_state

    def handle_event(self, event):
        transition = self.state_table.get((self.current_state, event))
        if transition:
            old_state = self.current_state
            self.current_state = transition['next_state']
            if 'action' in transition:
                transition['action']()
            return True
        return False


def table_driven_demo():
    # 定義狀態表
    state_table = {
        ('idle', 'start'): {'next_state': 'running', 'action': lambda: print("Starting!")},
        ('running', 'stop'): {'next_state': 'idle', 'action': lambda: print("Stopping!")},
        ('running', 'pause'): {'next_state': 'paused', 'action': lambda: print("Pausing!")},
        ('paused', 'resume'): {'next_state': 'running', 'action': lambda: print("Resuming!")},
        ('paused', 'stop'): {'next_state': 'idle', 'action': lambda: print("Stopping!")},
    }

    fsm = TableDrivenFSM(state_table, 'idle')

    fsm.handle_event('start')
    fsm.handle_event('pause')
    fsm.handle_event('resume')
    fsm.handle_event('stop')

table_driven_demo()
```

### 2. 事件驅動 FSM

```python
class Event:
    pass


class EventFSM:
    def __init__(self):
        self.handlers = {}
        self.current_state = None

    def add_handler(self, state, event_type, handler):
        if state not in self.handlers:
            self.handlers[state] = {}
        self.handlers[state][event_type] = handler

    def set_state(self, state):
        self.current_state = state

    def send_event(self, event):
        if self.current_state in self.handlers:
            if event.__class__ in self.handlers[self.current_state]:
                return self.handlers[self.current_state][event.__class__](self, event)
        return False


class StartEvent(Event):
    def __init__(self):
        self.name = "start"


class StopEvent(Event):
    def __init__(self):
        self.name = "stop"


def event_fsm_demo():
    fsm = EventFSM()

    def handle_start(fsm, event):
        print("Handling start")
        fsm.set_state('active')
        return True

    def handle_stop(fsm, event):
        print("Handling stop")
        fsm.set_state('idle')
        return True

    fsm.add_handler('idle', StartEvent, handle_start)
    fsm.add_handler('active', StopEvent, handle_stop)

    fsm.set_state('idle')
    fsm.send_event(StartEvent())
    fsm.send_event(StopEvent())

event_fsm_demo()
```

## FSM 的實際應用

### 網路連接管理

```python
class ConnectionState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    DISCONNECTING = auto()


class Connection:
    def __init__(self):
        self.state = ConnectionState.DISCONNECTED
        self.data_buffer = []

    def connect(self):
        if self.state == ConnectionState.DISCONNECTED:
            print("Initiating connection...")
            self.state = ConnectionState.CONNECTING
            return True
        return False

    def disconnect(self):
        if self.state == ConnectionState.CONNECTED:
            print("Initiating disconnection...")
            self.state = ConnectionState.DISCONNECTING
            self._flush_buffer()
            return True
        return False

    def send(self, data):
        if self.state == ConnectionState.CONNECTED:
            print(f"Sending: {data}")
            return True
        return False

    def _flush_buffer(self):
        print(f"Flushing {len(self.data_buffer)} items")
        self.data_buffer.clear()

    def on_connected(self):
        self.state = ConnectionState.CONNECTED
        print("Connected!")

    def on_disconnected(self):
        self.state = ConnectionState.DISCONNECTED
        print("Disconnected!")


def connection_demo():
    conn = Connection()
    conn.connect()
    conn.send("Hello")
    conn.disconnect()

connection_demo()
```

### HTTP 請求狀態機

```python
class HTTPRequestState(Enum):
    IDLE = auto()
    CONNECTING = auto()
    SENDING = auto()
    WAITING = auto()
    RECEIVING = auto()
    COMPLETED = auto()
    ERROR = auto()


class HTTPRequest:
    def __init__(self, url):
        self.url = url
        self.state = HTTPRequestState.IDLE
        self.response = None
        self.error = None

    def execute(self):
        transitions = {
            HTTPRequestState.IDLE: (HTTPRequestState.CONNECTING, self._do_connect),
            HTTPRequestState.CONNECTING: (HTTPRequestState.SENDING, self._do_send),
            HTTPRequestState.SENDING: (HTTPRequestState.WAITING, self._do_wait),
            HTTPRequestState.WAITING: (HTTPRequestState.RECEIVING, self._do_receive),
            HTTPRequestState.RECEIVING: (HTTPRequestState.COMPLETED, self._do_complete),
        }

        action = transitions.get(self.state)
        if action:
            next_state, action_fn = action
            self.state = next_state
            action_fn()

        return self.state == HTTPRequestState.COMPLETED

    def _do_connect(self):
        print(f"Connecting to {self.url}")

    def _do_send(self):
        print("Sending request")

    def _do_wait(self):
        print("Waiting for response")

    def _do_receive(self):
        print("Receiving response")
        self.response = {"status": 200, "body": "OK"}

    def _do_complete(self):
        print("Request completed")


def http_demo():
    req = HTTPRequest("https://example.com")
    while req.state != HTTPRequestState.COMPLETED:
        req.execute()

http_demo()
```

## FSM 的優勢與限制

### 優勢

1. **清晰的结构**：每個狀態的邏輯都很明確
2. **易於理解和維護**：狀態和轉換一目了然
3. **易於測試**：每個狀態可以獨立測試
4. **確定性**：同樣的輸入總是產生同樣的輸出

### 限制

1. **狀態爆炸**：當狀態和轉換增多時，表會變得很大
2. **不適合複雜行為**：層級狀態機或行為樹更適合複雜邏輯

## 小結

FSM 設計模式是一種經典且實用的設計模式。從正規語言理論中的有限自動機到實際的軟體設計，FSM 展示了一種將複雜系統分解為可管理狀態的強大方法。選擇合適的實現方式（表驅動、事件驅動、層級式）取決於具體應用場景的需求。

---

**延伸閱讀**

- [State Machine Design Pattern](https://www.google.com/search?q=state+machine+design+pattern)
- [FSM vs State Pattern](https://www.google.com/search?q=FSM+vs+state+pattern)
- [UML State Machine Diagrams](https://www.google.com/search?q=UML+state+machine+diagram)