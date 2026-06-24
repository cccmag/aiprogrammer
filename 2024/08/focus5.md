# 焦點 5：導航與路由

## Navigator 1.0（傳統路由）

Flutter 的傳統導航方式使用 `Navigator.push()` 與 `Navigator.pop()` 管理路由棧。

```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => DetailPage()),
);

Navigator.pop(context);
```

### 命名路由

可將路由集中定義：

```dart
MaterialApp(
  routes: {
    '/': (context) => HomePage(),
    '/detail': (context) => DetailPage(),
  },
)
```

命名路由的缺點是無法傳遞複雜參數，且缺乏深層連結支援。

## Navigator 2.0（宣告式路由）

Flutter 1.22 引入 Navigator 2.0，採用宣告式 API，開發者透過 `Page` 列表控制路由狀態。這讓 Flutter 可以更好地處理瀏覽器風格的導航、深層連結與多視窗情境。

```dart
Navigator(
  pages: [
    MaterialPage(child: HomePage()),
    if (showDetail) MaterialPage(child: DetailPage()),
  ],
  onPopPage: (route, result) => route.didPop(result),
)
```

Navigator 2.0 較為底層，多數專案會使用更高層的封裝。

## GoRouter（官方推薦）

GoRouter 是 Flutter 團隊維護的路由套件，基於 Navigator 2.0 封裝，提供簡潔的宣告式 API。

```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(path: '/', builder: (context, state) => HomePage()),
    GoRoute(
      path: '/detail/:id',
      builder: (context, state) => DetailPage(id: state.pathParameters['id']!),
    ),
  ],
);
```

### GoRouter 特性

- 路徑參數與查詢參數支援
- 深層連結（Deep Link）自動處理
- 重導向（Redirect）機制
- 巢狀路由（ShellRoute）
- 錯誤頁面自訂

## 路由選擇建議

- 小型 App：Navigator 1.0 足夠
- 需要深層連結：GoRouter 為最佳選擇
- 自訂導航行為：Navigator 2.0 提供最大彈性

- https://www.google.com/search?q=Flutter+GoRouter+tutorial
- https://www.google.com/search?q=Flutter+Navigator+2.0+vs+1.0
