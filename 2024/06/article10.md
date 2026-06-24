# iOS 效能與除錯

## 效能分析的重要性

iOS 應用程式的使用者對流暢度有極高的期待。一個卡頓的滾動、緩慢的啟動或過多的耗電，都可能導致使用者卸載你的應用。因此，效能分析與除錯是 iOS 開發中不可或缺的技能。

## Instruments

Instruments 是 Xcode 內建的強大效能分析工具集。它可以檢測應用的 CPU 使用率、記憶體分配、磁碟讀寫、網路活動等。

### Time Profiler

Time Profiler 是最常用的 Instruments 工具，用於分析 CPU 使用情況：

```swift
// 可能的效能瓶頸範例
func loadImages() {
    for url in urls {
        let data = try? Data(contentsOf: url)  // 同步載入會阻塞主執行緒
        // 應該改用非同步載入
    }
}
```

Time Profiler 會告訴你哪個函式花費了最多 CPU 時間，幫助你找到熱點。

### Allocations

Allocations 工具追蹤記憶體的分配和釋放。它可以幫助發現：

- 記憶體洩漏
- 過度分配
- 大型物件的不必要保留

```swift
// 記憶體洩漏範例
class LeakyClass {
    var closure: (() -> Void)?
    
    func setup() {
        closure = { [self] in  // 強引用循環
            print(self)
        }
    }
}
```

### Leaks 檢測

Leaks 工具自動檢測引用循環和未釋放的記憶體。它會在你的應用執行時持續監控，發現洩漏時發出警告。

## Xcode 除錯功能

### 中斷點

Xcode 的除錯器支援多種中斷點：

- 行中斷點：在特定行暫停執行
- 符號中斷點：在特定函式被調用時暫停
- 異常中斷點：在拋出異常時暫停
- 條件中斷點：符合特定條件時暫停

```swift
// 設定條件中斷點
// 在 count > 100 時暫停
for i in 0..<1000 {
    print(i)  // 在此行設定條件中斷點：i > 100
}
```

### LLDB 命令

除錯時可以在 LLDB 控制台輸入命令：

```
// 常用 LLDB 命令
po variableName    // 列印物件的詳細資訊
expr variable = 10 // 修改變數值
bt                // 顯示呼叫堆疊
continue          // 繼續執行
```

### View Debugging

Xcode 的 View Hierarchy 除錯器可以 3D 檢視所有的 UI 層次：

1. 在執行應用時點擊 Debug View Hierarchy 按鈕
2. 使用 3D 檢視查看 UI 元件的層疊關係
3. 檢查 Auto Layout 約束問題

## 常見效能問題

### 主執行緒阻塞

```swift
// 錯誤：在主執行緒執行耗時操作
DispatchQueue.main.async {
    let data = try? Data(contentsOf: url)  // 阻塞主執行緒！
}

// 正確：使用 async/await
func loadData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}
```

### 圖片載入

```swift
// 避免在主執行緒載入大型圖片
Image(uiImage: UIImage(contentsOfFile: path)!)  // 主執行緒阻塞
```

使用 `AsyncImage` 或快取機制：

```swift
AsyncImage(url: URL(string: imageUrl)) { phase in
    switch phase {
    case .success(let image):
        image.resizable()
    case .failure:
        Image(systemName: "photo")
    case .empty:
        ProgressView()
    @unknown default:
        EmptyView()
    }
}
```

## 延伸閱讀

- [Instruments 使用指南](https://www.google.com/search?q=Xcode+Instruments+guide)
- [iOS 效能最佳化](https://www.google.com/search?q=iOS+performance+optimization)
- [LLDB 除錯命令](https://www.google.com/search?q=LLDB+debugging+commands)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之十。*
