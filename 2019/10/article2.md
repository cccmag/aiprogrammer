# TypeScript 3.7 發布：可選鏈與空值合併

## 前言

TypeScript 3.7 於 2019 年 11 月發布，帶來了多項開發者期待已久的功能。本篇文章將深入解析可選鏈和空值合併這兩個最重要的新特性。

## 可選鏈（Optional Chaining）

### 問題的由來

在 TypeScript 3.7 之前，處理深層嵌套物件的屬性訪問非常麻瑣：

```typescript
// 傳統方式：需要層層檢查
let streetName: string;
if (user && user.address && user.address.street) {
    streetName = user.address.street;
} else {
    streetName = undefined;
}
```

### 可選鏈語法

TypeScript 3.7 引入的可選鏈允許你安全地訪問深層嵌套的屬性：

```typescript
// 使用可選鏈
const streetName = user?.address?.street;
```

### 三種使用形式

**可選屬性訪問**

```typescript
const name = person?.name;
```

**可選呼叫**

```typescript
const result = obj?.method?.();
```

**可選元素訪問**

```typescript
const item = arr?.[0];
```

### 實際應用

```typescript
// 複雜的 API 回應處理
interface ApiResponse {
    data?: {
        user?: {
            profile?: {
                name: string;
                avatar?: string;
            };
        };
    };
}

function getUserName(response: ApiResponse): string | undefined {
    return response?.data?.user?.profile?.name;
}
```

### 與短路求值

可選鏈會自動短路：

```typescript
// 如果 obj 為 null 或 undefined，不會執行後面的訪問
const value = obj?.foo?.bar;

// 相當於
const value = obj === null || obj === undefined ? undefined : obj.foo?.bar;
```

## 空值合併（Nullish Coalescing）

### 問題的由來

在 TypeScript 3.7 之前，我們經常需要使用邏輯運算子來處理預設值：

```typescript
// || 的問題
const name = inputName || "Default";  // 0、''、false 也會被當作預設值
```

### 空值合併運算子

`??` 運算子只在值為 `null` 或 `undefined` 時使用預設值：

```typescript
// 空值合併
const name = inputName ?? "Default";

// 與 || 的比較
console.log(0 ?? "Default");      // 輸出：0
console.log(0 || "Default");      // 輸出：Default

console.log("" ?? "Default");     // 輸出：""
console.log("" || "Default");     // 輸出：Default

console.log(false ?? "Default");   // 輸出：false
console.log(false || "Default");  // 輸出：Default
```

### 實際應用

```typescript
// 配置項處理
interface Config {
    timeout?: number;
    retries?: number;
    endpoint?: string;
}

function loadConfig(defaultConfig: Config): Config {
    return {
        timeout: config.timeout ?? 3000,
        retries: config.retries ?? 5,
        endpoint: config.endpoint ?? "/api"
    };
}

// 深度可選屬性
function getNestedValue(obj: any, path: string): string | undefined {
    return path.split('.').reduce((acc, key) => acc?.[key], obj);
}
```

### 組合使用

可選鏈和空值合併經常一起使用：

```typescript
// 從設定檔案中讀取值，不存在則使用預設值
const dbPort = config.database?.port ?? 5432;
const cacheSize = config.cache?.size ?? 1000;
```

## Assertion Functions

### 新增類型斷言

TypeScript 3.7 引入了 Assertion Functions（一種特殊的函式）：

```typescript
function assert(condition: unknown, message?: string): asserts condition {
    if (!condition) {
        throw new Error(message || "Assertion failed");
    }
}

// 使用
function process(data: string | null) {
    assert(data !== null);
    // 在這裡，TypeScript 知道 data 不為 null
    console.log(data.toUpperCase());
}
```

### 自定義斷言函式

```typescript
interface Cat {
    meow(): void;
}

function isCat(animal: unknown): animal is Cat {
    return (animal as Cat)?.meow !== undefined;
}
```

## 其他改進

### Smart Selection

編輯器現在可以智慧地選取或取消選取包圍的程式碼：

```typescript
// 選取這段程式碼
if (condition) {
    doSomething();
}

// 取消包圍
if (condition)
    doSomething();
```

### 無外部參照檔案中的宣告

TypeScript 3.7 優化了只有一個檔案時的類型檢查效能。

## TypeScript 3.7 的問題修復

這個版本也修復了多個長期存在的問題：

- 遞迴類型的處理
- ES Proxy 的類型支援
- 枚舉類型的改進

## 結論

TypeScript 3.7 的新特性極大地提升了開發者體驗。可選鏈讓處理嵌套物件變得優雅，空值合併解決了 `||` 運算子的痛點。這些功能在其他語言（如 C#、Swift）已經存在，TypeScript 終於跟上了腳步。

---

**延伸閱讀**

- [TypeScript 3.7 Release Notes](https://www.google.com/search?q=TypeScript+3.7+release+notes)
- [Optional Chaining RFC](https://www.google.com/search?q=TypeScript+optional+chaining+proposal)
- [Nullish Coalescing RFC](https://www.google.com/search?q=TypeScript+nullish+coalescing+proposal)