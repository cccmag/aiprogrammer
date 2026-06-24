# Android 開發實戰

## 建立第一個 Android 專案

讓我們從無到有建立一個簡單的 Android 應用程式。

### 前置需求

- JDK 5 或以上
- Eclipse IDE 搭配 ADT 擴充套件
- Android SDK

### Step 1：建立新專案

在 Eclipse 中：
1. File → New → Project
2. 選擇 Android → Android Project
3. 填寫專案資訊：

```
Project Name: MyFirstApp
Build Target: Android 1.0
Application Name: 我的第一個程式
Package Name: com.example.myfirstapp
Create Activity: MainActivity
```

### Step 2：專案結構

建立後的專案結構：

```
MyFirstApp/
├── AndroidManifest.xml
├── src/
│   └── com/example/myfirstapp/
│       └── MainActivity.java
├── res/
│   ├── layout/
│   │   └── main.xml
│   └── values/
│       └── strings.xml
└── gen/
    └── (自動產生的 R.java)
```

## Hello World 實作

### 版面配置（res/layout/main.xml）

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center">

    <TextView
        android:id="@+id/hello_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        android:layout_marginBottom="20dp" />

    <Button
        android:id="@+id/click_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="點擊我" />

</LinearLayout>
```

### Activity 程式碼（MainActivity.java）

```java
package com.example.myfirstapp;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
    private int clickCount = 0;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        final TextView textView = (TextView) findViewById(R.id.hello_text);
        Button button = (Button) findViewById(R.id.click_button);

        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                clickCount++;
                textView.setText("點擊次數：" + clickCount);
                Toast.makeText(MainActivity.this,
                    "已點擊 " + clickCount + " 次",
                    Toast.LENGTH_SHORT).show();
            }
        });
    }
}
```

### AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.myfirstapp">

    <application
        android:icon="@drawable/icon"
        android:label="@string/app_name">

        <activity
            android:name=".MainActivity"
            android:label="@string/app_name">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
```

## 執行與測試

### 在模擬器上執行

1. 在 Package Explorer 中選擇專案
2. 點擊 Run → Run As → Android Application
3. 選擇已建立的 AVD 或建立新的
4. 等待模擬器啟動（約 1-3 分鐘）
5. 觀察程式執行結果

### 在真實設備上測試

1. 在手機上開啟 USB 偵錯模式
2. 使用 USB 連接電腦
3. 安裝 USB 驅動程式（Windows）
4. 執行 Run → Run As → Android Application
5. 選擇設備而非模擬器

## 除錯技巧

### Logcat 日誌

```java
import android.util.Log;

public class MyActivity extends Activity {
    private static final String TAG = "MyActivity";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "onCreate called");
    }
}
```

### DDMS 除錯透視

DDMS（Dalvik Debug Monitor Service）提供：

- **Threads**：查看執行緒
- **Heap**：記憶體使用狀況
- **File Explorer**：檔案系統瀏覽
- **Emulator Control**：模擬器控制

### 常見錯誤

**R.java 錯誤**：
- 通常是資源檔案（如 layout、strings）有語法錯誤
- 檢查 XML 檔案

**NullPointerException**：
- 在 findViewById() 返回 null 時訪問其方法
- 確認 ID 正確且版面配置已設定

**Force Close**：
- 查看 Logcat 中的 stack trace
- 找到例外發生的位置

## 建立待辦事項應用程式

### 資料模型

```java
public class TodoItem {
    private long id;
    private String title;
    private boolean completed;

    public TodoItem(String title) {
        this.title = title;
        this.completed = false;
    }

    public long getId() { return id; }
    public void setId(long id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) { this.completed = completed; }
}
```

### 主要功能

1. **新增待辦事項**：輸入文字，點擊新增按鈕
2. **顯示待辦清單**：ListView 展示所有事項
3. **標記完成**：點擊事項切換完成狀態
4. **刪除事項**：長按刪除

### 完整版面配置

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">

        <EditText
            android:id="@+id/input_text"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:hint="新增待辦事項..." />

        <Button
            android:id="@+id/add_button"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="新增" />

    </LinearLayout>

    <ListView
        android:id="@+id/todo_list"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:layout_marginTop="16dp" />

</LinearLayout>
```

### ListView 的使用

```java
public class TodoListActivity extends Activity {
    private ArrayList<TodoItem> items = new ArrayList<>();
    private ArrayAdapter<TodoItem> adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.todo_list);

        ListView listView = (ListView) findViewById(R.id.todo_list);
        EditText inputText = (EditText) findViewById(R.id.input_text);
        Button addButton = (Button) findViewById(R.id.add_button);

        adapter = new ArrayAdapter<>(this,
            android.R.layout.simple_list_item_1, items);
        listView.setAdapter(adapter);

        addButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                String text = inputText.getText().toString();
                if (!text.isEmpty()) {
                    items.add(new TodoItem(text));
                    adapter.notifyDataSetChanged();
                    inputText.setText("");
                }
            }
        });
    }
}
```

## 打包與發布

### 簽署 APK

1. 在專案上點擊右鍵 → Android Tools → Export Signed Application Package
2. 選擇金鑰庫或建立新的
3. 設定金鑰密碼和別名
4. 選擇輸出位置
5. 完成打包

### 发布到 Android Market

1. 註冊 Android Market 開發者帳號（當時需付費 $25）
2. 上傳簽署過的 APK
3. 填寫應用程式說明、截圖、分類
4. 設定價格（免費或收費）
5. 提交審核

---

**延伸閱讀**

- [Android hello world tutorial](https://www.google.com/search?q=Android+hello+world+tutorial)
- [Android+debugging+techniques](https://www.google.com/search?q=Android+debugging+techniques)
- [ListView+tutorial](https://www.google.com/search?q=Android+ListView+tutorial)