# URLSession 網路請求

## 現代 iOS 網路請求

在 Swift 5.5 引入 async/await 之前，iOS 開發者需要使用閉包或 Combine 框架來處理非同步網路請求。async/await 的到來徹底改變了這一切，讓網路程式碼變得前所未有的簡潔。

## URLSession 基礎

### 建立請求

```swift
let url = URL(string: "https://api.example.com/v1/users")!
var request = URLRequest(url: url)
request.httpMethod = "GET"
request.setValue("application/json", forHTTPHeaderField: "Accept")
request.timeoutInterval = 30
```

### GET 請求

```swift
func fetchUsers() async throws -> [User] {
    let url = URL(string: "https://api.example.com/users")!
    let (data, response) = try await URLSession.shared.data(from: url)
    
    guard let httpResponse = response as? HTTPURLResponse,
          (200...299).contains(httpResponse.statusCode) else {
        throw URLError(.badServerResponse)
    }
    
    return try JSONDecoder().decode([User].self, from: data)
}
```

### POST 請求

```swift
func createUser(name: String, email: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = ["name": name, "email": email]
    request.httpBody = try JSONEncoder().encode(body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(User.self, from: data)
}
```

## 錯誤處理

### 網路錯誤

```swift
enum NetworkError: LocalizedError {
    case invalidURL
    case noData
    case decodingFailed(Error)
    case serverError(Int)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Invalid URL"
        case .noData: return "No data received"
        case .decodingFailed(let error): return "Decoding failed: \(error.localizedDescription)"
        case .serverError(let code): return "Server error: \(code)"
        }
    }
}
```

## 實際使用

```swift
struct UserListView: View {
    @State private var users: [User] = []
    @State private var error: Error?
    @State private var isLoading = false
    
    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else if let error = error {
                VStack {
                    Text("Error: \(error.localizedDescription)")
                    Button("Retry") { loadUsers() }
                }
            } else {
                List(users) { user in
                    Text(user.name)
                }
            }
        }
        .task {
            await loadUsers()
        }
    }
    
    func loadUsers() async {
        isLoading = true
        error = nil
        do {
            users = try await APIService.shared.fetchUsers()
        } catch {
            self.error = error
        }
        isLoading = false
    }
}
```

## 請求管理

### 取消請求

```swift
func fetchData() async throws -> Data {
    let task = Task {
        let url = URL(string: "https://api.example.com/large-file")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }
    
    // 5 秒後超時
    Task {
        try? await Task.sleep(nanoseconds: 5_000_000_000)
        task.cancel()
    }
    
    return try await task.value
}
```

### 下載進度

```swift
let session = URLSession(configuration: .default, delegate: self, delegateQueue: nil)

// 實作 URLSessionDownloadDelegate
func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask,
                didWriteData bytesWritten: Int64,
                totalBytesWritten: Int64,
                totalBytesExpectedToWrite: Int64) {
    let progress = Double(totalBytesWritten) / Double(totalBytesExpectedToWrite)
    DispatchQueue.main.async {
        self.progress = progress
    }
}
```

## 延伸閱讀

- [URLSession 文檔](https://www.google.com/search?q=URLSession+Apple+documentation)
- [async/await 網路請求](https://www.google.com/search?q=Swift+async+await+URLSession)
- [Codable JSON 解析](https://www.google.com/search?q=Swift+Codable+JSON)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」文章集錦之八。*
