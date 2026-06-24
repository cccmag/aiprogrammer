# 主題三：手機硬體規格競賽

## 2010 年硬體概況

### 旗艦手機規格

```
主要旗艦手機比較（2010 年 2 月）：
─────────────────────────────────────
             Nexus One    Droid     iPhone 3GS
處理器：     1GHz Snapdragon  600MHz OMAP3  600MHz Cortex
記憶體：     512MB          256MB     256MB
儲存：       512MB+32GB    16GB      16GB/32GB
螢幕：       3.7"AMOLED   3.7" LCD  3.5" LCD
解析度：     800x480       854x480   480x320
相機：       5MP          5MP       3MP
```

## 處理器發展

### 2010 年主要處理器

```
手機處理器（2010 年）：
───────────────────────────
Qualcomm Snapdragon：    1GHz，1GHz，45nm
TI OMAP 3：              600MHz，65nm
Samsung Hummingbird：    1GHz，45nm
Apple A4：               1GHz，45nm，S5PC110
```

### 效能提升

```
處理器演進：
───────────────────────────
2008:  528MHz (HTC Dream)
2009:  600MHz (Droid, iPhone 3GS)
2010:  1GHz (Nexus One, Galaxy S)
2011:  1.5GHz 雙核
2012:  四核成為主流
```

### 架構進步

```
ARM 架構演進：
───────────────────────────
ARM11：       2008 年以前的主流
Cortex-A8：   2009-2010，單核主力
Cortex-A9：   2011，多核開始
Cortex-A15：  2012，高效能
```

## 螢幕發展

### 螢幕技術

```
螢幕技術比較（2010 年）：
───────────────────────────
AMOLED：
  優點：    黑色表現好、省電、視角廣
  缺點：    戶外可視性稍差、成本高
  代表：    Nexus One、Galaxy S

LCD：
  優點：    戶外可視性好、壽命長、成本低
  缺點：    對比度稍差
  代表：    iPhone 3GS、Droid

Super LCD：
  優點：    接近 IPS 表現
  缺點：    產量有限
```

### 解析度進化

```
螢幕解析度演進：
───────────────────────────
2008:  320x480 (VGA)
2009:  480x320 / 480x854 (HVGA/WVGA)
2010:  800x480 (WVGA) 成為主流
2010:  960x640 (iPhone 4 Retina)
2012:  1280x720 (HD)
```

### 尺寸變化

```
螢幕尺寸趨勢：
───────────────────────────
早期智慧手機：  2.5-3.5"
2010 年旗艦：   3.5-4"
平板手機：      5"+ (2012 年後)
```

## 相機功能

### 百萬畫素競賽

```
相機畫素演進：
───────────────────────────
2008:  2MP
2009:  3MP、5MP
2010:  5MP、8MP（部分）
2012:  8MP、13MP
```

### 新功能

```
相機新功能（2010 年）：
───────────────────────────
臉部偵測：      Android 2.1 支援
自動對焦：      標配功能
LED 閃光燈：    逐漸普及
觸控對焦：      新旗艦標準
720p 錄影：     開始出現
```

### 相機 API

```java
// Android 2.1 臉部偵測
import android.hardware.Camera;

Camera camera = Camera.open();
Parameters params = camera.getParameters();

// 啟用臉部偵測
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

camera.setParameters(params);
camera.startPreview();
```

## 記憶體與儲存

### RAM 進化

```
RAM 容量演進：
───────────────────────────
2008:  128MB
2009:  256MB
2010:  512MB
2012:  1GB
2013:  2GB
```

### 儲存方案

```
儲存選項（2010 年）：
───────────────────────────
內建快閃記憶體：
  512MB - 32GB

可擴展儲存：
  microSD 支援（逐漸成為標準）
  支援到 32GB（當時最大值）

App2SD：
  Android 2.2 開始支援
  應用可移至 SD 卡
```

## 連接能力

### 網路支援

```
網路能力（2010 年旗艦）：
───────────────────────────
2G：    GSM/GPRS/EDGE
3G：    UMTS/HSPA (7.2Mbps)
4G：    LTE (部分旗艦)
Wi-Fi： 802.11 b/g/n
藍牙：  2.1 + EDR
GPS：   A-GPS
```

### HSPA+ 興起

```
HSPA+ 速度提升：
───────────────────────────
HSPA：        7.2Mbps 下載
HSPA+：       21Mbps 下載
DC-HSPA+：    42Mbps 下載（少數支援）
```

## 感應器

### 常見感應器

```
手機感應器（2010 年）：
───────────────────────────
加速度計：      體感遊戲、螢幕旋轉
陀螺儀：       少數旗艦支援（iPhone 4）
光學感應器：   自動亮度調整
距離感應器：   通話時關閉螢幕
數位羅盤：      導航、AR
GPS：          衛星定位
```

### 陀螺儀 API

```java
// 陀螺儀偵測（Android 2.3+）
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

SensorManager sm = (SensorManager) getSystemService(SENSOR_SERVICE);
Sensor gyroscope = sm.getDefaultSensor(Sensor.TYPE_GYROSCOPE);

sm.registerListener(this, gyroscope, SensorManager.SENSOR_DELAY_GAME);

@Override
public void onSensorChanged(SensorEvent event) {
    if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
        float x = event.values[0]; // X 軸旋轉
        float y = event.values[1]; // Y 軸旋轉
        float z = event.values[2]; // Z 軸旋轉
    }
}
```

## 電池技術

### 容量提升

```
電池容量趨勢：
───────────────────────────
2008:  1000-1500mAh
2009:  1400-1800mAh
2010:  1400-2000mAh
```

### 續航力挑戰

```
續航力問題：
───────────────────────────
原因：
  - 更強的處理器 = 更多功耗
  - 更大的螢幕 = 更多功耗
  - 更多的連線功能 = 更多功耗

解決方案：
  - 更省電的處理器製程（65nm → 45nm）
  - AMOLED 螢幕
  - 軟體優化
```

---

## 結論

2010 年是手機硬體快速進化的一年。1GHz 處理器、512MB RAM、800x480 解析度成為旗艦標準。相機也提升到 500 萬畫素，並開始支援臉部偵測等功能。

硬體競賽加劇，但真正的挑戰在於軟硬整合——如何讓強大的硬體發揮最佳效能，同時維持良好的續航力。

---

*本期文章到此結束。*