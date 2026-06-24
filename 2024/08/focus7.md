# 焦點 7：效能優化與發布

## 效能分析工具

### Flutter DevTools

Flutter DevTools 是效能分析的核心工具，支援：

- **效能覆蓋圖**（Performance Overlay）：檢視 UI 與光柵化幀率
- **Widget Inspector**：檢視 Widget 樹結構與重建次數
- **CPU Profiler**：定位耗時方法
- **Memory Profiler**：監控記憶體使用與洩漏
- **Network Profiler**：檢視 HTTP 請求

## 常見效能問題

### 1. 不必要的 Widget 重建

使用 `const` 關鍵字建立編譯期常數 Widget，避免重建。

```dart
const Text('不會重建');
```

### 2. 圖片快取

```dart
// 使用 cached_network_image 套件
CachedNetworkImage(imageUrl: 'https://example.com/large.jpg')
```

### 3. 長列表優化

ListView.builder 只建構可見項目的 Widget，避免一次性建立所有項目。

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ListTile(title: Text(items[index])),
)
```

### 4. 避免耗時操作在主 Isolate

使用 `compute()` 將耗時工作移至背景 Isolate。

```dart
final result = await compute(heavyFunction, data);
```

## 建置模式

Flutter 支援三種建置模式：

| 模式 | 命令 | 用途 |
|------|------|------|
| Debug | `flutter run` | 開發除錯，Hot Reload |
| Profile | `flutter run --profile` | 效能分析 |
| Release | `flutter build apk` | 上架發布 |

## APK 與 App Bundle

Google Play 強制要求使用 Android App Bundle（AAB）格式上架。Flutter 支援兩種格式：

```bash
flutter build apk          # APK（可直接安裝）
flutter build appbundle    # AAB（Play 商店要求）
```

## iOS 發布

```bash
flutter build ios
# 然後在 Xcode 中 Archive → Distribute
```

## 應用體積最佳化

- 使用 `--split-debug-info` 分離除錯資訊
- 啟用 `--obfuscate` 混淆程式碼
- 刪除未使用的圖示字型
- 將大資源放在網路，執行時期下載

- https://www.google.com/search?q=Flutter+performance+optimization+2024
- https://www.google.com/search?q=Flutter+release+APK+IPA+build+guide
