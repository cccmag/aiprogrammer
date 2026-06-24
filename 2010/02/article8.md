# 物聯網與 Android 的應用

## 物聯網興起

### 概念介紹

```
物聯網（IoT）概念：
───────────────────────────
定義：         物品連網、互相交換資料
起源：         1999 年 Kevin Ashton 首次提出
2010 年趨勢：   開始快速發展
關鍵技術：     感應器、網路、雲端
```

## Android 的延伸

### 非手機裝置

```
Android 延伸領域（2010 年猜測）：
───────────────────────────
智慧電視：       可能（Android TV 2014 年才成）
汽車系統：       可能（Android Auto 2014）
穿戴裝置：       早期實驗（2012 後爆發）
家用設備：       嵌入式 Android
遊戲主機：       有興趣（OUYA 2012）
```

## 嵌入式 Android

### 概念

```
嵌入式 Android：
───────────────────────────
定義：         Android 作為嵌入式系統的 OS
優點：         熟悉的介面、豐富的 App、生態系
挑戰：         資源限制、功耗、即時性
應用：         平板、機上盒、汽車
```

### 需求硬體

```
基本需求（2010 年評估）：
───────────────────────────
處理器：       ARMv7 以上
記憶體：       512MB+
儲存：         4GB+
螢幕：         7" 以上
網路：         Ethernet 或 Wi-Fi
```

## 遠端控制

### 應用場景

```
 Android 作為控制器（2010 年）：
───────────────────────────
智慧家居：     燈光、溫度控制
遠端監控：     保全 cameras
工業控制：     工廠自動化
醫療設備：     醫療儀器
汽車診斷：     OBD-II 適配器
```

### 範例：智慧家居

```java
// 智慧家居控制概念
public class SmartHomeController {
    private HttpClient httpClient;

    public void setLight(int room, boolean on) {
        String url = String.format(
            "http://home.local/api/light/%d/%s", room, on ? "on" : "off");
        try {
            httpClient.execute(new HttpGet(url));
        } catch (Exception e) {
            Log.e("SmartHome", e.getMessage());
        }
    }

    public void setThermostat(float temperature) {
        String url = String.format(
            "http://home.local/api/thermostat/%.1f", temperature);
        // ...
    }
}
```

## 感應器整合

### 常見感應器

```
物聯網常用感應器：
───────────────────────────
溫度感應器：     環境監控
濕度感應器：     農業、倉儲
光學感應器：     自動照明
動作感應器：     安防系統
氣體感應器：     空氣品質
GPS：            資產追蹤
```

### 藍牙感應器

```java
// 藍牙感應器讀取
public class SensorReader {
    private BluetoothAdapter adapter;

    public void connect(BluetoothDevice device) {
        UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
        BluetoothSocket socket = device.createRfcommSocketToServiceRecord(uuid);
        socket.connect();

        InputStream in = socket.getInputStream();
        // 讀取感應器資料
        byte[] buffer = new byte[1024];
        int bytes = in.read(buffer);
        String data = new String(buffer, 0, bytes);
    }
}
```

## M2M 通訊

### 機器對機器

```
M2M 溝通模式：
───────────────────────────
Device to Cloud：  裝置直接上傳雲端
Device to Gateway： 透過閘道器
Device to Device： 直接互連
```

### 通訊協定

```
物聯網通訊協定（2010 年）：
───────────────────────────
HTTP：          簡單但耗費資源
MQTT：          輕量級發布/訂閱（IBM 开发）
CoAP：          針對受限裝置（2013 年標準化）
XMPP：          即時通訊延伸
```

## 未來展望

### 預測（2010 年）

```
物聯網未來預測：
───────────────────────────
2010-2012：   概念驗證階段
2013-2015：   開始普及
2016-2020：   大規模採用
連網裝置：    從數億到數百億
```

---

## 結論

物聯網在 2010 年還處於早期階段，但 Android 作為一個開放的平台，被視為未來物聯網設備的重要作業系統候選人。雖然完整的 Android 延伸還需幾年時間，但相關的技術和概念已經在發展中。

---

*本期文章到此結束。*