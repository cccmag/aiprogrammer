# Core Data 資料儲存

## 建立資料模型

Core Data 的第一步是建立資料模型。在 Xcode 中建立 `.xcdatamodeld` 檔案，然後在其中定義實體（Entity）。

### 實體定義

假設我們要建立一個筆記應用，需要 Note 和 Category 兩個實體：

```swift
// Note 實體
- id: UUID
- title: String
- content: String
- createdAt: Date
- category: Category (對多關係)

// Category 實體
- id: UUID
- name: String
- color: String
- notes: NSSet? (對多關係反向)
```

### NSManagedObject 子類別

Xcode 可以自動生成 NSManagedObject 的子類別：

```swift
import Foundation
import CoreData

extension Note {
    @nonobjc class func fetchRequest() -> NSFetchRequest<Note> {
        return NSFetchRequest<Note>(entityName: "Note")
    }
    
    @NSManaged var id: UUID
    @NSManaged var title: String
    @NSManaged var content: String
    @NSManaged var createdAt: Date
    @NSManaged var category: Category?
}
```

## 使用 NSPersistentContainer

```swift
struct PersistenceController {
    static let shared = PersistenceController()
    
    let container: NSPersistentContainer
    
    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "NoteApp")
        if inMemory {
            container.persistentStoreDescriptions.first?.url = 
                URL(fileURLWithPath: "/dev/null")
        }
        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Core Data failed: \(error)")
            }
        }
    }
}
```

## CRUD 操作

### 建立

```swift
func createNote(title: String, content: String, category: Category?) {
    let context = PersistenceController.shared.container.viewContext
    let note = Note(context: context)
    note.id = UUID()
    note.title = title
    note.content = content
    note.createdAt = Date()
    note.category = category
    
    try? context.save()
}
```

### 讀取

```swift
func fetchNotes() -> [Note] {
    let context = PersistenceController.shared.container.viewContext
    let request: NSFetchRequest<Note> = Note.fetchRequest()
    request.sortDescriptors = [NSSortDescriptor(key: "createdAt", ascending: false)]
    request.predicate = NSPredicate(format: "title CONTAINS[c] %@", searchText)
    
    return (try? context.fetch(request)) ?? []
}
```

### 更新與刪除

```swift
func updateNote(_ note: Note, title: String) {
    let context = PersistenceController.shared.container.viewContext
    note.title = title
    try? context.save()
}

func deleteNote(_ note: Note) {
    let context = PersistenceController.shared.container.viewContext
    context.delete(note)
    try? context.save()
}
```

## 與 SwiftUI 整合

使用 `@FetchRequest` 屬性包裝器：

```swift
struct NoteListView: View {
    @Environment(\.managedObjectContext) private var viewContext
    @FetchRequest(
        sortDescriptors: [SortDescriptor(\.createdAt, order: .reverse)],
        predicate: nil
    ) private var notes: FetchedResults<Note>
    
    var body: some View {
        List {
            ForEach(notes) { note in
                VStack(alignment: .leading) {
                    Text(note.title ?? "")
                        .font(.headline)
                    Text(note.content ?? "")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            .onDelete(perform: deleteNotes)
        }
    }
    
    private func deleteNotes(offsets: IndexSet) {
        offsets.map { notes[$0] }.forEach(viewContext.delete)
        try? viewContext.save()
    }
}
```

## 延伸閱讀

- [Core Data 官方文檔](https://www.google.com/search?q=Core+Data+Apple+documentation)
- [Core Data 與 SwiftUI](https://www.google.com/search?q=Core+Data+SwiftUI+tutorial)
- [SwiftData 替代方案](https://www.google.com/search?q=SwiftData+Core+Data+replacement)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之九。*
