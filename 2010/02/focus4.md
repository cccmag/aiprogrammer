# 主題四：開發者工具鏈

## Android 開發環境

### 工具鏈組成

```
2010 年 Android 開發工具：
───────────────────────────
JDK：         Java Development Kit
Eclipse：     主要 IDE（需 Kepler 或更新）
ADT：         Android Development Tools
Android SDK： Android 軟體開發包
AVD：         Android Virtual Device
```

### 安裝需求

```
開發環境需求：
───────────────────────────
作業系統：    Windows/Mac/Linux
記憶體：      2GB+
磁碟空間：    2GB+
JDK：         JDK 5 或 JDK 6
```

## Eclipse 與 ADT

### ADT 安裝

```
ADT Plugin 安裝步驟：
───────────────────────────
1. Eclipse → Help → Install New Software
2. 新增 https://dl-ssl.google.com/android/eclipse/
3. 選擇 "Developer Tools"
4. 同意授權條款
5. 等待下載並安裝
6. 重啟 Eclipse
```

### ADT 功能

```
ADT 提供的功能：
───────────────────────────
Android 專案精靈
除錯工具
資源編輯器
UI 預覽
元件拖放
```

### Eclipse 設定

```xml
<!-- Android SDK 路徑設定 -->
<!-- Window → Preferences → Android -->
<!-- SDK Location: /path/to/android-sdk -->
```

## Android SDK

### SDK Manager

```
SDK Manager 功能：
───────────────────────────
安裝 SDK 版本
安裝 API 文件
安裝範例程式碼
安裝 Google API
更新 SDK 工具
```

### 可用 SDK 版本

```
SDK Platform 比較：
───────────────────────────
Android 1.5 (API 3)：     2009 年 4 月
Android 1.6 (API 4)：     2009 年 9 月
Android 2.0 (API 5)：     2009 年 11 月
Android 2.1 (API 7)：     2009 年 12 月
Android 2.2 (API 8)：     2010 年 5 月（Beta）
```

### 建立 AVD

```bash
# 命令列建立 AVD
android create avd \
  --name my_avd \
  --target 7 \
  --skin WVGA800

# 或使用 GUI
# Eclipse → Window → Android SDK and AVD Manager
```

## 模擬器

### 模擬器功能

```
Android 模擬器（2010 年）：
───────────────────────────
支援版本：    1.5-2.2
螢幕大小：    QVGA, HVGA, WVGA
功能：        打電話、發簡訊、網路
限制：        無相機、慢、耗記憶體
```

### 效能優化

```
模擬器效能技巧：
───────────────────────────
使用實體 GPU
啟用快照（Snapshots）
分配更多記憶體
使用 Host GPU（如果支援）
```

### 模擬器限制

```
模擬器不能做的事：
───────────────────────────
藍牙功能
Wi-Fi Direct
相機（可模拟但非實際）
USB
NFC
精確的耗電量測量
```

## UI 開發

### XML 佈局

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="10dp">

    <TextView
        android:id="@+id/title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="標題"
        android:textSize="20sp"/>

    <EditText
        android:id="@+id/input"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="輸入文字"/>

    <Button
        android:id="@+id/submit"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="提交"/>

</LinearLayout>
```

### Graphical Layout 編輯器

```
GUI 編輯器功能：
───────────────────────────
拖放元件
屬性面板
預覽效果
多螢幕預覽
```

### 資源檔案結構

```
res/ 目錄結構：
───────────────────────────
res/layout/        XML 佈局
res/values/        字串、顏色、尺寸
res/drawable/      圖片資源
res/menu/          選單定義
res/raw/           原始資源檔
res/anim/          動畫定義
res/xml/           XML 設定檔
```

## 程式碼編寫

### Activity 開發

```java
public class MainActivity extends Activity {
    private TextView title;
    private EditText input;
    private Button submit;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        // 取得元件
        title = (TextView) findViewId(R.id.title);
        input = (EditText) findViewById(R.id.input);
        submit = (Button) findViewById(R.id.submit);

        // 設定監聽
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String text = input.getText().toString();
                // 處理輸入
            }
        });
    }
}
```

### 除錯

```java
// Logcat 使用
Log.d("MyActivity", "Debug message");
Log.i("MyActivity", "Info message");
Log.w("MyActivity", "Warning message");
Log.e("MyActivity", "Error message");
```

## 應用發布

### 打包 APK

```bash
# 使用 Eclipse 匯出
# File → Export → Android Application
# 選擇專案
# 建立 keystore 或使用現有
# 選擇 alias 和密碼
# 選擇目的地
# 完成
```

### 發布到 Market

```
發布步驟：
───────────────────────────
1. 移除除錯程式碼
2. 申請 Android Market 開發者帳號（$25）
3. 簽署 APK（發布版本）
4. 上傳截圖和說明
5. 設定價格（免費或付費）
6. 提交審核
```

### ProGuard

```properties
# project.properties
# 啟用 ProGuard
proguard.config=proguard.cfg
```

```pro
# proguard.cfg
# 移除除錯程式碼
-optimizationpasses 5
-dontpreverify
-verbose

# 保留行號
-keepattributes SourceFile,LineNumberTable
```

---

## 結論

2010 年的 Android 開發工具鏈已相當成熟。Eclipse + ADT 提供了完整的開發、調試、打包能力。雖然模擬器有效能問題，但仍是重要的測試工具。

掌握這些工具是 Android 開發的第一步。

---

*本期文章到此結束。*