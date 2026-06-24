# Go 1.13 發布：Go Module 正式登場

## 前言

Go 1.13 於 2019 年 9 月正式發布。這是自 Go Module 引入以來最重要的版本，Module 功能正式成為默認的依賴管理方式。本文將詳細解析 Go 1.13 的重要更新。

## Go Module 的成熟

### go.mod 和 go.sum

Go 1.13 正式將 Module 功能設為默認：

```bash
# 初始化新專案
go mod init example.com/myproject

# 自動下載依賴
go mod tidy

# 構建
go build
```

### 語義導入版本控制（Semantic Import Versioning）

```go
// 不同的 major 版本作為不同的模組
import (
    "example.com/foo/v2"  // v2+
    "example.com/foo/v3" // v3+
)
```

---

## 錯誤處理改進

### errors.Is 和 errors.As

```go
import "errors"

var ErrNotFound = errors.New("not found")

// 使用 errors.Is 檢查錯誤
if errors.Is(err, ErrNotFound) {
    fmt.Println("資源不存在")
}

// 自定義錯誤類型
type ValidationError struct {
    Field string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s", e.Field)
}

// 使用 errors.As 斷言錯誤類型
var ve *ValidationError
if errors.As(err, &ve) {
    fmt.Printf("驗證錯誤: %s\n", ve.Field)
}
```

---

## 數字字面量改進

### 數字下劃線

```go
million := 1_000_000
pi := 3.14_159_265
hex := 0xFF_DE_AD_BE_EF
binary := 0b1111_1111
```

---

## 其他更新

### Go vet 改進

```bash
go vet ./...
```

### 競技場記憶體優化

即將引入的 arena 功能，優化記憶體使用。

---

## 結語

Go 1.13 標誌著 Go Module 生態的成熟，為 Go 開發者提供了更好的依賴管理體驗。

---

**延伸閱讀**

- [Go 1.13 Release Notes](https://www.google.com/search?q=Go+1.13+release+notes)
- [Go Modules](https://www.google.com/search?q=Go+modules+tutorial)