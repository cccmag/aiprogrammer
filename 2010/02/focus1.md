# 主題一：Android 2.1/2.2 新特性

## Android 2.1 (Eclair)

### 發布背景

Android 2.1 在 2009 年 12 月發布，2010 年 1-2 月成為主流。這是 Android 系統成熟的重要階段。

```
Android 2.1 時間線：
───────────────────
2009/12:  Nexus One 發布，搭載 Android 2.1
2010/01:  OTA 升級開始推送
2010/02:  新出廠手機預設 2.1
```

### 主要新功能

**即時桌布（Live Wallpapers）**

```java
// Live Wallpaper 開發
public class MyWallpaperService extends WallpaperService {
    @Override
    public Engine onCreateEngine() {
        return new MyWallpaperEngine();
    }

    class MyWallpaperEngine extends WallpaperService.Engine {
        @Override
        public void onSurfaceCreated(SurfaceHolder holder) {
            super.onSurfaceCreated(holder);
            // 初始化繪圖
        }

        @Override
        public void onSurfaceChanged(SurfaceHolder holder,
                int format, int width, int height) {
            // 處理尺寸變化
        }

        @Override
        public void onDraw(SurfaceHolder holder,
                Canvas canvas) {
            // 繪製每幀
            canvas.drawColor(Color.BLUE);
        }
    }
}
```

```xml
<!-- AndroidManifest.xml -->
<service
    android:name=".MyWallpaperService"
    android:permission="android.permission.BIND_WALLPAPER">
    <intent-filter>
        <action android:name="android.service.wallpaper.WallpaperService" />
    </intent-filter>
    <meta-data
        android:name="android.service.wallpaper"
        android:resource="@xml/my_wallpaper" />
</service>
```

**多點觸控支援**

```java
// 偵測多點觸控
public boolean onTouchEvent(MotionEvent event) {
    int action = event.getActionMasked();

    switch (action) {
        case MotionEvent.ACTION_DOWN:
            // 第一指按下
            break;

        case MotionEvent.ACTION_POINTER_DOWN:
            // 第二指按下
            int index = event.getActionIndex();
            float x = event.getX(index);
            float y = event.getY(index);
            break;

        case MotionEvent.ACTION_MOVE:
            // 多點移動
            for (int i = 0; i < event.getPointerCount(); i++) {
                int id = event.getPointerId(i);
                float x = event.getX(i);
                float y = event.getY(i);
            }
            break;

        case MotionEvent.ACTION_UP:
        case MotionEvent.ACTION_POINTER_UP:
            // 手指釋放
            break;
    }

    return true;
}
```

### 效能改進

```
2.1 效能提升：
──────────────────
啟動速度：   加快 20%
應用啟動：   加快 15%
記憶體管理： 改善穩定性
Java 執行：  更快 Dalvik VM
```

## Android 2.2 (Froyo)

### 發布時間線

Android 2.2（Froyo）在 2010 年 5 月正式發布，但 2 月已開始 Beta 測試。

```
Android 2.2 預計新特性（當時猜測）：
───────────────────────────────
Flash 支援：       Flash Player 10.1
效能提升：         JIT 編譯器
個人熱點：         Wi-Fi 與 USB 熱點
App2SD：           將應用移到 SD 卡
雲端同步：         聯絡人、日曆同步
```

### JIT 編譯器

```
Dalvik JIT 編譯器：
──────────────────
什麼是 JIT：  Just-In-Time 編譯
效果：        執行速度提升 2-5 倍
原理：        位元組碼轉為機器碼
支援：        從 2.2 開始內建
```

### 網頁瀏覽器改進

```javascript
// Android 2.2 瀏覽器支援
// V8 JavaScript 引擎更新
// 硬體加速渲染
// 完整的 HTML5 支援（部分）
```

## API 變化

### 2.1 新增 API

```
新 API 類別（2.1）：
──────────────────
android.service.wallpaper：  即時桌布
android.bluetooth：           藍牙控制
android.hardware.Camera：    臉部偵測
android.webkit：             HTML5 視訊
```

### 2.2 預期 API

```
預期新 API（2.2）：
──────────────────
android.net.wifi：           Wi-Fi 熱點
android.app.backup：         備份 API
android.webkit：             更好的 HTML5
dalvik.system：             JIT 控制
```

## 版本相容性

### 向下相容

```java
// 使用版本判斷確保相容
private void setupCamera() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.ECLAIR) {
        // 使用 2.0+ API
        enableAdvancedCamera();
    } else {
        // 回退到基本功能
        enableBasicCamera();
    }
}
```

### Feature Detection

```xml
<!-- 使用uses-feature控制安裝資格 -->
<uses-feature android:name="android.hardware.camera"
              android:required="false" />

<uses-feature android:name="android.hardware.touchscreen.multitouch"
              android:required="false" />
```

## 升級策略

### OTA 升級

```
Android 版本升級現況（2010年）：
───────────────────────────────
HTC：  可升級 2.1（部分 2.2）
Motorola： 可升級 2.1
Samsung：  可升級 2.1
Sony Ericsson： 2.1 進行中
```

### 開發者應對

```java
// 檢查系統版本
if (Build.VERSION.SDK_INT < Build.VERSION_CODES.ECLAIR_MR1) {
    // 低於 2.1 的處理
    showUpgradeDialog();
}

// 使用 @TargetApi 標記新 API
@TargetApi(Build.VERSION_CODES.ECLAIR)
private void newApiMethod() {
    // 2.1+ 才能使用
}
```

---

## 結論

Android 2.1 和 2.2 是系統成熟的關鍵版本。即時桌布、多點觸控、JIT 編譯器等功能的加入，讓 Android 的功能大幅提升，也為開發者提供了更豐富的 API。

版本碎片化仍是問題，但 Google 和 OEM 廠商正在努力改善升級體驗。

---

*本期文章到此結束。*