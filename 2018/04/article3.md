# TypeScript 3.0 發布：Project References

## 前言

2018 年 7 月，Microsoft 發布 TypeScript 3.0，引入了 Project References 功能，極大地改善了大型 TypeScript 專案的開發體驗。

## Project References

### 解決什麼問題？

在大型專案中，多個 package 可能相互依賴。手動管理編譯順序非常繁瑣。

### 如何使用

```json
// tsconfig.json
{
    "references": [
        { "path": "../shared" },
        { "path": "../utils" }
    ]
}
```

的好處：
1. 自動解析依賴順序
2. 支援「build mode」增量編譯
3. 更好的 IDE 支援

## 其他 TypeScript 3.0 新特性

### 1. 預設引導類型參數

```typescript
function merge<T = string>(x: T, y: T): T {
    return // ... 合並邏輯
}
```

### 2. 更寬鬆的 this 類型

### 3. 更好的 JSX 支援

### 4. 新的 Build Mode

```bash
tsc --build
```

## 結論

TypeScript 3.0 的 Project References 讓大型 TypeScript 專案的管理變得更加簡單。

---

**延伸閱讀**

- [TypeScript 3.0 發布說明](https://www.google.com/search?q=TypeScript+3.0+release+notes)
- [TypeScript 官方網站](https://www.google.com/search?q=TypeScript+official+site)