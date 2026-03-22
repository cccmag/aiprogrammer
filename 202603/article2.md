# TypeScript 6.0 登場：型別系統的再進化

## 前言

微軟於 2026 年 3 月正式發布 TypeScript 6.0，這是近年來幅度最大的版本更新。TypeScript 6.0 不僅帶來了更智慧的型別推論，還引入了多項實驗性功能，為 JavaScript 生態系的型別安全樹立新標竿。

## 型別推論的重大突破

### 自動深度推斷

TypeScript 6.0 的一大亮點是「自動深度推斷」功能。過去，當處理複雜的巢狀結構時，編譯器往往無法正確推斷所有型別。現在，這個問題得到了顯著改善。

```typescript
// 過去需要手動註解
const data = {
    users: [
        { name: "Alice", profile: { age: 30, settings: { theme: "dark" } } },
        { name: "Bob", profile: { age: 25, settings: { theme: "light" } } }
    ]
} as const;

// TypeScript 6.0：自動深度推斷
const data = {
    users: [
        { name: "Alice", profile: { age: 30, settings: { theme: "dark" } } },
        { name: "Bob", profile: { age: 25, settings: { theme: "light" } } }
    ]
};
// 自動推斷為 readonly readonlyArray，巢狀屬性皆為 readonly
```

### 泛型推斷增強

```typescript
// 過去：需要明確標註回傳類型
function createReducer<S, A>(initial: S, handlers: Record<string, (state: S, action: A) => S>) {
    return (state: S = initial, action: A): S => {
        const handler = handlers[action.type];
        return handler ? handler(state, action) : state;
    };
}

// TypeScript 6.0：更智慧的推斷
function createReducer(initial, handlers) {
    // S 和 A 現在能被自動推斷
    return (state = initial, action) => {
        const handler = handlers[action.type];
        return handler ? handler(state, action) : state;
    };
}
```

## 條件式型別蒸餾

### 自動簡化複雜條件型別

TypeScript 6.0 引入了「條件式型別蒸餾」機制，能自動檢測並簡化已知的條件型別。

```typescript
// 複雜的條件型別定義
type DeepReadonly<T> = T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

// TypeScript 6.0：編譯器自動蒸餾
type DeepReadonly<T> = /* 複雜條件 */;
// 當 T = string 時，自動簡化為 string
// 當 T = { a: number } 時，自動簡化為 { readonly a: number }
```

### 效能提升

條件式型別蒸餾不僅提升程式碼可讀性，還能大幅改善大型專案的編譯速度。根據微軟的內部測試，某些使用大量條件型別的專案編譯時間減少了約 40%。

## 型別註解推斷（實驗性）

### 背景

TypeScript 一直以來都需要開發者明確標註型別（儘管有推斷輔助）。TypeScript 6.0 引入了一項實驗性功能：在某些情境下，允許省略型別宣告。

```typescript
// TypeScript 6.0（實驗性）：可以省略回傳型別
function calculateTotal(items: { price: number; quantity: number }[]) {
    // 編譯器自動推斷回傳為 number
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// 仍然支援明確標註
function calculateTotal(items: { price: number; quantity: number }[]): number {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

### 語法選擇

注意：這是一個嚴格可選的功能。要啟用它，需要在 `tsconfig.json` 中設定：

```json
{
    "compilerOptions": {
        "experimentalInferTypes": true
    }
}
```

## 其他重要改進

### 裝飾器支援 ECMAScript 2026 標準

TypeScript 6.0 正式支援 ECMAScript 2026 的裝飾器提案，這與 TC39 標準完全同步。

```typescript
// 使用新版裝飾器語法
function logged(target: any, context: ClassMethodDecoratorContext) {
    return function (this: unknown, ...args: any[]) {
        console.log(`Calling ${String(context.name)}`);
        return target.apply(this, args);
    };
}

class Calculator {
    @logged
    add(a: number, b: number): number {
        return a + b;
    }
}
```

### Template Literal Types 增強

```typescript
// 新版支援更複雜的模板字面量型別
type EventName<T extends string> = `on${Capitalize<T>}`;

type ButtonEvents = EventName<'click' | 'hover' | 'focus'>;
// 推斷為 'onClick' | 'onHover' | 'onFocus'
```

### 更好的 IDE 效能

TypeScript 6.0 的語言服務層面進行了大量優化：

- 大型專案的自動完成回應速度提升約 50%
- 重構操作的準確性大幅提高
- 跨檔案跳轉的穩定性改善

## 遷移指南

### 從 TypeScript 5.x 遷移

大部分現有程式碼應該可以直接在 TypeScript 6.0 下編譯。建議的遷移步驟：

1. 更新 `npm install -D typescript@6`
2. 執行 `tsc --init` 更新 `tsconfig.json`
3. 檢查新的 `strict` 選項
4. 執行完整建置，檢查警告

### 已知的破壞性變更

- 移除了部分已棄用的型別別名
- `lib.es2025.d.ts` 取代了 `lib.es2024.d.ts`
- 某些寬鬆的推斷行為被修正（可能需要調整類型）

## 結語

TypeScript 6.0 是近年來最具實質意義的更新。從自動深度推斷到條件式型別蒸餾，這些改進將大幅提升開發者體驗和程式碼品質。建議團隊評估新功能，在新專案中率先採用，同時確保舊專案的平穩遷移。

---

**延伸閱讀**

- [TypeScript 6.0 官方部落格](https://devblogs.microsoft.com/typescript/announcing-typescript-6-0/)
- [TypeScript 6.0 Breaking Changes](https://github.com/microsoft/TypeScript/wiki/Breaking-Changes-within-6.0)
