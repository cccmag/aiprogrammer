# 原生模組與 API 串接

## 為什麼需要原生模組？

React Native 的核心是一個 JavaScript 執行環境與原生端的橋樑。當 React Native 沒有提供特定 API 時——例如藍牙、NFC、複雜的感測器——開發者需要編寫原生模組。

### 舊架構：Bridge

在舊架構中，JavaScript 與原生端透過 Bridge 通訊：

```
JS Thread ──序列化 JSON──→ Bridge ──反序列化──→ Native Thread
Native Thread ──序列化──→ Bridge ──反序列化──→ JS Thread
```

Bridge 的序列化/反序列化是效能瓶頸，特別是需要大量資料交換的場景。

### 新架構：JSI + TurboModules

新架構使用 JavaScript Interface（JSI），允許直接引用原生物件：

```
JS Thread ──JSI 直接呼叫──→ Native 方法
（無需序列化，無需 Bridge）
```

## 使用第三方套件

大多數情況下不需要自己寫原生模組。React Native 生態系已有大量封裝好的套件：

```bash
# 相機
npm install react-native-vision-camera

# 地理位置
npm install react-native-geolocation-service
npm install @react-native-community/geolocation

# 生物辨識
npm install react-native-biometrics

# 本地通知
npm install @notifee/react-native

# 檔案系統
npm install react-native-fs

# 分享
npm install react-native-share
```

## 整合相機功能

```jsx
import { Camera, useCameraDevice } from "react-native-vision-camera";
import { useState, useEffect } from "react";
import { View, Button, StyleSheet } from "react-native";

const CameraScreen = () => {
    const [hasPermission, setHasPermission] = useState(false);
    const device = useCameraDevice("back");

    useEffect(() => {
        (async () => {
            const permission = await Camera.requestCameraPermission();
            setHasPermission(permission === "granted");
        })();
    }, []);

    if (!device || !hasPermission) {
        return <View><Text>需要相機權限</Text></View>;
    }

    return (
        <View style={styles.container}>
            <Camera
                style={StyleSheet.absoluteFill}
                device={device}
                isActive={true}
                photo={true}
            />
        </View>
    );
};
```

## 地理位置 API

```jsx
import Geolocation from "@react-native-community/geolocation";
import { useState, useEffect } from "react";
import { View, Text, Button } from "react-native";

const LocationTracker = () => {
    const [location, setLocation] = useState(null);
    const [watchId, setWatchId] = useState(null);

    const startTracking = () => {
        Geolocation.requestAuthorization();

        const id = Geolocation.watchPosition(
            (position) => {
                setLocation({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                });
            },
            (error) => console.error(error),
            {
                enableHighAccuracy: true,
                distanceFilter: 10,
                interval: 5000,
            }
        );
        setWatchId(id);
    };

    const stopTracking = () => {
        if (watchId !== null) {
            Geolocation.clearWatch(watchId);
            setWatchId(null);
        }
    };

    useEffect(() => {
        return () => stopTracking();
    }, []);

    return (
        <View>
            {location && (
                <Text>
                    緯度：{location.lat.toFixed(6)}
                    經度：{location.lng.toFixed(6)}
                </Text>
            )}
            <Button
                title={watchId ? "停止追蹤" : "開始追蹤"}
                onPress={watchId ? stopTracking : startTracking}
            />
        </View>
    );
};
```

## 編寫自訂原生模組

當需要封裝 Android/iOS SDK 時，必須編寫原生模組：

### Android（Kotlin）

```kotlin
// ToastModule.kt
package com.myapp.modules

import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod

class ToastModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    override fun getName() = "ToastModule"

    @ReactMethod
    fun show(message: String, duration: Int) {
        android.widget.Toast.makeText(
            reactApplicationContext,
            message,
            duration
        ).show()
    }
}
```

### iOS（Objective-C）

```objc
// ToastModule.m
#import "React/RCTBridgeModule.h"

@interface RCT_EXTERN_MODULE(ToastModule, NSObject)
RCT_EXTERN_METHOD(show:(NSString *)message
                  duration:(int)duration)
@end
```

## TurboModules（新架構）

在新架構中，原生模組透過 JSI 註冊，呼叫更高效：

```typescript
import { TurboModule, TurboModuleRegistry } from "react-native";

interface Spec extends TurboModule {
    readonly getConstants: () => { [key: string]: any };
    show(message: string, duration: number): void;
}

export default TurboModuleRegistry.get<Spec>("ToastModule");
```

---

## 延伸閱讀

- [React Native 原生模組](https://www.google.com/search?q=React+Native+native+modules)
- [TurboModules 架構說明](https://www.google.com/search?q=React+Native+TurboModules)
- [react-native-vision-camera](https://www.google.com/search?q=react-native-vision-camera)

---

*本篇文章為「AI 程式人雜誌 2024 年 5 月號」焦點系列之六。*
