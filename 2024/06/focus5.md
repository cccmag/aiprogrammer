# 資料持久化：Core Data

## 為什麼需要資料持久化

幾乎所有 iOS 應用程式都需要保存資料。無論是使用者的設定偏好、筆記內容、購物清單還是遊戲進度，資料都需要在應用重新啟動後仍然存在。iOS 提供了多種資料持久化方案，其中 Core Data 是最成熟和全面的解決方案。

## Core Data 概述

Core Data 是 Apple 在 2005 年推出的物件關聯映射框架。它位於應用程式與持久化儲存（通常是 SQLite 資料庫）之間，提供了一個高層次的資料管理介面：

```
Application ↔ Core Data Stack ↔ SQLite
```

Core Data 不是資料庫，而是管理記憶體中物件圖的框架。它自動處理物件的生命週期、變更追蹤、關聯管理和資料持久化。

## Core Data 堆疊

Core Data 的核心元件包含：

### NSManagedObjectModel

資料模型描述檔（`.xcdatamodeld`），定義了實體（Entity）、屬性（Attribute）和關聯（Relationship）。你可以在 Xcode 的模型編輯器中可視化地設計資料結構。

```swift
// 對應到模型中的 User 實體
class User: NSManagedObject {
    @NSManaged var name: String
    @NSManaged var age: Int16
    @NSManaged var emails: NSSet?
}
```

### NSPersistentContainer

負責管理整個 Core Data 堆疊的容器。iOS 10 之後，開發者只需建立一個容器實例：

```swift
let container = NSPersistentContainer(name: "MyApp")
container.loadPersistentStores { _, error in
    if let error = error { print("Failed: \(error)") }
}
```

### NSManagedObjectContext

管理物件上下文，所有資料操作都在上下文中進行：

```swift
let context = container.viewContext
```

## CRUD 操作

### 建立（Create）

```swift
let user = User(context: context)
user.name = "Alice"
user.age = 30
try? context.save()
```

### 讀取（Read）

```swift
let request = User.fetchRequest()
request.predicate = NSPredicate(format: "age > %d", 18)
let results = try? context.fetch(request) as? [User]
```

### 更新（Update）

```swift
user.age = 31
try? context.save()
```

### 刪除（Delete）

```swift
context.delete(user)
try? context.save()
```

## SwiftData：Core Data 的現代化

2023 年，Apple 在 iOS 17 中推出了 SwiftData，這是 Core Data 的 Swift 原生替代方案。SwiftData 使用宏（Macro）和 Swift 的現代語法，大幅簡化了資料模型定義：

```swift
import SwiftData

@Model
class User {
    var name: String
    var age: Int
    var notes: [Note]
    
    init(name: String, age: Int) {
        self.name = name
        self.age = age
        self.notes = []
    }
}
```

SwiftData 與 SwiftUI 深度整合，支援 `@Query` 屬性包裝器自動查詢和更新 UI：

```swift
struct UserList: View {
    @Query(sort: \User.name) var users: [User]
    
    var body: some View {
        List(users) { user in
            Text(user.name)
        }
    }
}
```

## 檔案儲存

除了 Core Data，iOS 也支援直接檔案讀寫。應用程式的沙箱目錄包含：

- `Documents/`：使用者產生的資料，會備份到 iCloud
- `Library/Caches/`：快取資料，不會備份
- `tmp/`：暫存檔案，系統可能隨時清除

## 使用建議

- 簡單資料使用 `UserDefaults`
- 結構化資料使用 Core Data 或 SwiftData
- 大量檔案使用檔案系統
- 考慮使用 CloudKit 實現雲端同步

## 延伸閱讀

- [Core Data 官方文檔](https://www.google.com/search?q=Core+Data+Apple+documentation)
- [SwiftData 入門](https://www.google.com/search?q=SwiftData+tutorial)
- [Core Data vs SwiftData](https://www.google.com/search?q=Core+Data+vs+SwiftData)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」iOS 開發入門系列之五。*
