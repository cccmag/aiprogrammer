# 主題五：UI 設計模式

## Android UI 架構

### 核心元件

```
Android UI 核心類別：
───────────────────────────
Activity：       單一螢幕容器
View：          基本 UI 元件
ViewGroup：     容器元件（Layout）
Fragment：      可重用的 UI 區塊（2.2+ 不支援）
```

## Activity 生命週期

### 生命週期圖

```
Activity 生命週期：
───────────────────────────
onCreate()        建立 activity
    ↓
onStart()         可見但無焦點
    ↓
onResume()        可互動
    ↓
[執行中]
    ↓
onPause()         失去焦點
    ↓
onStop()          不可見
    ↓
onDestroy()       銷毀
    ↓
onRestart()       重新開始
```

### 程式碼範例

```java
public class MyActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        Log.d("MyActivity", "onCreate");
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.d("MyActivity", "onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d("MyActivity", "onResume");
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.d("MyActivity", "onPause");
    }

    @Override
    protected void onStop() {
        super.onStop();
        Log.d("MyActivity", "onStop");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d("MyActivity", "onDestroy");
    }
}
```

## Layout 系統

### 常見 Layout

```
Layout 型別：
───────────────────────────
LinearLayout：    線性排列
RelativeLayout： 相對定位
FrameLayout：     框架佈局
TableLayout：     表格佈局
AbsoluteLayout：  絕對定位（已棄用）
```

### LinearLayout

```xml
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="標題"/>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">

        <Button android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="左"/>

        <Button android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="右"/>

    </LinearLayout>

</LinearLayout>
```

### RelativeLayout

```xml
<RelativeLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:id="@+id/title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_alignParentTop="true"
        android:layout_centerHorizontal="true"
        android:text="標題"/>

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_below="@id/title"
        android:layout_alignParentLeft="true"
        android:text="按鈕"/>

</RelativeLayout>
```

## AdapterView 與 Adapter

### 常見元件

```
AdapterView 家族：
───────────────────────────
ListView：        垂直列表
GridView：        網格顯示
Spinner：         下拉選單
Gallery：         水平滾動（已棄用）
ExpandableListView： 可展開列表
```

### ListView + ArrayAdapter

```java
// 簡單的 ListView
String[] items = {"項目一", "項目二", "項目三"};
ArrayAdapter<String> adapter = new ArrayAdapter<>(
    this,
    android.R.layout.simple_list_item_1,
    items
);

ListView listView = (ListView) findViewById(R.id.list);
listView.setAdapter(adapter);
```

### 自訂 Adapter

```java
public class MyAdapter extends BaseAdapter {
    private List<Item> items;
    private Context context;

    public MyAdapter(Context context, List<Item> items) {
        this.context = context;
        this.items = items;
    }

    @Override
    public int getCount() {
        return items.size();
    }

    @Override
    public Object getItem(int position) {
        return items.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(context)
                .inflate(R.layout.list_item, parent, false);
        }

        Item item = items.get(position);
        TextView title = (TextView) convertView.findViewById(R.id.title);
        title.setText(item.getTitle());

        return convertView;
    }
}
```

### ViewHolder 模式

```java
@Override
public View getView(int position, View convertView, ViewGroup parent) {
    ViewHolder holder;

    if (convertView == null) {
        convertView = LayoutInflater.from(context)
            .inflate(R.layout.list_item, parent, false);

        holder = new ViewHolder();
        holder.title = (TextView) convertView.findViewById(R.id.title);
        holder.icon = (ImageView) convertView.findViewById(R.id.icon);

        convertView.setTag(holder);
    } else {
        holder = (ViewHolder) convertView.getTag();
    }

    Item item = items.get(position);
    holder.title.setText(item.getTitle());
    holder.icon.setImageResource(item.getIcon());

    return convertView;
}

static class ViewHolder {
    TextView title;
    ImageView icon;
}
```

## Intent 系統

### 啟動 Activity

```java
// 明確 Intent
Intent intent = new Intent(this, TargetActivity.class);
intent.putExtra("key", "value");
startActivity(intent);

// 隱含 Intent
Intent intent = new Intent(Intent.ACTION_VIEW);
intent.setData(Uri.parse("http://example.com"));
startActivity(intent);

// 取得結果
Intent intent = new Intent(this, ResultActivity.class);
startActivityForResult(intent, REQUEST_CODE);

@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
        String result = data.getStringExtra("result");
    }
}
```

### 系統 Intent

```java
// 開啟電話
Intent callIntent = new Intent(Intent.ACTION_DIAL);
callIntent.setData(Uri.parse("tel:12345678"));
startActivity(callIntent);

// 傳送簡訊
Intent smsIntent = new Intent(Intent.ACTION_SENDTO);
smsIntent.setData(Uri.parse("smsto:12345678"));
smsIntent.putExtra("sms_body", "內容");
startActivity(smsIntent);

// 開啟地圖
Intent mapIntent = new Intent(Intent.ACTION_VIEW);
mapIntent.setData(Uri.parse("geo:37.7749,-122.4194"));
startActivity(mapIntent);
```

## 選單系統

### 選單類型

```
Android 選單：
───────────────────────────
Options Menu：      Activity 頂部的選單
Context Menu：      長按出現的選單
SubMenu：          子選單
PopupMenu：        彈出式選單（3.0+）
```

### Options Menu

```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    MenuInflater inflater = getMenuInflater();
    inflater.inflate(R.menu.main_menu, menu);
    return true;
}

@Override
public boolean onOptionsItemSelected(MenuItem item) {
    switch (item.getItemId()) {
        case R.id.action_settings:
            openSettings();
            return true;
        case R.id.action_about:
            showAbout();
            return true;
        default:
            return super.onOptionsItemSelected(item);
    }
}
```

```xml
<!-- res/menu/main_menu.xml -->
<menu xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:id="@+id/action_settings"
          android:icon="@android:drawable/ic_menu_preferences"
          android:title="設定"/>
    <item android:id="@+id/action_about"
          android:icon="@android:drawable/ic_menu_info_details"
          android:title="關於"/>
</menu>
```

## 對話框

### AlertDialog

```java
// 簡單對話框
new AlertDialog.Builder(this)
    .setTitle("標題")
    .setMessage("訊息")
    .setPositiveButton("確定", new DialogInterface.OnClickListener() {
        @Override
        public void onClick(DialogInterface dialog, int which) {
            // 確定
        }
    })
    .setNegativeButton("取消", new DialogInterface.OnClickListener() {
        @Override
        public void onClick(DialogInterface dialog, int which) {
            // 取消
        }
    })
    .show();

// 列表對話框
new AlertDialog.Builder(this)
    .setTitle("選擇")
    .setItems(items, new DialogInterface.OnClickListener() {
        @Override
        public void onClick(DialogInterface dialog, int which) {
            // 處理選擇
        }
    })
    .show();
```

---

## 結論

Android UI 設計模式提供了一致的開發體驗。Activity 作為螢幕容器，Layout 負責排版，AdapterView 負責顯示列表資料，Intent 負責元件間的溝通。

掌握這些模式是建立良好 Android 應用的基礎。

---

*本期文章到此結束。*