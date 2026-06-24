# 主題四：平板專用 App 開發

## iOS 開發

### Xcode 與 Objective-C

2010 年的 iOS 開發環境：

```
開發工具鏈：
──────────────────
Xcode 3.6：    整合開發環境
Objective-C：  主要程式語言
Interface Builder： UI 設計工具
Instruments：   效能分析工具
```

### 基本 iOS 應用結構

```objc
// AppDelegate.h
@interface AppDelegate : UIResponder <UIApplicationDelegate>
@property (strong, nonatomic) UIWindow *window;
@end

// AppDelegate.m
@implementation AppDelegate

- (BOOL)application:(UIApplication *)application
    didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    self.window = [[UIWindow alloc] initWithFrame:
                   [[UIScreen mainScreen] bounds]];
    self.window.rootViewController =
        [[UIViewController alloc] init];
    [self.window makeKeyAndVisible];
    return YES;
}

@end
```

### UIViewController 生命週期

```objc
@implementation MyViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // 視圖載入完成
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    // 視圖即將顯示
}

- (void)viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];
    // 視圖已顯示
}

- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];
    // 視圖即將消失
}

- (void)viewDidDisappear:(BOOL)animated {
    [super viewDidDisappear:animated];
    // 視圖已消失
}

@end
```

### iPad 專用視圖控制器

```objc
// 分割視圖（Split View Controller）
UISplitViewController *splitVC =
    [[UISplitViewController alloc] init];

// 彈出視圖（Popover）
UIPopoverController *popover =
    [[UIPopoverController alloc]
        initWithContentViewController:detailVC];

[popover presentPopoverFromBarButtonItem:sender
                 permittedArrowDirections:UIPopoverArrowDirectionAny
                                 animated:YES];
```

### Touch 事件處理

```objc
- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    UITouch *touch = [touches anyObject];
    CGPoint location = [touch locationInView:self.view];
    NSLog(@"Touch at: %f, %f", location.x, location.y);
}

- (void)touchesMoved:(NSSet *)touches withEvent:(UIEvent *)event {
    UITouch *touch = [touches anyObject];
    CGPoint location = [touch locationInView:self.view];
    // 處理拖曳
}

- (void)touchesEnded:(NSSet *)touches withEvent:(UIEvent *)event {
    // 觸控結束
}
```

## Android 開發

### 開發環境

```
Android 開發工具鏈：
───────────────────
Eclipse + ADT：      整合開發環境
Android SDK：        SDK 工具
Dalvik  VM：         執行環境
ADB：                偵錯橋接工具
```

### 基本 Android 應用

```java
// MainActivity.java
public class MainActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }
}
```

### Android 2.1/2.2 的新特性

```java
// 複製到剪貼簿
ClipboardManager clipboard =
    (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
ClipData clip = ClipData.newPlainText("label", "text");
clipboard.setPrimaryClip(clip);

// 快速搜尋框
@Override
public boolean onSearchRequested() {
    // 開啟快速搜尋
    return super.onSearchRequested();
}
```

### 平板 UI 設計

```xml
<!-- res/layout/main.xml -->
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="horizontal">

    <!-- 側邊欄 -->
    <ListView
        android:id="@+id/list"
        android:layout_width="200dp"
        android:layout_height="match_parent" />

    <!-- 主內容區 -->
    <FrameLayout
        android:id="@+id/content"
        android:layout_width="0dp"
        android:layout_height="match_parent"
        android:layout_weight="1" />

</LinearLayout>
```

### 觸控事件處理

```java
// 實作 OnTouchListener
view.setOnTouchListener(new View.OnTouchListener() {
    @Override
    public boolean onTouch(View v, MotionEvent event) {
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                Log.d("Touch", "DOWN at " +
                      event.getX() + ", " + event.getY());
                return true;
            case MotionEvent.ACTION_MOVE:
                Log.d("Touch", "MOVE");
                return true;
            case MotionEvent.ACTION_UP:
                Log.d("Touch", "UP");
                return true;
        }
        return false;
    }
});
```

## 跨平台開發框架

### PhoneGap / Cordova

2010 年的 PhoneGap 是早期跨平台框架代表：

```html
<!-- HTML 應用結構 -->
<!DOCTYPE html>
<html>
<head>
    <title>PhoneGap App</title>
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">
    <script src="cordova.js"></script>
</head>
<body>
    <h1>Hello平板</h1>
    <button onclick="showAlert()">按鈕</button>
    <script>
        function showAlert() {
            navigator.notification.alert(
                '訊息',
                null,
                '標題',
                '確定'
            );
        }
    </script>
</body>
</html>
```

```javascript
// PhoneGap API 存取
document.addEventListener('deviceready', () => {
    // 設備準備完成
    console.log(Cordova.version);

    // 相機 API
    navigator.camera.getPicture(
        (imageData) => {
            document.getElementById('photo').src =
                'data:image/jpeg;base64,' + imageData;
        },
        (error) => console.error(error),
        { quality: 50 }
    );
});
```

### Titanium Mobile

```javascript
// Titanium 範例
var win = Ti.UI.createWindow({
    title: '平板應用',
    backgroundColor: 'white'
});

var button = Ti.UI.createButton({
    title: '點擊我',
    width: 200,
    height: 50,
    top: 100
});

button.addEventListener('click', () => {
    alert('按鈕被點擊了！');
});

win.add(button);
win.open();
```

## 開發工具比較

| 特性 | Xcode | Eclipse ADT | PhoneGap |
|------|-------|-------------|----------|
| 平台 | iOS | Android | 跨平台 |
| 語言 | Objective-C | Java | HTML/CSS/JS |
| 學習曲線 | 高 | 中 | 低 |
| 效能 | 最佳 | 佳 | 中 |
| 原生 API | 完整 | 完整 | 有限 |
| UI 設計 | Interface Builder | XML | HTML |

## App 發布

### iOS App Store

```bash
# Xcode 建置流程
1. 設定 Code Signing
2. 建置 Release 版本
3. 驗證 App
4. 提交至 App Store
5. 等待審核（7-14天）
```

### Android Market

```bash
# Android 發布流程
1. 移除除錯程式碼
2. 申請開發者帳號（$25）
3. 簽署 APK
4. 上傳至 Android Market
5. 審核（數小時至數天）
```

### 訂價策略

```
App 訂價考量：
─────────────────
免費：     累積用戶、廣告收入
付費：     直接營收
 Freemium： 免費下載、付費功能
內購：     遊戲虛寶、功能擴展
訂閱：     持續服務、內容供應
```

---

## 結論

平板 App 開發在 2010 年正處於起飛階段。iOS 平台有成熟工具和完整生態系，Android 平台則以開放性和多元硬體取勝。跨平台框架如 PhoneGap 提供另一種選擇，但在效能和原生功能上仍有差距。

選擇開發方式時應考慮：
1. 目標平台
2. 效能需求
3. 團隊技能
4. 發布時程
5. 長期維護成本

---

*本期文章到此結束。*