# 文章 2：Dart 變數與非同步

## 變數宣告

Dart 是強型別語言，支援型別推斷與明確型別宣告。

```dart
void main() {
  // 基本型別
  String name = 'Flutter';
  int version = 3;
  double pi = 3.14;
  bool isStable = true;

  // 型別推斷
  var framework = 'Flutter';     // 推斷為 String
  final releaseYear = 2024;      // 不可變，執行期賦值
  const company = 'Google';      // 不可變，編譯期常數

  print('$framework $version.$releaseYear');
}
```

## 集合

```dart
var list = [1, 2, 3];                    // List<int>
var map = {'key': 'value'};              // Map<String, String>
var set = {1, 2, 3};                     // Set<int>
list.add(4);
```

## 函式

Dart 支援頂層函式、匿名函式、箭頭語法。

```dart
int add(int a, int b) => a + b;

var multiply = (int a, int b) => a * b;

void main() {
  var numbers = [1, 2, 3, 4];
  var doubled = numbers.map((n) => n * 2).toList();
}
```

## 非同步基礎

`Future` 代表一個 eventual value，`async`/`await` 讓非同步程式碼看起來像同步。

```dart
Future<String> fetchUserData() async {
  // 模擬網路延遲
  await Future.delayed(Duration(seconds: 2));
  return '用戶資料';
}

Future<void> main() async {
  print('開始讀取...');
  var data = await fetchUserData();
  print('讀取完成: $data');
}
```

## Stream

`Stream` 代表一連串的非同步事件序列。

```dart
Stream<int> countStream(int max) async* {
  for (int i = 1; i <= max; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i;  // 發出一個值
  }
}

void main() async {
  await for (var num in countStream(5)) {
    print(num);  // 每秒輸出 1, 2, 3, 4, 5
  }
}
```

- https://www.google.com/search?q=Dart+async+await+stream+tutorial
- https://www.google.com/search?q=Dart+variables+types+null+safety
