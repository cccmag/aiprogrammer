# 智慧手機的感測器應用：加速度計與定位

## 前言

2009 年，智慧手機開始配備越來越多的感測器，這為 Web 開發者打開了全新的大門。加速度計、GPS、陀螺儀等感測器讓網頁應用能夠感知真實世界。

## 手機感測器概述

### 2009 年主流智慧手機感測器

```
2009 年智慧手機感測器：

iPhone 3GS（2009年6月）：
- 加速度計
- 磁力計（羅盤）
- proximity sensor（接近感測）
- 環境光感測

Google Nexus One（2010年1月）：
- 加速度計
- 陀螺儀（新增）
- GPS
- WiFi 定位
- 細胞基地台定位

主流 Android 手機（2009年）：
- HTC Dream (G1)
- HTC Magic (G2)
- 三星 Galaxy
```

### 感測器類型

| 感測器 | 用途 | Web API |
|--------|------|---------|
| 加速度計 | 偵測移動和方向 | DeviceMotion |
| 陀螺儀 | 偵測旋轉 | DeviceOrientation |
| 磁力計 | 指南針 | DeviceOrientation |
| GPS | 位置 | Geolocation API |
| 光感測 | 螢幕亮度調整 | 無標準 API |

## DeviceMotion API

### 基本用法

```javascript
// 監聽加速度變化
window.addEventListener('devicemotion', function(event) {
  var acceleration = event.acceleration;
  var x = acceleration.x;
  var y = acceleration.y;
  var z = acceleration.z;

  console.log('X: ' + x + ', Y: ' + y + ', Z: ' + z);
});
```

### 偵測搖晃

```javascript
var lastAcceleration = {x: 0, y: 0, z: 0};
var shakeThreshold = 15;

window.addEventListener('devicemotion', function(event) {
  var current = event.acceleration;

  var deltaX = Math.abs(current.x - lastAcceleration.x);
  var deltaY = Math.abs(current.y - lastAcceleration.y);
  var deltaZ = Math.abs(current.z - lastAcceleration.z);

  if (deltaX + deltaY + deltaZ > shakeThreshold) {
    // 偵測到搖晃
    onShake();
  }

  lastAcceleration = current;
});

function onShake() {
  console.log('搖晃了！');
  // 切換歌曲、刷新頁面等
}
```

### 步數計

```javascript
var stepCount = 0;
var lastMagnitude = 0;

window.addEventListener('devicemotion', function(event) {
  var acc = event.accelerationIncludingGravity;

  // 計算向量大小
  var magnitude = Math.sqrt(
    acc.x * acc.x +
    acc.y * acc.y +
    acc.z * acc.z
  );

  // 峰值檢測
  if (magnitude > 12 && magnitude > lastMagnitude) {
    stepCount++;
    updateDisplay(stepCount);
  }

  lastMagnitude = magnitude;
});
```

## DeviceOrientation API

### 基本用法

```javascript
// 監聽方向變化
window.addEventListener('deviceorientation', function(event) {
  var alpha = event.alpha; // 繞 Z 軸（指南針）
  var beta = event.beta;   // 繞 X 軸（前後傾斜）
  var gamma = event.gamma; // 繞 Y 軸（左右傾斜）

  console.log('Alpha: ' + alpha);
  console.log('Beta: ' + beta);
  console.log('Gamma: ' + gamma);
});
```

### 指南針應用

```javascript
var compassElement = document.getElementById('compass');
var arrowElement = document.getElementById('arrow');

window.addEventListener('deviceorientation', function(event) {
  var alpha = event.alpha;

  if (alpha !== null) {
    // 處理羅盤角度
    var rotation = 360 - alpha;
    arrowElement.style.transform =
      'rotate(' + rotation + 'deg)';
  }
});
```

### 視差效果

```javascript
// 根據手機傾斜創建視差效果
var layer1 = document.getElementById('layer1');
var layer2 = document.getElementById('layer2');

window.addEventListener('deviceorientation', function(event) {
  var beta = event.beta || 0;  // -180 到 180
  var gamma = event.gamma || 0; // -90 到 90

  // 限制範圍
  beta = Math.max(-45, Math.min(45, beta));
  gamma = Math.max(-45, Math.min(45, gamma));

  // 應用視差移動
  layer1.style.transform =
    'translate(' + (gamma * 0.5) + 'px, ' + (beta * 0.5) + 'px)';

  layer2.style.transform =
    'translate(' + (gamma * 1) + 'px, ' + (beta * 1) + 'px)';
});
```

## Geolocation API

### 基本用法

```javascript
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    function(position) {
      console.log('緯度：' + position.coords.latitude);
      console.log('經度：' + position.coords.longitude);
    },
    function(error) {
      console.log('錯誤：' + error.message);
    }
  );
}
```

### 選項參數

```javascript
navigator.geolocation.getCurrentPosition(
  successCallback,
  errorCallback,
  {
    enableHighAccuracy: true,  // 使用 GPS
    timeout: 5000,            // 5 秒超時
    maximumAge: 0              // 不快取
  }
);
```

### 持續追蹤

```javascript
var watchId = navigator.geolocation.watchPosition(
  function(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    var speed = position.coords.speed;

    updateMap(lat, lng);
    updateSpeed(speed);
  },
  function(error) {
    console.log('Error:', error.message);
  },
  {
    enableHighAccuracy: true,
    maximumAge: 10000  // 10 秒快取
  }
);

// 停止追蹤
navigator.geolocation.clearWatch(watchId);
```

## 應用場景

### 遊戲控制

```javascript
// 體感遊戲
GameCanvas.addEventListener('deviceorientation', function(event) {
  var beta = event.beta;   // 控制上下
  var gamma = event.gamma; // 控制左右

  // 將傾斜轉換為角色移動
  player.x += gamma * 0.5;
  player.y += beta * 0.5;
});
```

### 擴增實境（AR）

```javascript
// 簡化的 AR 效果
var video = document.getElementById('camera');

navigator.getUserMedia(
  { video: { facingMode: 'environment' } },
  function(stream) {
    video.srcObject = stream;
  },
  function(error) {
    console.log('Camera error:', error);
  }
);

window.addEventListener('deviceorientation', function(event) {
  var alpha = event.alpha;
  var beta = event.beta;

  // 根據方向計算 AR 疊加位置
  updateAROverlay(alpha, beta);
});
```

### 室內導航

```javascript
// 使用 WiFi 定位進行室內導航
function indoorNavigation() {
  // 結合加速度計和 WiFi 指紋
  navigator.geolocation.getCurrentPosition(
    function(position) {
      // WiFi 定位結果
      var wifiLocation = position.coords;

      // 使用加速度計進行室內推算
      window.addEventListener('devicemotion', function(e) {
        var acc = e.acceleration;
        // 積分計算移動距離
        var distance = integrateAccelerometer(acc);

        // 結合 WiFi 定位和 dead reckoning
        var finalPosition = fuse(
          wifiLocation,
          distance,
          getHeading()
        );

        updateMap(finalPosition);
      });
    }
  );
}
```

## 瀏覽器支援（2009年）

```javascript
// 2009 年支援狀況

// iPhone Safari
// - DeviceMotion: iOS 4 之前有限支援
// - DeviceOrientation: iOS 4 之前有限支援
// - Geolocation: iPhone OS 3 支援

// Android Browser
// - DeviceMotion: Android 2.3+ 支援
// - DeviceOrientation: Android 2.3+ 支援
// - Geolocation: Android 2.0+ 支援

// Feature Detection
if (window.DeviceMotionEvent) {
  // 支援 DeviceMotion
}

if (navigator.geolocation) {
  // 支援 Geolocation
}
```

## 結語

2009 年是行動 Web 的起點。雖然當時的感測器 API 還很原始，瀏覽器支援也很有限，但這開啟了一個新的可能性——網頁應用不再只是靜態的內容展示，而是可以感知和回應真實世界的互動。

## 延伸閱讀

- [W3C DeviceOrientation API](https://www.google.com/search?q=W3C+DeviceOrientation+API+2009)
- [Geolocation API 規格](https://www.google.com/search?q=Geolocation+API+specification)
- [iPhone 感測器應用](https://www.google.com/search?q=iPhone+accelerometer+web+apps+2009)
- [Mobile Web 感測器](https://www.google.com/search?q=mobile+web+sensors+API)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*