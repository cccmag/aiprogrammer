# 行動開發年度觀察

## 前言

2015 年是行動開發領域變革的一年。Swift 的開源、React Native 的發布、跨平台開發框架的興起，都在重新定義行動應用開發的方式。

## Swift 開放源代碼

### 12 月的重大宣布

Apple 在 2015 年 12 月的 WWDC 上宣布 Swift 正式開源，這是 Apple 有史以來最重要的開源決定之一：

- **Linux 支援**：Swift 可以在 Linux 上運行
- **社群參與**：允許開發者貢獻語言發展
- **開源網站**：swift.org 上線

### Swift 開源的影響

#### 對開發者的影響

1. **更多平台選擇**：Swift 不再只限於 Apple 平台
2. **社群參與**：開發者可以貢獻標準備 Library
3. **學習價值**：Swift 成為系統程式設計的選擇

#### 對生態的影響

1. **伺服器端 Swift**： Vapor、Perfect 等框架出現
2. **跨平台開發**：用 Swift 開發 Android 應用
3. **工具鏈完善**：Linux 上的開發體驗改善

### Swift 2.2

在開源前，Swift 2.2 發布了多項改進：

```swift
// 關鍵字作參數標籤（允許使用 #）
func greet(#name: String) {
    print("Hello, \(name)")
}

// 錯誤處理關鍵字統一
enum NetworkError: Error {
    case badResponse
    case noConnection
}

// 編譯器診斷改進
```

## React Native

### 發布與成長

React Native 在 2015 年正式發布，引發了轟動：

- **1 月**：React Native 開源
- **3 月**：支援 Android
- **9 月**：React Native 0.11 發布

### 核心概念

```javascript
// React Native 元件
import React, { Component } from 'react';
import { View, Text, Image } from 'react-native';

class HelloWorld extends Component {
  render() {
    return (
      <View>
        <Text>Hello, World!</Text>
      </View>
    );
  }
}
```

### 與傳統開發的比較

| 面向 | 原生開發 | React Native |
|------|---------|-------------|
| 效能 | 最優 | 接近原生 |
| 學習曲線 | 陡 | 中等 |
| 程式碼共用 | 0% | 60-80% |
| 維護成本 | 高 | 中 |
| 生態成熟度 | 成熟 | 成長中 |

## 跨平台開發趨勢

### 主要框架比較

| 框架 | 語言 | 渲染方式 | 代表應用 |
|------|------|---------|---------|
| React Native | JavaScript | 原生元件 | Facebook |
| Xamarin | C# | 原生控制項 | Slack |
| Flutter | Dart | 自繪 | Alibaba |
| Ionic | JavaScript | WebView | 多個應用 |

### 2015 年的變化

- **Xamarin 收購**：Microsoft 宣布收購 Xamarin（2016 年完成）
- **Ionic 成熟**：v1.0 發布
- **Cordova vs Ionic**：Ionic 逐步取代 Cordova

## iOS 9 新特性

### Swift 相關

- **App Extensions**：分享、鍵盤擴展
- **Multi-tasking**：Split View、Slide Over
- **Search APIs**：Spotlight 整合
- **3D Touch**：Peek 和 Pop

### Apple Pay

```swift
// Apple Pay 整合
import PassKit

class PaymentViewController: UIViewController, PKPaymentAuthorizationViewControllerDelegate {
    func pay() {
        let request = PKPaymentRequest()
        request.merchantIdentifier = "merchant.com.example"
        request.supportedNetworks = [.visa, .masterCard]
        request.merchantCapabilities = .capability3DS
        request.countryCode = "US"
        request.currencyCode = "USD"

        let payment = PKPaymentRequest()
        // ...
    }
}
```

## Android Studio 進展

### 1.4/1.5 版本

- **Gradle 改進**：更快的建構速度
- **Vector Assets**：向量圖形支援
- **Data Binding**：宣告式 UI 開發
- **Memory Monitor**：效能分析工具

### Material Design

Material Design 逐步成為 Android 應用標準：

```xml
<android.support.design.widget.FloatingActionButton
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:src="@drawable/ic_add"
    app:fabSize="normal" />
```

## Windows 10 與 UWP

### 單一平台策略

Windows 10 推動了 UWP（Universal Windows Platform）的發展：

- **單一碼基底**：PC、平板、手機通用
- **Continuum**：手機當電腦用
- **HoloLens**：擴增實境應用

### Cordova for Windows

使用 Cordova 開發 Windows 應用：

```bash
cordova platform add windows
cordova build windows
```

## 未來展望

### 2016 年預期

1. **Swift 3.0**：語法改進和標準化
2. **React Native 成熟**：更多企業採用
3. **跨平台框架整合**：Xamarin、Ionic 進一步發展
4. **Instant Apps**：Google 推動的即時應用
5. **WWDC 2016**：iOS 10 和 Swift 3

## 小結

2015 年行動開發領域經歷了重要變化：

- **Swift 開源**：開啟了新的可能性
- **React Native**：用 JavaScript 開發原生應用
- **跨平台成熟**：開發者有更多選擇
- **平台整合**：iOS、Android、Windows 互通性增加

行動開發的未來將更加多元和開放。

---

## 延伸閱讀

- [Swift Open Source](https://www.google.com/search?q=Swift+open+source+apple)
- [React Native Tutorial](https://www.google.com/search?q=React+Native+tutorial)
- [Cross-Platform Mobile Development](https://www.google.com/search?q=cross+platform+mobile+development+comparison)