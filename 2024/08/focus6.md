# 焦點 6：原生平台通道

## 什麼是平台通道？

Flutter 本身不直接存取平台 API（如相機、藍牙、指紋辨識）。平台通道（Platform Channel）是 Flutter 與原生（Android / iOS）之間的雙向通訊機制。

## MethodChannel

最常用的通道類型。Flutter 端調用方法，原生端執行後返回結果。

### Flutter 端

```dart
static const platform = MethodChannel('com.example/battery');

Future<String> getBatteryLevel() async {
  final result = await platform.invokeMethod('getBatteryLevel');
  return result;
}
```

### Android 端 (Kotlin)

```kotlin
MethodChannel(flutterEngine.dartExecutor, "com.example/battery").setMethodCallHandler {
  call, result ->
  if (call.method == "getBatteryLevel") {
    val batteryLevel = getBatteryLevel()
    result.success(batteryLevel)
  }
}
```

### iOS 端 (Swift)

```swift
let channel = FlutterMethodChannel(name: "com.example/battery",
                                    binaryMessenger: controller.binaryMessenger)
channel.setMethodCallHandler { call, result in
  if call.method == "getBatteryLevel" {
    result(getBatteryLevel())
  }
}
```

## EventChannel

用於持續性的資料串流，如感測器資料、位置更新。

```dart
const eventChannel = EventChannel('com.example/sensor');
eventChannel.receiveBroadcastStream().listen((data) {
  print(data);
});
```

## BasicMessageChannel

在 Flutter 與原生之間傳送字串或位元組訊息，適合需要自訂序列化協議的場景。

```dart
const messageChannel = BasicMessageChannel('com.example/messages',
    StandardMessageCodec());
messageChannel.send('Hello from Flutter');
```

## Pigeon：型別安全的通道

手動維護 MethodChannel 的 Flutter 與原生端程式碼容易出錯。Pigeon 是官方推出的程式碼產生工具，透過一個 dart 定義檔自動生成雙平台程式碼。

```dart
// 定義檔 (pigeon/messages.dart)
@HostApi()
abstract class BatteryApi {
  int getBatteryLevel();
}
```

執行 `flutter pub run pigeon` 後自動產生 Flutter 端與原生端的型別安全程式碼。

## 最佳實務

- 通道名稱使用反轉網域名稱避免衝突
- 非同步操作使用 async/await 並處理逾時
- 序列化大量資料時考慮使用檔案路徑傳遞
- 優先使用社群套件（如 camera、geolocator）而非自行實作

- https://www.google.com/search?q=Flutter+platform+channel+MethodChannel+tutorial
- https://www.google.com/search?q=Flutter+Pigeon+package
