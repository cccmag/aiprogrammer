# Go 1.9：Type Aliases 與並發改進

## 前言

Go 1.9 於 2017 年 8 月發布，引入了 Type Aliases 和其他改進，使得 Go 語言更適合大規模軟體開發。

## Type Aliases

```go
// Type Alias 允許為現有類型建立別名
type Timestamp = int64

// 這對於重構很有用
type UserStore = map[string]*User

// 介面也支援別名
type DataReader = io.Reader
```

## 並發改進

```go
// sync.Map 併發安全
var m sync.Map

// 儲存和讀取
m.Store("key", "value")
value, ok := m.Load("key")

// 更好的goroutine排程
```

## 泛型的替代方案

Go 1.9 透過 Type Alias 和介面組合來實現部分泛型功能：

```go
// 使用介面定義通用操作
type Number interface {
    int | int64 | float64
}

func Sum[T Number](a, b T) T {
    return a + b
}
```

## Go 在微服務的應用

Go 的高效能和簡潔語法使其成為 AI 服務的理想語言：

```go
// AI 推理 HTTP 服務
func inferenceHandler(w http.ResponseWriter, r *http.Request) {
    var req InferenceRequest
    json.NewDecoder(r.Body).Decode(&req)

    result := model.Predict(req.Input)

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(result)
}
```

---

**延伸閱讀**

- [Go 1.9 Release Notes](https://www.google.com/search?q=Go+1.9+release)
- [Type Aliases Proposal](https://www.google.com/search?q=Go+type+aliases+proposal)