# Google Android 發布：手機開源平台

2007 年 11 月，Google 宣布了 Android 開放手機聯盟和 SDK。這個基於 Linux 核心的開源手機平台，預示著手機產業的革命性變革。

## Android 架構

```java
// Android 應用架構
public class MyActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        Button btn = (Button) findViewById(R.id.myButton);
        btn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Toast.makeText(MyActivity.this,
                    "Hello, Android!", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
```

## 關鍵元件

```java
// Activity - 螢幕介面
// Service - 後台服務
// BroadcastReceiver - 廣播接收
// ContentProvider - 資料共享
```

## 結語

Android 的發布開創了手機開源的新時代，改變了整個行動產業的格局。

---

*延伸閱讀：[Android 開發者網站](https://developers.google.com/search/?q=android+official)*