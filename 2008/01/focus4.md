# Activity 與生命週期

## Activity 的基本概念

Activity 是 Android 應用程式中最重要的元件之一，代表一個包含使用者介面的螢幕。每一個 Activity 都會佔據整個螢幕（或作為一個 dialog），使用者可以在上面進行各種互動操作。

### Activity 的定義

```java
public class MainActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }
}
```

在 AndroidManifest.xml 中註冊 Activity：

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app">

    <application ...>
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

## Activity 生命週期

Activity 有四種主要狀態：

| 狀態 | 說明 |
|------|------|
| Active/Running | Activity 在螢幕最上層，可與使用者互動 |
| Paused | Activity 失去焦點但仍可見（如 dialog） |
| Stopped | Activity 被其他 Activity 覆蓋，不可見 |
| Killed | Activity 被終結或行程被結束 |

### 生命週期回調方法

```
        ┌─────────────────────────────────────┐
        │         Activity 生命週期            │
        └─────────────────────────────────────┘

onCreate()
   │
   ▼
onStart()───────────────► onRestart()
   │                           │
   ▼                           │
onResume()◄──────────────────────┘
   │
   │ [Activity 運行中，可與使用者互動]
   │
   ▼
onPause()
   │
   ├──► [另一個 Activity 取得焦點但仍部分可見]
   │
   ▼
onStop()
   │
   ├──► [Activity 完全不可見]
   │
   ▼
onDestroy()
   │
   ▼
   [Activity 結束]
```

### 各階段說明

**onCreate()**
- Activity 第一次建立時調用
- 進行初始化設定：建立 views、初始化資料
- 一定要調用 super.onCreate()

**onStart()**
- Activity 即將可見時調用
- 良好的準備階段

**onResume()**
- Activity 即將與使用者互動
- 恢復暫停的動畫、感應器等

**onPause()**
- Activity 即將失去焦點
- 儲存持久資料、暫停動畫

**onStop()**
- Activity 即將不可見
- 釋放大型資源

**onDestroy()**
- Activity 即將被終結
- 最後的清理工作

**onRestart()**
- Activity 從 stopped 狀態重新啟動

## 實際範例：生命週期追蹤

```java
public class LifecycleActivity extends Activity {
    private static final String TAG = "LifecycleActivity";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        Log.d(TAG, "onCreate() called");
    }

    @Override
    public void onStart() {
        super.onStart();
        Log.d(TAG, "onStart() called");
    }

    @Override
    public void onResume() {
        super.onResume();
        Log.d(TAG, "onResume() called");
    }

    @Override
    public void onPause() {
        super.onPause();
        Log.d(TAG, "onPause() called");
    }

    @Override
    public void onStop() {
        super.onStop();
        Log.d(TAG, "onStop() called");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy() called");
    }

    @Override
    public void onRestart() {
        super.onRestart();
        Log.d(TAG, "onRestart() called");
    }
}
```

## Activity 堆疊（Back Stack）

Android 使用堆疊來管理 Activity 的返回順序：

### 堆疊運作原理

```
使用者操作流程：

Step 1: 啟動 App
┌─────────┐
│Activity A│  ← 堆疊頂部
└─────────┘

Step 2: 啟動 Activity B
┌─────────┐
│Activity B│  ← 堆疊頂部
├─────────┤
│Activity A│
└─────────┘

Step 3: 啟動 Activity C
┌─────────┐
│Activity C│  ← 堆疊頂部
├─────────┤
│Activity B│
├─────────┤
│Activity A│
└─────────┘

Step 4: 按下返回鍵
┌─────────┐
│Activity B│  ← 堆疊頂部
├─────────┤
│Activity A│
└─────────┘
```

### 堆疊模式

| 模式 | 說明 |
|------|------|
| standard | 預設模式，每次啟動都創建新實例 |
| singleTop | 若 Activity 在堆疊頂部，則重用 |
| singleTask | 在新任務堆疊中創建，若已存在則清除其上方的 Activity |
| singleInstance | 獨立的任務堆疊，只會有一個實例 |

```xml
<activity
    android:name=".MyActivity"
    android:launchMode="singleTop" />
```

## 狀態儲存與恢復

### 儲存實例狀態

當 Activity 被系統終結（如旋轉螢幕）時，可以儲存臨時狀態：

```java
@Override
public void onSaveInstanceState(Bundle outState) {
    super.onSaveInstanceState(outState);
    outState.putString("text", myEditText.getText().toString());
    outState.putInt("count", counter);
}

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.main);

    if (savedInstanceState != null) {
        String text = savedInstanceState.getString("text");
        int count = savedInstanceState.getInt("count");
    }
}
```

### 持久化儲存

對於需要長期保存的資料，應該使用其他儲存方式：

| 方式 | 適用場景 |
|------|----------|
| SharedPreferences | 設定值、小量資料 |
| SQLite | 結構化資料 |
| 檔案 | 大型檔案、二進位資料 |
| ContentProvider | 跨應用程式資料共享 |

## 範例：簡單的計數器 Activity

```java
public class CounterActivity extends Activity {
    private int count = 0;
    private TextView countView;
    private Button incrementBtn;
    private Button decrementBtn;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.counter);

        countView = (TextView) findViewById(R.id.count_text);
        incrementBtn = (Button) findViewById(R.id.btn_increment);
        decrementBtn = (Button) findViewById(R.id.btn_decrement);

        updateDisplay();

        incrementBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                count++;
                updateDisplay();
            }
        });

        decrementBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                count--;
                updateDisplay();
            }
        });
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putInt("count", count);
    }

    @Override
    protected void onRestoreInstanceState(Bundle savedInstanceState) {
        super.onRestoreInstanceState(savedInstanceState);
        count = savedInstanceState.getInt("count");
        updateDisplay();
    }

    private void updateDisplay() {
        countView.setText("Count: " + count);
    }
}
```

---

**延伸閱讀**

- [Android Activity lifecycle](https://www.google.com/search?q=Android+Activity+lifecycle)
- [Activity+back+stack](https://www.google.com/search?q=Android+Activity+back+stack)
- [onSaveInstanceState+example](https://www.google.com/search?q=Android+onSaveInstanceState+example)