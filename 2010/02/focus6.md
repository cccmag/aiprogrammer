# 主題六：Android 與雲端整合

## Google 雲端服務

### 主要服務

```
Google 雲端服務（2010 年）：
───────────────────────────
Google App Engine：   雲端代管
Google Cloud Storage： 檔案儲存
Google Cloud SQL：    雲端資料庫（Beta）
Google Prediction API： 機器學習
```

## Account Manager

### 帳號驗證

```java
// 取得 Google 帳號
AccountManager manager = AccountManager.get(this);
Account[] accounts = manager.getAccountsByType("com.google");

// 請求帳號存取權限
AccountManagerCallback<Bundle> callback = new AccountManagerCallback<Bundle>() {
    @Override
    public void run(AccountManagerFuture<Bundle> future) {
        try {
            Bundle bundle = future.getResult();
            String authToken = bundle.getString(AccountManager.KEY_AUTHTOKEN);
            // 使用 token
        } catch (OperationCanceledException e) {
            // 使用者取消
        } catch (IOException e) {
            // IO 錯誤
        } catch (AuthenticatorException e) {
            // 認證錯誤
        }
    }
};

Intent intent = manager.getAuthToken(
    accounts[0],
    "android",
    true,
    callback,
    null
);
startActivity(intent);
```

## 同步框架

### SyncAdapter

```java
// 建立 SyncAdapter
public class MySyncAdapter extends AbstractThreadedSyncAdapter {
    private ContentResolver mContentResolver;

    public MySyncAdapter(Context context, boolean autoInitialize) {
        super(context, autoInitialize);
        mContentResolver = context.getContentResolver();
    }

    @Override
    public void onPerformSync(Account account, Bundle extras,
            String authority, ContentProviderClient provider,
            SyncResult syncResult) {
        // 執行同步
        try {
            // 從伺服器取得資料
            List<Item> items = fetchItemsFromServer();

            // 更新本地資料庫
            for (Item item : items) {
                ContentValues values = new ContentValues();
                values.put(COLUMN_TITLE, item.getTitle());
                mContentResolver.insert(CONTENT_URI, values);
            }
        } catch (Exception e) {
            syncResult.stats.numIoExceptions++;
        }
    }
}
```

### 觸發同步

```java
// 請求立即同步
Bundle extras = new Bundle();
extras.putBoolean(ContentResolver.SYNC_EXTRAS_MANUAL, true);
extras.putBoolean(ContentResolver.SYNC_EXTRAS_EXPEDITED, true);
ContentResolver.requestSync(
    account,
    AUTHORITY,
    extras
);
```

## Cloud to Device Messaging

### C2DM 概述

```
C2DM（Cloud to Device Messaging）：
───────────────────────────
功能：        伺服器推送訊息到手機
推出時間：    2010 年（Beta）
限制：       需要 Google 帳號
後續：        演變為 GCM（2012）
```

### C2DM 實作

```java
// C2DM 監聽服務
public class C2DMReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals("com.google.android.c2dm.intent.RECEIVE")) {
            String payload = intent.getStringExtra("payload");
            // 處理訊息
            Log.d("C2DM", "收到訊息: " + payload);
        }
    }
}
```

## App Engine 整合

### 遠端 API

```python
# App Engine 後端（Python）
import webapp2
from google.appengine.ext import db

class Item(db.Model):
    title = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class APIHandler(webapp2.RequestHandler):
    def get(self):
        items = db.Query(Item).order(-Item.created).fetch(10)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps([
            {'title': i.title, 'created': str(i.created)}
            for i in items
        ]))

app = webapp2.WSGIApplication([
    ('/api/items', APIHandler),
], debug=True)
```

### Android 客戶端

```java
// 從 App Engine 取得資料
public class ApiClient {
    private static final String BASE_URL = "http://your-app.appspot.com";

    public List<Item> fetchItems() throws Exception {
        URL url = new URL(BASE_URL + "/api/items");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        BufferedReader reader = new BufferedReader(
            new InputStreamReader(conn.getInputStream())
        );

        StringBuilder response = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            response.append(line);
        }
        reader.close();

        return parseItems(response.toString());
    }
}
```

## 資料同步策略

### 離線優先

```java
// 離線優先的資料存取
public class DataRepository {
    private LocalDatabase localDb;
    private RemoteApi remoteApi;
    private SyncStatus syncStatus;

    public void save(Item item) {
        // 1. 先寫入本地
        localDb.save(item);

        // 2. 嘗試同步到雲端
        if (syncStatus.isOnline()) {
            try {
                remoteApi.save(item);
                localDb.markSynced(item.getId());
            } catch (Exception e) {
                localDb.markPending(item.getId());
            }
        } else {
            localDb.markPending(item.getId());
        }
    }

    public List<Item> getAll() {
        // 返回本地資料（過時的也顯示）
        return localDb.getAll();
    }
}
```

## Backup API

### 資料備份

```xml
<!-- AndroidManifest.xml -->
<application android:label="MyApp"
              android:backupAgent="MyBackupAgent">
    <meta-data
        android:name="com.google.android.backup.api_key"
        android:value="your_backup_api_key"/>
</application>
```

```java
// BackupAgent
public class MyBackupAgent extends BackupAgentHelper {
    @Override
    public void onCreate() {
        SharedPreferencesBackupHelper helper =
            new SharedPreferencesBackupHelper(this, "my_prefs");
        addHelper("prefs", helper);
    }
}
```

## 使用 Google 帳號的服務

### 常用整合

```
Google 服務整合：
───────────────────────────
Google Maps：      地圖與定位
Google Search：    語音搜尋
YouTube：         影片嵌入
Google Analytics： 使用分析
AdMob：           行動廣告
```

### Google Maps

```java
// 顯示地圖
MapView mapView = new MapView(this, "YOUR_API_KEY");
mapView.setClickable(true);
setContentView(mapView);

// 控制地圖
MapController controller = mapView.getController();
controller.setZoom(15);
controller.setCenter(new GeoPoint(latitude, longitude));
```

---

## 結論

Android 與 Google 雲端服務的整合是其重要優勢。從帳號驗證、資料同步到推送通知，Google 提供了完整的雲端解決方案。

雖然 2010 年的服務還在早期階段，但這些基礎為日後 Android 生態系的繁榮奠定了重要基礎。

---

*本期文章到此結束。*