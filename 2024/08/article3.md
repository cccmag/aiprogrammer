# 文章 3：StatelessWidget vs StatefulWidget

## 選擇的關鍵

Widget 分為兩大類：StatelessWidget（無狀態）與 StatefulWidget（有狀態）。選擇時應遵循「盡量無狀態」原則。

## StatelessWidget

當 Widget 的 UI 完全由傳入的參數決定，且不會隨時間改變時使用。

```dart
class ProfileAvatar extends StatelessWidget {
  final String imageUrl;
  final double size;

  ProfileAvatar({required this.imageUrl, this.size = 48});

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      radius: size / 2,
      backgroundImage: NetworkImage(imageUrl),
    );
  }
}
```

特點：
- 單一 `build()` 方法
- 不包含可變狀態
- 效能較佳，重建成本低

## StatefulWidget

當 Widget 需要維護可變狀態、響應用戶互動或監聽資料變更時使用。

```dart
class LikeButton extends StatefulWidget {
  @override
  State<LikeButton> createState() => _LikeButtonState();
}

class _LikeButtonState extends State<LikeButton> {
  bool _isLiked = false;
  int _likeCount = 0;

  void _toggleLike() {
    setState(() {
      _isLiked = !_isLiked;
      _likeCount += _isLiked ? 1 : -1;
    });
  }

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(_isLiked ? Icons.favorite : Icons.favorite_border),
      onPressed: _toggleLike,
    );
  }
}
```

## 生命週期

StatefulWidget 的 State 物件有明確的生命週期：

1. **createState** — 建立 State 物件
2. **initState** — 初始化，僅執行一次
3. **didChangeDependencies** — 依賴的 InheritedWidget 變更時
4. **build** — 建構 UI（可多次調用）
5. **didUpdateWidget** — Widget 配置變更時
6. **setState** — 觸發重建
7. **dispose** — 永久銷毀

## 實務建議

- 預設使用 StatelessWidget
- 僅在處理動態資料、動畫、表單輸入時使用 StatefulWidget
- 使用 `const` 建構 StatelessWidget 以利 Flutter 優化
- 將業務邏輯抽取至 Controller / ViewModel，保持 Widget 簡潔

- https://www.google.com/search?q=Flutter+StatelessWidget+vs+StatefulWidget+lifecycle
- https://www.google.com/search?q=Flutter+StatefulWidget+lifecycle+methods
