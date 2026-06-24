# Intent 與元件通訊

## Intent 簡介

Intent 是 Android 中的訊息物件，用於在元件之間傳遞訊息和啟動元件。它是 Android 元件通訊的核心機制。

### Intent 的用途

Intent 主要用於：

1. **啟動 Activity**：顯示一個螢幕
2. **啟動 Service**：啟動背景服務
3. **傳遞廣播**：發送系統或自訂廣播

### Intent 的組成

```java
Intent intent = new Intent();

// 動作（Action）
intent.setAction("com.example.ACTION_TEST");

// 資料（Data）
intent.setData(Uri.parse("content://myprovider/data"));

// 類別（Category）
intent.addCategory(Intent.CATEGORY_DEFAULT);

// 附加資料（Extras）
intent.putExtra("key", "value");

// 元件（Component）
intent.setClass(context, TargetActivity.class);
```

## Explicit Intent vs Implicit Intent

### Explicit Intent

明確指定要啟動的元件：

```java
Intent intent = new Intent(this, MyActivity.class);
startActivity(intent);
```

這種方式通常用於同一應用程式內部的元件啟動。

### Implicit Intent

不明確指定元件，由系統找到合適的元件來處理：

```java
Intent intent = new Intent(Intent.ACTION_VIEW);
intent.setData(Uri.parse("https://www.google.com"));
startActivity(intent);
```

系統會找到能夠處理此意圖的 Activity（如瀏覽器）。

## Intent Filter

當一個 Activity 能夠處理多種 Implicit Intent 時，需要定義 Intent Filter：

```xml
<activity android:name=".MyActivity">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
</activity>
```

### Intent Filter 的組成

| 元素 | 說明 |
|------|------|
| action | 要執行的動作（如 VIEW、EDIT） |
| category | 元件類別（如 DEFAULT、BROWSABLE） |
| data | 資料格式和 URI 結構 |

### 常见 Action

| Action | 說明 |
|--------|------|
| ACTION_VIEW | 顯示資料 |
| ACTION_EDIT | 編輯資料 |
| ACTION_SEND | 傳送資料 |
| ACTION_CALL | 打電話 |
| ACTION_DIAL | 撥號 |
| ACTION_SENDTO | 發送訊息 |

## Activity 之間的資料傳遞

### 傳遞資料到目標 Activity

```java
Intent intent = new Intent(this, SecondActivity.class);
intent.putExtra("name", "Alice");
intent.putExtra("age", 25);
intent.putExtra("score", 95.5);
startActivity(intent);
```

### 在目標 Activity 接收資料

```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    Intent received = getIntent();
    String name = received.getStringExtra("name");
    int age = received.getIntExtra("age", 0);
    double score = received.getDoubleExtra("score", 0.0);

    Log.d("Received", "Name: " + name + ", Age: " + age);
}
```

### 傳遞復雜資料（Bundle）

```java
Bundle bundle = new Bundle();
bundle.putString("name", "Bob");
bundle.putInt("age", 30);
bundle.putStringArray("hobbies", new String[]{"Reading", "Gaming"});

Intent intent = new Intent(this, ProfileActivity.class);
intent.putExtras(bundle);
startActivity(intent);
```

## 回傳結果給上一個 Activity

### 啟動並等待結果

```java
static final int REQUEST_CODE = 1;

Intent intent = new Intent(this, EditActivity.class);
startActivityForResult(intent, REQUEST_CODE);
```

### 發送結果

```java
Intent result = new Intent();
result.putExtra("edited_text", "New content");
setResult(RESULT_OK, result);
finish();
```

### 處理回傳結果

```java
@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    if (requestCode == REQUEST_CODE) {
        if (resultCode == RESULT_OK) {
            String editedText = data.getStringExtra("edited_text");
            // 處理回傳的資料
        }
    }
}
```

## Service 與 Intent

### 啟動 Service

```java
Intent serviceIntent = new Intent(this, MyService.class);
startService(serviceIntent);
```

### 停止 Service

```java
Intent serviceIntent = new Intent(this, MyService.class);
stopService(serviceIntent);
```

### 綁定到 Service

```java
private ServiceConnection connection = new ServiceConnection() {
    public void onServiceConnected(ComponentName name, IBinder service) {
        MyBinder binder = (MyBinder) service;
        myService = binder.getService();
    }

    public void onServiceDisconnected(ComponentName name) {
        myService = null;
    }
};

Intent intent = new Intent(this, MyService.class);
bindService(intent, connection, Context.BIND_AUTO_CREATE);
```

## 廣播訊息（Broadcast）

### 發送廣播

```java
Intent broadcast = new Intent();
broadcast.setAction("com.example.MY_BROADCAST");
broadcast.putExtra("message", "Hello from Activity A");
sendBroadcast(broadcast);
```

### 接收廣播

```java
public class MyReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        String message = intent.getStringExtra("message");
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
    }
}
```

### 註冊Receiver

在 AndroidManifest.xml 中註冊：

```xml
<receiver android:name=".MyReceiver">
    <intent-filter>
        <action android:name="com.example.MY_BROADCAST" />
    </intent-filter>
</receiver>
```

或在程式碼中動態註冊：

```java
IntentFilter filter = new IntentFilter("com.example.MY_BROADCAST");
registerReceiver(receiver, filter);
```

## 常見 Intent 範例

### 開啟網頁

```java
Intent browser = new Intent(Intent.ACTION_VIEW,
    Uri.parse("https://www.google.com"));
startActivity(browser);
```

### 發送電子郵件

```java
Intent email = new Intent(Intent.ACTION_SEND);
email.setType("message/rfc822");
email.putExtra(Intent.EXTRA_EMAIL, new String[]{"test@example.com"});
email.putExtra(Intent.EXTRA_SUBJECT, "Subject");
email.putExtra(Intent.EXTRA_TEXT, "Body");
startActivity(Intent.createChooser(email, "Send Email"));
```

### 撥打電話

```java
Intent dial = new Intent(Intent.ACTION_DIAL,
    Uri.parse("tel:+886912345678"));
startActivity(dial);
```

### 分享文字

```java
Intent share = new Intent(Intent.ACTION_SEND);
share.setType("text/plain");
share.putExtra(Intent.EXTRA_TEXT, "Check out this link!");
startActivity(Intent.createChooser(share, "Share via"));
```

---

**延伸閱讀**

- [Android Intent documentation](https://www.google.com/search?q=Android+Intent+documentation)
- [Intent+filter+examples](https://www.google.com/search?q=Android+Intent+filter+examples)
- [Activity+communication+Intent](https://www.google.com/search?q=Android+Activity+communication+Intent)