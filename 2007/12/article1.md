# iPhone SDK 開發指南

## 前言

2007 年 6 月，Apple 發布了 iPhone，立即在全球掀起熱潮。同年 10 月，Apple 發布了 iPhone SDK，讓開發者能夠建立原生 iPhone 應用程式。

## iPhone SDK 概述

### SDK 元件

```python
# iPhone SDK 核心元件
components = {
    'Xcode': '整合開發環境',
    'Interface Builder': '視覺化 UI 設計工具',
    'Instruments': '效能分析工具',
    'iPhone Simulator': '模擬器',
    'Documentation': '開發文件'
}
```

### 開發語言

iPhone 開發使用 Objective-C：

```objc
// Objective-C 範例
@interface HelloWorldViewController : UIViewController {
    UILabel *messageLabel;
}

@property (nonatomic, retain) UILabel *messageLabel;

- (void)viewDidLoad;
- (void)dealloc;

@end

@implementation HelloWorldViewController

@synthesize messageLabel;

- (void)viewDidLoad {
    [super viewDidLoad];
    self.view.backgroundColor = [UIColor whiteColor];

    messageLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 320, 100)];
    messageLabel.text = @"Hello, iPhone!";
    messageLabel.textAlignment = UITextAlignmentCenter;
    [self.view addSubview:messageLabel];
}

- (void)dealloc {
    [messageLabel release];
    [super dealloc];
}

@end
```

## Cocoa Touch 框架

### UIKit

```objc
// UIViewController 生命週期
- (void)viewDidLoad {
    // 視圖載入完成
}

- (void)viewWillAppear:(BOOL)animated {
    // 視圖即將顯示
}

- (void)viewDidAppear:(BOOL)animated {
    // 視圖已顯示
}
```

### 常用 UI 元件

| 元件 | 說明 |
|------|------|
| UIView | 基礎視圖 |
| UILabel | 文字標籤 |
| UIButton | 按鈕 |
| UITextField | 文字輸入框 |
| UITableView | 表格視圖 |
| UINavigationController | 導航控制器 |

## MVC 設計模式

```objc
// Model
@interface Article : NSObject {
    NSString *title;
    NSString *content;
    NSDate *publishedDate;
}

@property (nonatomic, retain) NSString *title;
@property (nonatomic, retain) NSString *content;
@property (nonatomic, retain) NSDate *publishedDate;

@end

// View
// Interface Builder 中設計

// Controller
@interface ArticleListViewController : UITableViewController {
    NSArray *articles;
}

@property (nonatomic, retain) NSArray *articles;

@end
```

## 資料儲存

### NSUserDefaults

```objc
// 使用 NSUserDefaults 儲存設定
NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
[defaults setObject:@"user_name" forKey:@"user_name"];
[defaults synchronize];
```

### SQLite

```objc
// 使用 SQLite 儲存結構化資料
#import <sqlite3.h>

- (void)createDatabase {
    sqlite3 *database;
    sqlite3_open("app.db", &database);

    char *errorMessage;
    const char *createSQL = "CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT);";
    sqlite3_exec(database, createSQL, NULL, NULL, &errorMessage);
}
```

## 網路程式設計

```objc
// 使用 NSURLConnection 發送網路請求
- (void)fetchData:(NSString *)urlString {
    NSURL *url = [NSURL URLWithString:urlString];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];

    NSURLConnection *connection = [NSURLConnection connectionWithRequest:request delegate:self];
}
```

## 結語

iPhone SDK 開創了行動應用開發的新時代。觸控介面、豐富的 API、以及 App Store 的分銷模式，改變了整個軟體產業。

---

## 延伸閱讀

- [iPhone+SDK+2007+development](https://www.google.com/search?q=iPhone+SDK+2007+development)
- [iOS+Objective-C+programming](https://www.google.com/search?q=iOS+Objective-C+programming)

---