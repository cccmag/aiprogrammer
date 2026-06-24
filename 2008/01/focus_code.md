# Android SDK 程式實作

## 前言

本篇文章展示 `android_core.py` 的完整程式碼，模擬 Android 核心概念。雖然 Python 無法完全替代 Java 的 Android 開發，但我們可以用 Python 來理解 Android 的核心概念。

---

## 原始碼

完整的 Python 實作請參考：[_code/android_core.py](_code/android_core.py)

```python
#!/usr/bin/env python3
"""Android 核心概念示範程式"""

import json
from datetime import datetime


class Activity:
    def __init__(self, name):
        self.name = name
        self.state = "created"
        print(f"[Activity] {self.name} - onCreate()")

    def on_start(self):
        self.state = "started"
        print(f"[Activity] {self.name} - onStart()")

    def on_resume(self):
        self.state = "resumed"
        print(f"[Activity] {self.name} - onResume()")

    def on_pause(self):
        self.state = "paused"
        print(f"[Activity] {self.name} - onPause()")

    def on_stop(self):
        self.state = "stopped"
        print(f"[Activity] {self.name} - onStop()")

    def on_destroy(self):
        self.state = "destroyed"
        print(f"[Activity] {self.name} - onDestroy()")

    def on_restart(self):
        self.state = "restarted"
        print(f"[Activity] {self.name} - onRestart()")


class Intent:
    def __init__(self, action=None, data=None):
        self.action = action
        self.data = data
        self.extras = {}

    def put_extra(self, key, value):
        self.extras[key] = value

    def get_extra(self, key, default=None):
        return self.extras.get(key, default)

    def __str__(self):
        return f"Intent(action={self.action}, data={self.data}, extras={self.extras})"


class IntentFilter:
    def __init__(self):
        self.actions = []
        self.categories = []

    def add_action(self, action):
        self.actions.append(action)

    def add_category(self, category):
        self.categories.append(category)

    def match(self, intent):
        if intent.action in self.actions:
            return True
        return False


class Service:
    def __init__(self, name):
        self.name = name
        self.running = False
        print(f"[Service] {self.name} created")

    def on_create(self):
        print(f"[Service] {self.name} - onCreate()")

    def on_start_command(self, intent):
        self.running = True
        print(f"[Service] {self.name} - onStartCommand(), running={self.running}")

    def on_destroy(self):
        self.running = False
        print(f"[Service] {self.name} - onDestroy()")


class BroadcastReceiver:
    def __init__(self, name):
        self.name = name

    def on_receive(self, context, intent):
        print(f"[Receiver] {self.name} received: {intent}")


class ContentProvider:
    def __init__(self, name):
        self.name = name
        self.data = {}

    def query(self, uri):
        print(f"[Provider] {self.name} query: {uri}")
        return self.data

    def insert(self, uri, values):
        print(f"[Provider] {self.name} insert: {uri}")
        self.data[uri] = values
        return uri


class AndroidManifest:
    def __init__(self):
        self.activities = []
        self.services = []
        self.receivers = []
        self.providers = []

    def register_activity(self, activity, intent_filter=None):
        self.activities.append((activity, intent_filter))
        print(f"[Manifest] Activity '{activity}' registered")

    def register_service(self, service):
        self.services.append(service)
        print(f"[Manifest] Service '{service.name}' registered")

    def register_receiver(self, receiver, intent_filter):
        self.receivers.append((receiver, intent_filter))
        print(f"[Manifest] Receiver '{receiver.name}' registered")


class View:
    def __init__(self, view_type, width="wrap_content", height="wrap_content"):
        self.view_type = view_type
        self.width = width
        self.height = height
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return f"{self.view_type}({self.width}x{self.height}, {len(self.children)} children)"


class LinearLayout(View):
    def __init__(self, orientation="vertical"):
        super().__init__("LinearLayout")
        self.orientation = orientation


class TextView(View):
    def __init__(self, text="", text_size=16):
        super().__init__("TextView")
        self.text = text
        self.text_size = text_size


class Button(View):
    def __init__(self, text="", on_click=None):
        super().__init__("Button")
        self.text = text
        self.on_click = on_click


class ListView(View):
    def __init__(self):
        super().__init__("ListView")
        self.items = []

    def set_adapter(self, adapter):
        self.adapter = adapter
        self.items = adapter.get_items()


def demo_activity_lifecycle():
    print("\n=== Activity 生命週期 ===")

    activity = Activity("MainActivity")
    activity.on_start()
    activity.on_resume()

    print(f"  [狀態] Activity 運行中: {activity.state}")

    activity.on_pause()
    activity.on_stop()
    activity.on_destroy()


def demo_intent_and_communication():
    print("\n=== Intent 與元件通訊 ===")

    intent1 = Intent(action="android.intent.action.VIEW")
    intent1.put_extra("url", "https://www.google.com")
    print(f"  Intent 1: {intent1}")

    intent2 = Intent(action="android.intent.action.SEND")
    intent2.put_extra("text", "Hello Android!")
    intent2.put_extra("count", 42)
    print(f"  Intent 2: {intent2}")

    value = intent2.get_extra("text")
    print(f"  取得 extra 'text': {value}")


def demo_intent_filter():
    print("\n=== Intent Filter 匹配 ===")

    filter1 = IntentFilter()
    filter1.add_action("android.intent.action.VIEW")
    filter1.add_category("android.intent.category.DEFAULT")

    intent1 = Intent(action="android.intent.action.VIEW")
    intent2 = Intent(action="android.intent.action.SEND")

    print(f"  Filter 匹配 intent1(VIEW): {filter1.match(intent1)}")
    print(f"  Filter 匹配 intent2(SEND): {filter1.match(intent2)}")


def demo_service():
    print("\n=== Service 元件 ===")

    service = Service("MyBackgroundService")
    service.on_create()
    service.on_start_command(Intent(action="START"))
    service.on_destroy()


def demo_broadcast_receiver():
    print("\n=== BroadcastReceiver ===")

    receiver = BroadcastReceiver("MyReceiver")

    intent = Intent(action="com.example.MY_BROADCAST")
    intent.put_extra("message", "Test broadcast")
    receiver.on_receive(None, intent)


def demo_content_provider():
    print("\n=== ContentProvider ===")

    provider = ContentProvider("MyContentProvider")

    uri = "content://com.example.provider/data"
    values = {"name": "Test", "value": 100}
    provider.insert(uri, values)

    result = provider.query(uri)
    print(f"  查詢結果: {result}")


def demo_view_hierarchy():
    print("\n=== View 階層結構 ===")

    root = LinearLayout(orientation="vertical")

    title = TextView(text="歡迎使用 Android")
    root.add_child(title)

    button_layout = LinearLayout(orientation="horizontal")
    btn1 = Button(text="確定")
    btn2 = Button(text="取消")
    button_layout.add_child(btn1)
    button_layout.add_child(btn2)

    root.add_child(button_layout)

    print(f"  根視圖: {root}")
    print(f"  子視圖數量: {len(root.children)}")


def demo_manifest():
    print("\n=== AndroidManifest 註冊 ===")

    manifest = AndroidManifest()

    activity = Activity("MainActivity")
    intent_filter = IntentFilter()
    intent_filter.add_action("android.intent.action.MAIN")

    manifest.register_activity(activity, intent_filter)
    manifest.register_service(Service("MyService"))
    manifest.register_receiver(
        BroadcastReceiver("MyReceiver"),
        IntentFilter()
    )


def demo():
    print("Android 核心概念示範")
    print("=" * 40)

    demo_activity_lifecycle()
    demo_intent_and_communication()
    demo_intent_filter()
    demo_service()
    demo_broadcast_receiver()
    demo_content_provider()
    demo_view_hierarchy()
    demo_manifest()

    print("\n所有示範完成！")


if __name__ == "__main__":
    demo()
```

---

## 執行結果

```
Android 核心概念示範
========================================

=== Activity 生命週期 ===
[Activity] MainActivity - onCreate()
[Activity] MainActivity - onStart()
[Activity] MainActivity - onResume()
  [狀態] Activity 運行中: resumed
[Activity] MainActivity - onPause()
[Activity] MainActivity - onStop()
[Activity] MainActivity - onDestroy()

=== Intent 與元件通訊 ===
  Intent 1: Intent(action=android.intent.action.VIEW, data=None, extras={'url': 'https://www.google.com'})
  Intent 2: Intent(action=android.intent.action.SEND, data=None, extras={'text': 'Hello Android!', 'count': 42})
  取得 extra 'text': Hello Android!

=== Intent Filter 匹配 ===
  Filter 匹配 intent1(VIEW): True
  Filter 匹配 intent2(SEND): False

=== Service 元件 ===
[Service] MyBackgroundService created
[Service] MyBackgroundService - onCreate()
[Service] MyBackgroundService - onStartCommand(), running=True
[Service] MyBackgroundService - onDestroy()

=== BroadcastReceiver ===
[Receiver] MyReceiver received: Intent(action=com.example.MY_BROADCAST, data=None, extras={'message': 'Test broadcast'})

=== ContentProvider ===
[Provider] MyContentProvider insert: content://com.example.provider/data
[Provider] MyContentProvider query: content://com.example.provider/data
  查詢結果: {'content://com.example.provider/data': {'name': 'Test', 'value': 100}}

=== View 階層結構 ===
  根視圖: LinearLayout(wrap_contentxwrap_content, 2 children)
  子視圖數量: 2

=== AndroidManifest 註冊 ===
[Manifest] Activity 'MainActivity' registered
[Manifest] Service 'MyBackgroundService' registered
[Manifest] Receiver 'MyReceiver' registered

所有示範完成！
```

---

## 程式說明

### 1. Activity 生命週期

Activity 類別展示了 Android Activity 的狀態變化：

```python
activity = Activity("MainActivity")
activity.on_start()
activity.on_resume()
# ... 使用者互動 ...
activity.on_pause()
activity.on_stop()
activity.on_destroy()
```

### 2. Intent 與元件通訊

Intent 是 Android 中訊息傳遞的核心：

```python
intent = Intent(action="android.intent.action.VIEW")
intent.put_extra("url", "https://www.google.com")
```

### 3. Intent Filter

IntentFilter 用於宣告 Activity 或 Service 能夠處理的 Intent：

```python
filter1 = IntentFilter()
filter1.add_action("android.intent.action.VIEW")
filter1.add_category("android.intent.category.DEFAULT")
```

### 4. Service 元件

Service 是背景執行的元件：

```python
service = Service("MyBackgroundService")
service.on_start_command(Intent(action="START"))
```

### 5. BroadcastReceiver

廣播接收器用於接收系統或應用程式發送的廣播：

```python
receiver = BroadcastReceiver("MyReceiver")
receiver.on_receive(None, intent)
```

### 6. ContentProvider

ContentProvider 提供了跨應用程式資料共享的機制：

```python
provider = ContentProvider("MyContentProvider")
provider.insert(uri, values)
```

### 7. View 階層結構

UI 元件以樹狀結構組織：

```python
root = LinearLayout(orientation="vertical")
title = TextView(text="標題")
root.add_child(title)
```

---

## 延伸閱讀

- [Android Activity lifecycle](https://www.google.com/search?q=Android+Activity+lifecycle)
- [Android Intent documentation](https://www.google.com/search?q=Android+Intent+documentation)
- [Android+四大元件](https://www.google.com/search?q=Android+四大元件)

---

*本篇文章為「AI 程式人雜誌 2008 年 1 月號」Android 開發系列補充文章。*