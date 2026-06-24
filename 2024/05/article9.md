# 相機與地理位置

## 善用手機的硬體能力

手機 App 的魅力在於可以存取裝置的硬體功能——相機、GPS、陀螺儀等。React Native 提供統一的 API 來使用這些功能。本文將實戰相機拍照與地理位置追蹤。

## 權限處理

在 iOS 和 Android 上使用敏感硬體前，必須先請求使用者權限：

```bash
npm install react-native-permissions
```

```jsx
import { Platform, Alert, Linking } from "react-native";
import { check, request, PERMISSIONS, RESULTS } from "react-native-permissions";

const requestCameraPermission = async () => {
    const permission = Platform.select({
        ios: PERMISSIONS.IOS.CAMERA,
        android: PERMISSIONS.ANDROID.CAMERA,
    });

    const result = await check(permission);

    switch (result) {
        case RESULTS.GRANTED:
            return true;
        case RESULTS.DENIED:
            const requestResult = await request(permission);
            return requestResult === RESULTS.GRANTED;
        case RESULTS.BLOCKED:
            Alert.alert(
                "需要相機權限",
                "請前往設定開啟相機權限",
                [
                    { text: "取消" },
                    { text: "前往設定", onPress: Linking.openSettings },
                ]
            );
            return false;
    }
};
```

## 相機功能實作

使用 `react-native-vision-camera` 套件：

```bash
npm install react-native-vision-camera
```

### 拍照功能

```jsx
import { Camera, useCameraDevice, useCameraPermission } from "react-native-vision-camera";
import { useState, useRef } from "react";
import { View, TouchableOpacity, StyleSheet } from "react-native";

const CameraScreen = () => {
    const camera = useRef(null);
    const [cameraPosition, setCameraPosition] = useState("back");
    const device = useCameraDevice(cameraPosition);
    const { hasPermission, requestPermission } = useCameraPermission();

    const takePhoto = async () => {
        try {
            const photo = await camera.current.takePhoto({
                qualityPrioritization: "quality",
                flash: "off",
            });
            // photo.path 為照片檔案路徑
            // 可以儲存或上傳
            console.log("照片儲存於:", photo.path);
        } catch (error) {
            console.error("拍照失敗:", error);
        }
    };

    const flipCamera = () => {
        setCameraPosition((p) =>
            p === "back" ? "front" : "back"
        );
    };

    if (!hasPermission) {
        return (
            <View style={styles.container}>
                <TouchableOpacity onPress={requestPermission}>
                    <Text>授予相機權限</Text>
                </TouchableOpacity>
            </View>
        );
    }

    if (!device) {
        return <View style={styles.container}><Text>找不到相機</Text></View>;
    }

    return (
        <View style={styles.container}>
            <Camera
                ref={camera}
                style={StyleSheet.absoluteFill}
                device={device}
                isActive={true}
                photo={true}
            />
            <View style={styles.controls}>
                <TouchableOpacity style={styles.captureBtn} onPress={takePhoto} />
                <TouchableOpacity style={styles.flipBtn} onPress={flipCamera}>
                    <Text>翻轉</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};
```

### 掃描 QR Code

```bash
npm install react-native-vision-camera
npm install react-native-qrcode-scanner
```

```jsx
import { useScanBarcodes, BarcodeFormat } from "react-native-vision-camera";

const ScannerScreen = () => {
    const [{}, frames] = useScanBarcodes([BarcodeFormat.QR_CODE], {
        checkInverted: true,
    });

    return (
        <Camera
            style={StyleSheet.absoluteFill}
            device={device}
            isActive={true}
            frameProcessor={frames}
        />
    );
};
```

## 地理位置

### 單次定位

```bash
npm install react-native-geolocation-service
npm install @react-native-community/geolocation
```

```jsx
import Geolocation from "react-native-geolocation-service";
import { Platform, Alert } from "react-native";

const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
        Geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy,
                });
            },
            (error) => {
                reject(error);
            },
            {
                enableHighAccuracy: true,
                timeout: 15000,
                maximumAge: 10000,
            }
        );
    });
};
```

### 持續追蹤位置

```jsx
import { useState, useEffect, useRef } from "react";
import Geolocation from "react-native-geolocation-service";
import { View, Text, Button, StyleSheet } from "react-native";

const LocationTracker = () => {
    const [location, setLocation] = useState(null);
    const [path, setPath] = useState([]);
    const watchId = useRef(null);

    const startTracking = () => {
        Geolocation.requestAuthorization("always");

        watchId.current = Geolocation.watchPosition(
            (position) => {
                const newPoint = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    timestamp: position.timestamp,
                };
                setLocation(newPoint);
                setPath((prev) => [...prev, newPoint]);
            },
            (error) => console.error(error),
            {
                enableHighAccuracy: true,
                distanceFilter: 5,      // 每 5 公尺更新一次
                interval: 2000,          // Android 最小更新間隔
                fastestInterval: 1000,   // Android 最快更新間隔
            }
        );
    };

    const stopTracking = () => {
        if (watchId.current !== null) {
            Geolocation.clearWatch(watchId.current);
            watchId.current = null;
        }
    };

    useEffect(() => {
        return () => stopTracking();
    }, []);

    return (
        <View style={styles.container}>
            {location && (
                <>
                    <Text>緯度: {location.latitude.toFixed(6)}</Text>
                    <Text>經度: {location.longitude.toFixed(6)}</Text>
                    <Text>已記錄 {path.length} 個位置點</Text>
                </>
            )}
            <Button
                title={watchId.current ? "停止" : "開始追蹤"}
                onPress={watchId.current ? stopTracking : startTracking}
            />
        </View>
    );
};
```

## 整合地圖顯示

```bash
npm install react-native-maps
```

```jsx
import MapView, { Marker, Polyline } from "react-native-maps";

const MapScreen = ({ path }) => (
    <MapView
        style={StyleSheet.absoluteFill}
        initialRegion={{
            latitude: 25.033,
            longitude: 121.565,
            latitudeDelta: 0.01,
            longitudeDelta: 0.01,
        }}
        showsUserLocation={true}
        followUserLocation={true}
    >
        <Marker
            coordinate={{
                latitude: 25.033,
                longitude: 121.565,
            }}
            title="目前位置"
        />
        <Polyline
            coordinates={path}
            strokeColor="#007AFF"
            strokeWidth={3}
        />
    </MapView>
);
```

---

## 延伸閱讀

- [react-native-vision-camera](https://www.google.com/search?q=react-native-vision-camera)
- [react-native-maps](https://www.google.com/search?q=react-native-maps)
- [Geolocation API 文件](https://www.google.com/search?q=Geolocation+API+React+Native)
