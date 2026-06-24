# Go 2.0 草案出爐：泛型增強與錯誤處理新語法

## 前言

Go 語言團隊於 2026 年 3 月發布了 Go 2.0 的初步草案，標誌著這個由 Google 支援的語言即將迎來十年來最大的變革。草案聚焦於三個核心領域：泛型增強、錯誤處理新語法，以及結構化日誌標準庫。本文帶您搶先了解這些令人期待的改進。

## 泛型增強

### Go 1.18 引入泛型以來

Go 在 2022 年發布的 1.18 版本中正式引入了泛型支援。然而，早期的實現較為保守，存在諸多限制。Go 2.0 草案旨在解決這些痛點。

### 新增的型別約束

```go
// 過去：自訂型別約束語法冗長
type Number interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
    ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
    ~float32 | ~float64
}

func Max[T Number](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// Go 2.0：內建型別約束
func Max[T constraints.Float | constraints.Integer](a, b T) T {
    if a > b {
        return a
    }
    return b
}
```

### 多返回值約束

```go
// 過去：無法直接約束多返回值函式
// Go 2.0：支援多返回值約束
type Iterator[T any] interface {
    ~func() (T, bool) | ~func() (T, error)
}

func Collect[T any, I Iterator[T]](iter I) []T {
    var result []T
    for v, ok := iter(); ok; v, ok = iter() {
        result = append(result, v)
    }
    return result
}
```

### 型別集增強

```go
// 過去：型別集表達式功能有限
type Number interface {
    ~int | ~float64 | ~complex128
}

// Go 2.0：支援更複雜的型別集
type ComparableOrdered interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64 |
    ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
    ~float32 | ~float64 | ~string
    
    // 內建比較運算子約束
    type Comparable
}

func Sort[T ComparableOrdered](slice []T) []T {
    sort.Slice(slice, func(i, j int) bool {
        return slice[i] < slice[j]
    })
    return slice
}
```

## 錯誤處理新語法

### 現有錯誤處理的痛點

Go 的錯誤處理長期以來是社群討論的焦點。現有的 `if err != nil` 模式雖然簡單明瞭，但在處理多個可能錯誤的流程時會導致深層嵌套：

```go
// 現有模式：深層嵌套
result, err := step1()
if err != nil {
    return nil, err
}
result, err = step2(result)
if err != nil {
    return nil, err
}
result, err = step3(result)
if err != nil {
    return nil, err
}
return process(result), nil
```

### try 表達式

Go 2.0 草案引入了類似 C# 的 `try` 表達式：

```go
// 新語法：簡潔的錯誤傳播
result := try step1()
result = try step2(result)
result = try step3(result)
return try process(result)

// 完整版本
result, err := step1()
if err != nil {
    return nil, err
}
result, err = step2(result)
if err != nil {
    return nil, err
}
result, err = step3(result)
if err != nil {
    return nil, err
}
return process(result), nil
```

### 錯誤鏈增強

```go
// Go 2.0：更好的錯誤包裝
import "errors"

func readConfig(path string) error {
    data, err := os.ReadFile(path)
    if err != nil {
        // 新語法：鏈式錯誤
        return errors.Wrap(err, "reading config file {path}")
    }
    
    // 新語法：攜帶額外上下文
    return errors.Join(err,
        errors.Details("config path: {path}"),
        errors.Cause(ValidationError{Path: path})
    )
}
```

### 錯誤處理模式匹配

```go
// Go 2.0：錯誤模式匹配
switch err := process(); {
case errors.Is(err, io.EOF):
    // 處理檔案結束
case errors.Is(err, os.ErrNotExist):
    // 處理檔案不存在
case errors.As(err, &ValidationError{}):
    // 處理驗證錯誤
default:
    // 處理其他錯誤
}
```

## 結構化日誌標準庫

### logging 包

Go 2.0 將引入標準化的日誌套件，結束社群依賴第三方庫的混亂局面：

```go
import "log"

// 基本用法
log.Info("starting server", "addr", ":8080")
log.Debug("processing request", "method", "GET", "path", "/api/users")
log.Error("connection failed", "err", err)

// 結構化日誌
log.Log(logger.LevelInfo,
    "request completed",
    "method", "POST",
    "path", "/api/users",
    "status", 200,
    "duration", 125 * time.Millisecond,
)
```

### 日誌級別和過濾�

```go
import "log"

func init() {
    // 設定日誌級別
    log.SetLevel(log.LevelDebug)
    
    // 設定輸出格式
    log.SetFormat(log.JSON)  // 結構化 JSON 輸出
    // 或
    log.SetFormat(log.Text)  // 人類可讀文本
    
    // 條件過濾
    log.AddFilter(func(entry log.Entry) bool {
        return entry.Level >= log.LevelWarning || entry.Has("error")
    })
}
```

## 草案時間表

根據 Go 團隊的規劃：

- **2026 Q1-Q2**：收集社群反饋，完善草案
- **2026 Q3-Q4**：原型實現和測試
- **2027 Q1**：Go 1.24 可能包含部分特性
- **2028**：Go 2.0 正式發布

## 社群反應

Go 社群對草案反應熱烈：

**支持者觀點**：
- `try` 表達式能大幅減少樣板程式碼
- 泛型增強解決了實際的型別約束需求
- 結構化日誌標準庫結束了依賴地獄

**疑慮者觀點**：
- `try` 可能讓錯誤處理過於隱蔽
- 泛型複雜度可能讓 Go 失去簡潔性
- 草案距離正式版還有很長的路

## 結語

Go 2.0 草案展現了 Go 團隊對社群聲音的重視。這些改進瞄準了 Go 長期以來的核心痛點，有望讓 Go 在保持簡潔的同時，變得更加強大。建議 Go 開發者積極參與草案討論，為語言的未來貢獻意見。

---

**延伸閱讀**

- [Go 2.0 草案](https://www.google.com/search?q=Go+2.0+draft+proposal)
- [Go Error Handling 提案](https://www.google.com/search?q=Go+error+handling+proposal)
- [Go Generics 增強提案](https://www.google.com/search?q=Go+generics+enhancement)
