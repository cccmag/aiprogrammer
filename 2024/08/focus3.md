# 焦點 3：Flutter Widget 體系

## 萬物皆 Widget

在 Flutter 中，Widget 是 UI 的基礎建構單元。從一個按鈕、一段文字，到整個頁面，全部都是 Widget。Widget 描述了 UI 的配置與樣式，而非實際的渲染物件。

## 三棵樹的協作

Flutter 內部維護三棵樹來管理 UI：

1. **Widget 樹** — 開發者撰寫的設定描述。輕量，每次重建都會重新建立。
2. **Element 樹** — Widget 樹的實例化。維持狀態、關聯 RenderObject。此樹是持久化的。
3. **RenderObject 樹** — 實際執行佈局與繪製。負責計算大小、位置、以及像素輸出。

當 Widget 重建時，Flutter 會比較新舊 Widget 的型別與 key，決定 Element 要更新、重複使用或重新建立。

## StatelessWidget

不包含可變狀態，完全由外部參數決定 UI。

```dart
class Greeting extends StatelessWidget {
  final String name;
  Greeting(this.name);
  @override
  Widget build(BuildContext context) {
    return Text('Hello, $name!');
  }
}
```

## StatefulWidget

包含可變狀態，透過 `setState()` 觸發重建。

```dart
class TimerWidget extends StatefulWidget {
  @override
  State<TimerWidget> createState() => _TimerState();
}

class _TimerState extends State<TimerWidget> {
  int _seconds = 0;
  @override
  void initState() {
    super.initState();
    Timer.periodic(Duration(seconds: 1), (_) {
      setState(() => _seconds++);
    });
  }
  @override
  Widget build(BuildContext context) {
    return Text('$_seconds 秒');
  }
}
```

## InheritedWidget

Flutter 中實作狀態共享的底層機制。Provider 正是基於 InheritedWidget 封裝而來。當 InheritedWidget 更新時，所有依賴它的子 Widget 會自動重建。

## 關鍵設計原則

- Widget 應為純函式：給定相同輸入，輸出相同 UI
- 盡量使用 StatelessWidget，必要時才用 StatefulWidget
- 將狀態上移，讓 Widget 保持無狀態

- https://www.google.com/search?q=Flutter+Widget+tree+Element+RenderObject
- https://www.google.com/search?q=Flutter+StatelessWidget+StatefulWidget+difference
