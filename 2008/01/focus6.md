# UI 設計與 Views

## Android UI 架構

Android 的使用者介面採用階層式結構，所有 UI 元件都繼承自 View 類別。

### View 層級結構

```
ViewGroup (容器)
├── View (文字標籤)
├── View (按鈕)
└── ViewGroup (子容器)
    ├── View (輸入框)
    └── View (按鈕)
```

### 核心類別

| 類別 | 說明 |
|------|------|
| View | 所有 UI 元件的基底類別 |
| ViewGroup | 可包含子 View 的容器 |
| Activity | 承載 UI 的元件 |
| Layout | 用於排版的 ViewGroup 子類別 |

## 常用 UI 元件

### TextView（文字標籤）

```xml
<TextView
    android:id="@+id/text_view"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Hello Android!"
    android:textSize="24sp"
    android:textColor="#FF0000"
    android:gravity="center" />
```

對應的 Java 程式碼：

```java
TextView textView = (TextView) findViewById(R.id.text_view);
textView.setText("New Text");
```

### Button（按鈕）

```xml
<Button
    android:id="@+id/btn_click"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="點擊我"
    android:onClick="onButtonClick" />
```

處理點擊事件：

```java
public void onButtonClick(View view) {
    Toast.makeText(this, "按鈕被點擊了！", Toast.LENGTH_SHORT).show();
}
```

### EditText（輸入框）

```xml
<EditText
    android:id="@+id/edit_name"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:hint="請輸入姓名"
    android:inputType="textPersonName" />
```

取得輸入內容：

```java
EditText editName = (EditText) findViewById(R.id.edit_name);
String name = editName.getText().toString();
```

### ImageView（圖片）

```xml
<ImageView
    android:id="@+id/image_view"
    android:layout_width="200dp"
    android:layout_height="200dp"
    android:src="@drawable/my_image"
    android:scaleType="centerCrop" />
```

## 佈局管理器（Layout）

### LinearLayout（線性佈局）

水準或垂直排列子視圖：

```xml
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="第一項" />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="按鈕" />

</LinearLayout>
```

### RelativeLayout（相對佈局）

以相對位置排列子視圖：

```xml
<RelativeLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:id="@+id/title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="標題"
        android:layout_alignParentTop="true" />

    <Button
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="確定"
        android:layout_below="@id/title"
        android:layout_centerHorizontal="true" />

</RelativeLayout>
```

### TableLayout（表格佈局）

以表格形式排列子視圖：

```xml
<TableLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:stretchColumns="1">

    <TableRow>
        <TextView android:text="姓名：" />
        <EditText android:id="@+id/input_name" />
    </TableRow>

    <TableRow>
        <TextView android:text="電話：" />
        <EditText android:id="@+id/input_phone" />
    </TableRow>

</TableLayout>
```

### FrameLayout（框架佈局）

適用於重疊顯示的場景：

```xml
<FrameLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:src="@drawable/background" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="覆蓋在圖片上"
        android:layout_gravity="center" />

</FrameLayout>
```

## 常見屬性

### 尺寸屬性

| 屬性 | 說明 |
|------|------|
| `layout_width` | 寬度：match_parent、wrap_content、具體數值 |
| `layout_height` | 高度：match_parent、wrap_content、具體數值 |

### 內距與外距

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:padding="8dp"
    android:layout_margin="16dp"
    android:paddingLeft="16dp" />
```

### 對齊屬性

| 屬性 | 說明 |
|------|------|
| `layout_gravity` | 本身在父容器中的對齊方式 |
| `gravity` | 內容的對齊方式 |

## 實戰：建立登入畫面

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="32dp">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="登入系統"
        android:textSize="24sp"
        android:layout_marginBottom="32dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="帳號" />

    <EditText
        android:id="@+id/account"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginBottom="16dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="密碼" />

    <EditText
        android:id="@+id/password"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:inputType="textPassword"
        android:layout_marginBottom="24dp" />

    <Button
        android:id="@+id/btn_login"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="登入"
        android:layout_marginBottom="16dp" />

    <Button
        android:id="@+id/btn_register"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="註冊" />

</LinearLayout>
```

對應的 Activity 程式碼：

```java
public class LoginActivity extends Activity {
    private EditText accountEdit;
    private EditText passwordEdit;
    private Button loginButton;
    private Button registerButton;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        accountEdit = (EditText) findViewById(R.id.account);
        passwordEdit = (EditText) findViewById(R.id.password);
        loginButton = (Button) findViewById(R.id.btn_login);
        registerButton = (Button) findViewById(R.id.btn_register);

        loginButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                String account = accountEdit.getText().toString();
                String password = passwordEdit.getText().toString();
                if (validateLogin(account, password)) {
                    Toast.makeText(LoginActivity.this,
                        "登入成功", Toast.LENGTH_SHORT).show();
                }
            }
        });

        registerButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this,
                    RegisterActivity.class);
                startActivity(intent);
            }
        });
    }

    private boolean validateLogin(String account, String password) {
        return !account.isEmpty() && !password.isEmpty();
    }
}
```

---

**延伸閱讀**

- [Android UI development](https://www.google.com/search?q=Android+UI+development+tutorial)
- [Android+Layout+tutorials](https://www.google.com/search?q=Android+Layout+tutorials)
- [View+and+ViewGroup](https://www.google.com/search?q=Android+View+and+ViewGroup)