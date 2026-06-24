# 焦點 4：狀態管理 — Provider / Riverpod

## 為什麼需要狀態管理？

當 App 規模增長，元件之間共享狀態的需求愈發複雜。簡單的 `setState()` 無法滿足跨頁面資料傳遞、多 Widget 同步更新的需求。

## Provider

Provider 是目前 Flutter 生態中最廣泛使用的狀態管理方案。它封裝了 InheritedWidget，提供簡單的依賴注入與狀態監聽。

### ChangeNotifier + Consumer

```dart
class Counter extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  void increment() { _count++; notifyListeners(); }
}

// 在 Widget 中使用
Consumer<Counter>(
  builder: (context, counter, child) {
    return Text('${counter.count}');
  },
)
```

### MultiProvider

多個 Provider 可以嵌套組合：

```dart
MultiProvider(
  providers: [
    ChangeNotifierProvider(create: (_) => Counter()),
    ChangeNotifierProvider(create: (_) => TodoModel()),
  ],
  child: MyApp(),
)
```

## Riverpod

Riverpod 是 Provider 的進化版，由同一作者維護，解決了 Provider 的多個痛點：

- 編譯期安全：不再有 `ProviderNotFoundException`
- 無需 BuildContext：狀態可脫離 Widget 樹存取
- 自動銷毀：狀態在不需要時自動清理
- 支援族裔參數：可建立參數化的 Provider

```dart
final counterProvider = StateNotifierProvider<Counter, int>((ref) {
  return Counter();
});

// 讀取
final count = ref.watch(counterProvider);
// 寫入
ref.read(counterProvider.notifier).increment();
```

## 選擇指南

| 情境 | 建議方案 |
|------|----------|
| 小型專案、局部狀態 | setState |
| 中等規模、頁面間共享 | Provider / ChangeNotifier |
| 大型專案、複雜依賴 | Riverpod / BLoC |
| 即時資料流 | StreamProvider / BLoC |

- https://www.google.com/search?q=Flutter+Provider+vs+Riverpod+2024
- https://www.google.com/search?q=Flutter+state+management+comparison
