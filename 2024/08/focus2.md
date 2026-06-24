# 焦點 2：Dart 語言基礎

## Dart 簡介

Dart 由 Google 開發，是 Flutter 的程式語言。它結合了 JavaScript 的靈活性與 Java 的嚴謹型別系統，支援 JIT（開發期）與 AOT（發布期）雙重編譯模式。

## 變數與型別

```dart
// 型別推斷
var name = 'Flutter';  // String
final age = 10;        // int, 不可變
const pi = 3.14159;    // 編譯期常數

// 明確型別
String greeting = 'Hello';
int count = 42;
double height = 1.75;
bool isActive = true;
```

## 萬用型別與集合

```dart
List<String> items = ['A', 'B', 'C'];
Map<String, int> scores = {'Alice': 95, 'Bob': 87};
Set<int> uniqueIds = {1, 2, 3};

// 擴展運算子
var all = [...items, 'D'];
```

## 類別與繼承

Dart 是純物件導向語言，所有類別繼承自 Object。支援 mixin 機制實現程式碼重用。

```dart
abstract class Animal {
  void speak();
}

mixin Flyable {
  void fly() => print('飛翔中');
}

class Bird extends Animal with Flyable {
  @override
  void speak() => print('啾啾');
}
```

## Null Safety

Dart 2.12 引入 Sound Null Safety。型別預設不可為 null，需加上 `?` 標記可空型別。

```dart
String? nullableName;
nullableName?.length;    // 安全存取
nullableName ?? '預設值'; // 空值合併
```

## 非同步程式設計

```dart
Future<String> fetchData() async {
  final response = await http.get(Uri.parse('...'));
  return response.body;
}

Stream<int> countStream() async* {
  for (int i = 0; i < 10; i++) {
    yield i;
  }
}
```

- https://www.google.com/search?q=Dart+language+tutorial+2024
- https://www.google.com/search?q=Dart+null+safety+guide
