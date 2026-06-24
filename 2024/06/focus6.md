# 網路請求與 API

## iOS 網路開發簡介

現代 iOS 應用程式幾乎都離不開網路。從社群媒體的動態更新、天氣應用的即時資料，到電商應用的商品資訊，網路通訊是應用程式的生命線。iOS 提供了完善的網路框架，讓開發者可以輕鬆地與後端 API 通訊。

## URLSession

URLSession 是 Apple 官方的網路請求框架，支援 HTTP/HTTPS、FTP 等協定。它提供了非同步的請求機制，讓網路操作不會阻塞主執行緒。

### 基本用法

```swift
let url = URL(string: "https://api.example.com/users")!
let task = URLSession.shared.dataTask(with: url) { data, response, error in
    guard let data = data else { return }
    // 處理回傳資料
}
task.resume()
```

### async/await 語法

Swift 5.5 引入的 async/await 語法大幅簡化了非同步程式碼：

```swift
func fetchUsers() async throws -> [User] {
    let url = URL(string: "https://api.example.com/users")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode([User].self, from: data)
}

Task {
    let users = try await fetchUsers()
    print(users)
}
```

這種寫法讓非同步程式碼看起來就像同步程式碼一樣直覺。

## Codable 與 JSON 解析

Swift 的 Codable 協定提供了自動的 JSON 編解碼功能：

```swift
struct User: Codable, Identifiable {
    let id: Int
    let name: String
    let email: String
    let isActive: Bool
}

// JSON 解析
let decoder = JSONDecoder()
let users = try decoder.decode([User].self, from: jsonData)

// JSON 編碼
let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
let data = try encoder.encode(user)
```

### 自訂鍵名映射

當 API 回傳的鍵名與 Swift 的命名慣例不同時，可以使用 `CodingKeys`：

```swift
struct User: Codable {
    let id: Int
    let fullName: String
    
    enum CodingKeys: String, CodingKey {
        case id
        case fullName = "full_name"
    }
}
```

## 請求解構

### GET 請求

```swift
func getPosts() async throws -> [Post] {
    let url = URL(string: "https://api.example.com/posts")!
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw APIError.invalidResponse
    }
    return try JSONDecoder().decode([Post].self, from: data)
}
```

### POST 請求

```swift
func createPost(title: String) async throws -> Post {
    let url = URL(string: "https://api.example.com/posts")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    let body = ["title": title]
    request.httpBody = try JSONEncoder().encode(body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode(Post.self, from: data)
}
```

## 網路層架構

### MVVM 模式

```swift
class APIService {
    static let shared = APIService()
    private let baseURL = "https://api.example.com/v1"
    
    func fetch<T: Codable>(_ endpoint: String) async throws -> T {
        let url = URL(string: "\(baseURL)/\(endpoint)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

### 錯誤處理

```swift
enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case decodingFailed
    
    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Invalid URL"
        case .invalidResponse: return "Invalid server response"
        case .decodingFailed: return "Failed to decode data"
        }
    }
}
```

## 最佳實踐

1. 使用 async/await 簡化非同步程式碼
2. 封裝網路層，避免請求邏輯散落各處
3. 處理所有錯誤情況（網路斷線、逾時等）
4. 實作請求重試機制
5. 使用快取減少不必要的網路請求

## 延伸閱讀

- [URLSession 文檔](https://www.google.com/search?q=URLSession+Apple+documentation)
- [Codable 使用指南](https://www.google.com/search?q=Swift+Codable+JSON+tutorial)
- [iOS 網路層最佳實踐](https://www.google.com/search?q=iOS+network+layer+best+practices)

---

*本篇文章為「AI 程式人雜誌 2024 年 6 月號」iOS 開發入門系列之六。*
