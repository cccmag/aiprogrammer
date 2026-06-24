# Android 開發實務

## 概述

本期實作將展示 Android 開發的基礎程式碼，包括 Activity、Intent、以及基本 UI 元件的使用。

## Activity 生命週期

```java
// activity-demo.java - Activity 生命週期展示
public class MainActivity extends Activity {
    private static final String TAG = "ActivityDemo";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "onCreate");
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.d(TAG, "onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG, "onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.d(TAG, "onPause");
    }

    @Override
    protected void onStop() {
        super.onStop();
        Log.d(TAG, "onStop");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "onDestroy");
    }
}
```

## Intent 使用

```java
// intent-demo.java - Intent 範例展示
public class IntentDemo {
    public void explicitIntent(Context context) {
        Intent intent = new Intent(context, TargetActivity.class);
        intent.putExtra("key", "value");
        context.startActivity(intent);
    }

    public void implicitIntent(Context context) {
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setData(Uri.parse("http://example.com"));
        context.startActivity(intent);
    }
}
```

## UI 元件使用

```java
// ui-demo.java - UI 元件範例
public class UIDemo {
    public void setupButton(Activity activity) {
        Button button = (Button) activity.findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("UI", "Button clicked!");
            }
        });
    }
}
```

## 程式碼展示

本期程式碼位於 `_code/` 目錄：

- `activity-demo.js` - Activity 生命週期展示
- `intent-demo.js` - Intent 使用範例
- `ui-demo.js` - UI 元件範例

---

*本期程式實作到此結束。*