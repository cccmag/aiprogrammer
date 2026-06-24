# 雲端運算與手機的結合

## 雲端與手機的整合趨勢

### 2010 年趨勢

```
雲端 + 手機的發展（2010 年）：
───────────────────────────
同步服務：     聯絡人、日曆、書籤
儲存服務：     照片、文件、音樂
推送服務：     即時通知
運算服務：     雲端處理、手機顯示
Backup：       資料備份
```

## 同步服務

### Google 同步

```
Google 帳號同步：
───────────────────────────
聯絡人：       雙向同步
日曆：         事件同步
Gmail：        郵件同步
Photos：       Picasa 網路相簿
Docs：         文件同步（後來加入）
```

### 設定方式

```java
// 觸發同步
ContentResolver.requestSync(
    account,
    "com.android.contacts",
    new Bundle()
);

// 或在手機設定中開啟自動同步
// Settings → Accounts → Google → 開啟同步
```

## 雲端儲存

### 照片同步

```
照片雲端化（2010 年）：
───────────────────────────
Picasa：        Google 照片服務
自動上傳：     拍攝後自動上傳（需 App）
空間配額：     1GB 免費
分享：         連結分享
```

### 文件同步

```
文件服務（2010 年）：
───────────────────────────
Google Docs：   雲端文書處理
Dropbox：       檔案同步服務（iOS App 剛推出）
SugarSync：     多設備同步
iCloud：        2011 年推出
```

## 推送服務

### C2DM

```
Cloud to Device Messaging（C2DM）：
───────────────────────────
推出時間：     2010 年（Beta）
功能：         伺服器推送訊息到手機
限制：         需要 Google 帳號
後續：         演變為 GCM（2012）
```

### 實作範例

```java
// C2DM 註冊
public void onRegister(View view) {
    Intent intent = new Intent("com.google.android.c2dm.intent.REGISTER");
    intent.putExtra("app", PendingIntent.getBroadcast(this, 0,
        new Intent(), 0));
    intent.putExtra("sender", SENDER_ID);
    startService(intent);
}

// 接收訊息
public class C2DMReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals("com.google.android.c2dm.intent.RECEIVE")) {
            String payload = intent.getStringExtra("payload");
            // 處理訊息
        }
    }
}
```

## 遠端存取

### App Engine 整合

```python
# App Engine 後端
import webapp2
import json

class DeviceHandler(webapp2.RequestHandler):
    def post(self):
        device_id = self.request.get('device_id')
        data = self.request.get('data')

        # 儲存資料
        device = Device( device_id=device_id, data=data )
        device.put()

        # 回傳確認
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({'status': 'ok'}))
```

### 客戶端實作

```java
// Android 客戶端上傳
public void uploadData(String data) {
    HttpClient client = new DefaultHttpClient();
    HttpPost post = new HttpPost("http://yourapp.appspot.com/api/device");

    try {
        List<NameValuePair> params = new ArrayList<>();
        params.add(new BasicNameValuePair("device_id",
            Settings.Secure.getString(getContentResolver(),
                Settings.Secure.ANDROID_ID)));
        params.add(new BasicNameValuePair("data", data));

        post.setEntity(new UrlEncodedFormEntity(params));
        client.execute(post);
    } catch (Exception e) {
        Log.e("Upload", e.getMessage());
    }
}
```

## 離線支援

### 離線優先架構

```
離線優先策略：
───────────────────────────
本地儲存：     SQLite、SharedPreferences
同步佇列：     待同步的資料
網路監控：     連線狀態偵測
衝突處理：     最後寫入優先或提示用戶
```

### SyncAdapter

```java
// SyncAdapter 實作
public class MySyncAdapter extends AbstractThreadedSyncAdapter {
    @Override
    public void onPerformSync(Account account, Bundle extras,
            String authority, ContentProviderClient provider,
            SyncResult syncResult) {
        // 從伺服器取得新資料
        try {
            List<Item> serverItems = fetchFromServer();
            for (Item item : serverItems) {
                // 更新本地資料庫
                updateLocal(item);
            }
        } catch (Exception e) {
            syncResult.stats.numIoExceptions++;
        }
    }
}
```

---

## 結論

雲端與手機的結合在 2010 年已成為明顯趨勢。Google、Apple、微軟都在建立自己的雲端生態系。對於開發者來說，理解雲端整合是建立現代應用的必備技能。

---

*本期文章到此結束。*