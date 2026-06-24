# Android 的誕生與行動開發新時代

## Android 計畫的起源

2007 年 11 月 5 日，Google 宣布了一個震驚科技界的計畫：Android。這個由 Google 主導的開放手機平台，旨在為全球數十億手機用戶提供更智慧、更開放的行動體驗。

### 開放手機聯盟

Android 計畫的另一個重要支柱是「開放手機聯盟」（Open Handset Alliance）。這個聯盟包含了 34 家來自全球的領導企業：

- **電信業者**：中國移動、T-Mobile、NTT DoCoMo、Vodafone
- **硬體製造商**：HTC、Motorola、Samsung、LG、Sony Ericsson
- **半導體公司**：Qualcomm、NVIDIA、Texas Instruments、Intel
- **軟體公司**：Google、eBay、Synaptics

聯盟的目標是共同開發開放標準，讓手機產業擺脫傳統的封閉模式。

## Android 與傳統手機平台的差異

### 傳統平台的限制

在 Android 出現之前，手機應用開發面臨諸多挑戰：

- **封閉的作業系統**：各大手機廠商使用各自的專屬系統
- **有限的 API**：開發者能使用的功能受到嚴格限制
- **審核制度**：應用程式必須通過漫長的審核才能上架
- **開發工具匱乏**：缺乏統一的開發環境和工具鏈

### Android 的創新

Android 的出現徹底改變了這一局面：

```
傳統模式：           Android 模式：
┌─────────┐         ┌─────────┐
│  封閉   │         │  開放   │
│  專屬   │         │  標準化 │
│  限制多 │         │  API 完整│
└─────────┘         └─────────┘
```

**開放原始碼**：Android 的核心代碼以 Apache 授權條款開源
**完整 SDK**：提供齊全的開發工具、模擬器、文件和範例
**自由發布**：任何人都能發布應用程式到 Android Market
**豐富 API**：涵蓋電話、網路、感應器、資料儲存等

## 行動開發的新典範

### Linux 核心的優勢

Android 基於 Linux 核心，這帶來了諸多好處：

- **穩定的核心**：經過數十年驗證的作業系統核心
- **硬體驅動程式支援**：大量的現成驅動程式
- **記憶體管理**：成熟的虛擬記憶體機制
- **安全性**：Linux 的權限模型

### Java 程式語言

Android 選擇 Java 作為主要開發語言：

```java
public class HelloWorldActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        TextView text = (TextView) findViewById(R.id.text);
        text.setText("Hello, Android!");
    }
}
```

Java 的優點：
- **廣大的開發者社群**
- **豐富的學習資源**
- **跨平台的開發經驗**
- **強制的物件導向設計**

### Dalvik 虛擬機器

Android 不使用標準的 JVM，而是使用專門設計的 Dalvik VM。Dalvik 針對手機設備進行了大量最佳化，特別是在記憶體使用和執行效率方面。

## Android 系統架構

Android 的系統架構可分為多層：

### 應用程式層（Applications）

最上層是使用者直接接觸的應用程式：
- 電話、簡訊、相機
- 瀏覽器、郵件、地圖
- 第三方應用程式

### 應用程式框架層（Application Framework）

這是開發者最常接觸的層，提供了大量的 API：

- **Activity Manager**：管理應用程式生命週期
- **Window Manager**：管理視窗和螢幕
- **Content Provider**：跨應用程式資料共享
- **Notification Manager**：狀態列通知
- **Package Manager**：應用程式管理

### 函式庫層（Libraries）

豐富的原生 C/C++ 函式庫：

| 函式庫 | 用途 |
|--------|------|
| Surface Manager | 2D/3D 圖形渲染 |
| SQLite | 輕量級資料庫 |
| OpenGL ES | 3D 圖形加速 |
| Media Framework | 音訊/視訊播放 |
| WebKit | 網頁瀏覽引擎 |
| SGL | 2D 圖形引擎 |

### Android 執行環境（Android Runtime）

- **Dalvik VM**：執行 Android 位元組碼
- **核心類別庫**：Java 基礎類別

### Linux 核心層（Linux Kernel）

基於 Linux 2.6 版核心，提供基礎服務：

- 硬體驅動程式
- 記憶體管理
- 行程管理
- 網路堆疊

## 開發環境的革新

### 整合開發環境

Android SDK 提供了完整的開發環境：

1. **Eclipse 整合**：透過 ADT 擴充套件
2. **視覺化編輯器**：拖放式 UI 設計
3. **模擬器**：無需真實手機即可測試
4. **除錯工具**：完整的偵錯能力

### 模擬器功能

Android 模擬器模擬了完整的手機環境：

```
模擬器功能：
├── 螢幕顯示（多種解析度）
├── 電話功能
├── 網路連線
├── GPS 位置
├── 加速計
├── 相機（模擬）
└── 各種感應器
```

## Android 的未來

2008 年是 Android 的元年。這個開放平台承諾：

- **更多硬體選擇**：擺脫单一厂商的限制
- **更低的進入門檻**：任何人都能開發應用
- **更多的創新**：開放平台催生更多可能性
- **更好的用戶體驗**：良性競爭推動進步

---

**延伸閱讀**

- [Android 官方網站](https://www.google.com/search?q=Android+official+site)
- [開放手機聯盟](https://www.google.com/search?q=Open+Handset+Alliance)
- [Android+SDK+download](https://www.google.com/search?q=Android+SDK+download+2008)