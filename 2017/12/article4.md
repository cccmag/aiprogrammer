# Go 生態：雲端與微服務

## 前言

Go 語言在 2017 年繼續在雲端和微服務領域保持領先地位，Docker 和 Kubernetes 等重要工具都是用 Go 開發的。

## Go 1.9

```go
// Go 1.9 新特性

// Type Aliases
type UserStore = map[string]*User

// 并發 Map
var syncMap sync.Map
syncMap.Store("key", "value")
value, ok := syncMap.Load("key")

// Monotonic Time
start := time.Now().UnixMono()
```

## Go 的優勢

```go
// Go 語言核心優勢

// 1. 簡潔語法
func greet(name string) string {
    return "Hello, " + name
}

// 2. 內建併發
func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- j * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }
}

// 3. 快速編譯
// go build -o myapp main.go

// 4. 靜態連結
// 單一二進位檔案部署
```

## 雲端原生工具

```go
// Docker (用 Go 編寫)
// Kubernetes (用 Go 編寫)

// 簡單的 HTTP 伺服器
package main

import (
    "encoding/json"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
    Status  int    `json:"status"`
}

func handler(w http.ResponseWriter, r *http.Request) {
    response := Response{
        Message: "Hello, World!",
        Status:  200,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/", handler)
    http.ListenAndServe(":8080", nil)
}
```

## AI 服務

```go
// 使用 Go 構建 AI 微服務

// gRPC 服務定義
// proto 檔案
//syntax = "proto3";
//
//service ImageClassifier {
//    rpc Classify(Image) returns (ClassificationResult) {}
//}

// Go 實現
type server struct{}

func (s *server) Classify(ctx context.Context, img *Image) (*ClassificationResult, error) {
    // AI 推論邏輯
    return &ClassificationResult{
        Label:      "cat",
        Confidence: 0.95,
    }, nil
}
```

## 2018 年展望

Go 1.11 預計帶來：
- Go Modules (vgo)
- WebAssembly 支援
- 更好的效能

---

**延伸閱讀**

- [Go Official](https://www.google.com/search?q=Go+official)
- [Go at Google](https://www.google.com/search?q=go+language+google+cloud)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*