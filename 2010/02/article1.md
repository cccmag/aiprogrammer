# Android 2.1 發布：效能大幅提升

## Android 2.1 (Eclair) 發布

### 發布背景

2010 年 1 月，Google 正式發布 Android 2.1，這是 Android 系統走向成熟的重要里程碑。

```
Android 2.1 發布重點：
───────────────────────────
發布時間：     2009 年 12 月（ Nexus One 搭載）
主要提升：     效能、穩定性、新功能
適用裝置：     Nexus One、部分 HTC 裝置
升級推送：     2010 年 1-2 月
```

## 主要新功能

### 即時桌布（Live Wallpapers）

即時桌布是 2.1 最視覺化的新功能：

```
即時桌布功能：
───────────────────────────
WallpaperService API： 允許第三方開發
視覺效果：      3D 背景、粒子效果
效能：         需要 GPU 支援
受歡迎程度：    非常高
```

### 多點觸控

```
多點觸控支援：
───────────────────────────
支援裝置：     Nexus One、部分 Droid
API：          MotionEvent 擴展
應用場景：     圖片縮放、遊戲
限制：         並非所有應用都支援
```

## 效能提升

### Dalvik VM 優化

```
VM 效能改進：
───────────────────────────
啟動速度：     加快 20%
記憶體管理：   更穩定
Java 執行：    更快
GC 改進：      減少卡頓
```

### 瀏覽器改進

```
瀏覽器更新：
───────────────────────────
V8 引擎更新：  JavaScript 更快
HTML5 支援：   視訊、Canvas 部分支援
外掛支援：     Flash 10.1 預備
```

## API 改進

### 新增 API

```
2.1 新增 API：
───────────────────────────
Bluetooth A2DP：    藍牙音訊設定檔
Camera Face Detection： 相機臉部偵測
Wallpaper Service： 即時桌布 API
Voice Recognition： 語音辨識
```

### 臉部偵測 API

```java
// 臉部偵測範例
Camera camera = Camera.open();
Camera.Parameters params = camera.getParameters();

List<Camera.Face> faces = params.getSupportedFaces();
if (faces != null && faces.size() > 0) {
    params.setFaceDetection("on");
    camera.setFaceDetectionListener(new Camera.FaceDetectionListener() {
        @Override
        public void onFaceDetection(Camera.Face[] faces, Camera camera) {
            for (Camera.Face face : faces) {
                Rect rect = face.rect;
                // 繪製對焦框
            }
        }
    });
    camera.startFaceDetection();
}
```

## 升級情況

### 官方升級

```
Android 2.1 升級時間線：
───────────────────────────
Nexus One：     發布時即為 2.1
HTC Droid：     2010 年 1 月
HTC Incredible： 發布時即為 2.1
其他：         陸續升級中
```

### 非官方升級

```
社群 ROM：
───────────────────────────
CyanogenMod：   提供 2.1 給更多裝置
其他 ROM：       陸續支援
風險：          可能影響保固
```

## 對開發者的影響

### 開發考量

```
開發者需注意：
───────────────────────────
最小 SDK 版本：  7 (2.1)
target SDK：     7
編譯 SDK：       7
使用新 API：     需要版本檢查
```

### 相容性處理

```java
// 版本檢查範例
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.ECLAIR) {
    // 使用 2.1+ API
    enableMultiTouch();
}
```

---

## 結論

Android 2.1 是系統成熟的重要版本。即時桌布和多點觸控提升了使用者體驗，效能優化讓系統更加流暢。雖然仍有升級延遲問題，但 Google 和 OEM 廠商正在改善。

---

*本期文章到此結束。*