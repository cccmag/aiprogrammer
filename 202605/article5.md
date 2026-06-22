# TypeScript 6.0 發布：型別系統的再進化

## 前言

2026 年 4 月，Microsoft 正式發布了 TypeScript 6.0——這是自 TS 5.0 以來型別系統最大的一次進化。核心特性包括**依賴型別**（Dependent Types）、**編譯期巨集**（Compile-time Macros）以及全新的**型別模式匹配**。本文深入解析 TypeScript 6.0 的新特性。

## 依賴型別：值與型別的統一

### 什麼是依賴型別？

依賴型別允許型別依賴於執行期的值。這是 TypeScript 邁向「證明助理」級別型別系統的第一步：

```typescript
// TypeScript 6.0：依賴型別基礎
function createArray<T, N extends number>(value: T, count: N): T[] & { length: N } {
    return Array.from({ length: count }, () => value) as any;
}

// count 的實際值成為型別的一部分
const threeNumbers = createArray(42, 3);
//    ^? const threeNumbers: number[] & { length: 3 }

const fiveStrings = createArray("hello", 5);
//    ^? const fiveStrings: string[] & { length: 5 }

// 編譯期檢查長度！
type ExactLength<T, N> = T extends { length: N } ? T : never;

function processTriple(arr: ExactLength<typeof threeNumbers, 3>) {
    // 安全存取三個元素
    const [a, b, c] = arr;
    console.log(a, b, c);
}
```

### 型別層級運算

```typescript
// 型別層級的數值運算
type Add<A extends number, B extends number> = 
    A extends 0 ? B :
    A extends 1 ? [...BuildTuple<1>, ...BuildTuple<B>]['length'] :
    never;

type BuildTuple<N extends number, Acc extends any[] = []> = 
    Acc['length'] extends N ? Acc : BuildTuple<N, [...Acc, any]>;

type Three = Add<1, 2>;
//   ^? type Three = 3

type Five = Add<Three, 2>;
//   ^? type Five = 5

// 在實際程式碼中使用
function createMatrix<Rows extends number, Cols extends number>(
    rows: Rows, 
    cols: Cols,
    initial: number
): number[][][] & { shape: [Rows, Cols] } {
    return Array.from({ length: rows }, () =>
        Array.from({ length: cols }, () => initial)
    ) as any;
}

const matrix = createMatrix(3, 4, 0);
//    ^? const matrix: number[][][] & { shape: [3, 4] }
```

### 字串模板依賴型別

```typescript
// 字串模板的依賴型別
type HexDigit = '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'a'|'b'|'c'|'d'|'e'|'f';
type HexColor<N extends number> = 
    N extends 3 ? `#${HexDigit}${HexDigit}${HexDigit}` :
    N extends 6 ? `#${HexDigit}${HexDigit}${HexDigit}${HexDigit}${HexDigit}${HexDigit}` :
    never;

function parseColor<N extends 3 | 6>(hex: HexColor<N>): { r: number; g: number; b: number } {
    const normalized = hex.length === 4 
        ? `#${hex[1]}${hex[1]}${hex[2]}${hex[2]}${hex[3]}${hex[3]}`
        : hex;
    
    return {
        r: parseInt(normalized.slice(1, 3), 16),
        g: parseInt(normalized.slice(3, 5), 16),
        b: parseInt(normalized.slice(5, 7), 16),
    };
}

const color = parseColor("#ff8800");
//    ^? const color: { r: number; g: number; b: number }

// 編譯期錯誤！
// parseColor("#xyz");     // Error: Argument of type '"#xyz"' is not assignable
// parseColor("#ff8800cc"); // Error: Argument of length 9 is not assignable
```

## 編譯期巨集

TypeScript 6.0 引入了類似 Rust `macro_rules!` 的巨集系統：

### macro 定義

```typescript
// TypeScript 6.0：macro 定義
macro json_stringify {
    // 模式匹配：匹配物件字面量
    rule { { $($key: ident : $value: expr),* $(,)? } } => {
        JSON.stringify({ $($key: $value),* })
    }
    
    // 模式匹配：匹配陣列
    rule { [ $($elem: expr),* $(,)? ] } => {
        JSON.stringify([ $($elem),* ])
    }
}

// 使用巨集（編譯期展開）
const str1 = json_stringify!({ name: "Alice", age: 30 });
// 展開為：const str1 = JSON.stringify({ name: "Alice", age: 30 });

const str2 = json_stringify!([1, 2, 3, 4, 5]);
// 展開為：const str2 = JSON.stringify([1, 2, 3, 4, 5]);
```

### SQL 查詢巨集

```typescript
// 編譯期 SQL 驗證巨集
macro sql {
    // 匹配 SELECT 查詢並驗證語法
    rule { SELECT $columns FROM $table WHERE $condition } => {
        // 編譯期檢查 SQL 語法
        const _validated: true = compileTimeValidateSQL(
            "SELECT ${columns} FROM ${table} WHERE ${condition}"
        );
        `SELECT ${columns} FROM ${table} WHERE ${condition}`
    }
    
    // 匹配 INSERT
    rule { INSERT INTO $table ($($cols: ident),*) VALUES ($($vals: expr),*) } => {
        `INSERT INTO ${table} (${cols.join(', ')}) VALUES (${vals.map(v => '?').join(', ')})`
    }
}

// 使用巨集 — SQL 在編譯期被驗證
const query = sql! { SELECT id, name, email FROM users WHERE active = true };
// 如果 SQL 語法錯誤，編譯期報錯
```

### 測試巨集

```typescript
// 參數化測試巨集
macro parametrized_test {
    rule {
        $name: ident:
        cases = [ $($case: expr),+ $(,)? ];
        fn = $fn: expr;
    } => {
        describe(stringify!($name), () => {
            for (const [index, args] of [$($case),+].entries()) {
                it(`case ${index}`, () => {
                    $fn(...(Array.isArray(args) ? args : [args]));
                });
            }
        });
    }
}

// 使用
parametrized_test! {
    test_addition:
    cases = [
        [1, 2, 3],
        [0, 0, 0],
        [-1, 1, 0],
        [100, 200, 300],
    ];
    fn = (a: number, b: number, expected: number) => {
        expect(a + b).toBe(expected);
    };
}
```

## 型別模式匹配

### match 型別

TypeScript 6.0 引入了 `match` 型別運算子，類似 Rust 的模式匹配：

```typescript
// 型別層級的模式匹配
type ProcessValue<T> = match T {
    null => "null",
    undefined => "undefined",
    number => "number",
    string => "string",
    boolean => "boolean",
    Array<infer U> => `array<${U}>`,
    Promise<infer U> => `promise<${U}>`,
    _ => "unknown",
};

type R1 = ProcessValue<number>;
//   ^? type R1 = "number"
type R2 = ProcessValue<Array<string>>;
//   ^? type R2 = "array<string>"
type R3 = ProcessValue<Promise<number>>;
//   ^? type R3 = "promise<number>"
```

### 遞迴型別比對

```typescript
// JSON 型別的遞迴定義
type JSONValue = match {
    string => string,
    number => number,
    boolean => boolean,
    null => null,
    Array<infer U> => JSONArray<U>,
    { [key: string]: infer V } => JSONObject<V>,
};

type JSONArray<T> = T extends JSONValue ? T[] : never;
type JSONObject<T> = {
    [K in keyof T]: T[K] extends JSONValue ? T[K] : never;
};

// 編譯期驗證 JSON
const config = {
    host: "localhost",
    port: 8080,
    debug: true,
    features: ["auth", "logging"],
    nested: { key: "value" },
} satisfies JSONValue;  // 型別安全！
```

## 從 TypeScript 5.x 遷移到 6.0

### 自動遷移

```bash
# 升級 TypeScript
$ npm install typescript@6.0

# 執行遷移工具
$ npx tsc --migrate-to-60

# 檢查型別
$ npx tsc --strict --noEmit
```

### 主要破壞性變更

| 變更 | 說明 | 處理方式 |
|------|------|---------|
| `macro` 成為保留字 | 變數不可命名為 `macro` | 重新命名變數 |
| `match` 成為保留字 | 型別層級的 match 關鍵字 | 重新命名變數 |
| 泛型預設行為變更 | `T` 不再自動推導為 `unknown` | 明確標註 `T = unknown` |
| 依賴型別影響重載解析 | 部分重載簽章需要調整 | 使用 `--migrate-to-60` 自動修復 |
| 舊版裝飾器棄用 | 移除 Stage 1 裝飾器 | 遷移到 Stage 3 裝飾器 |

### 逐步遷移策略

```typescript
// 步驟 1：在 tsconfig.json 中啟用新特性
{
  "compilerOptions": {
    "target": "ES2026",
    "module": "ES2026",
    "strict": true,
    "experimentalDecorators": false,  // 舊裝飾器已棄用
    "dependentTypes": true,           // 啟用依賴型別
    "macros": true                    // 啟用巨集
  }
}

// 步驟 2：逐步引入依賴型別
// 從最簡單的開始
function identity<T, N extends number>(value: T, tag: N): T & { tag: N } {
    return Object.assign(value, { tag });
}

// 步驟 3：重構重複的型別模式為巨集
// 步驟 4：啟用型別模式匹配取代複雜的 conditional types
```

## 編譯器支援

| 編譯器/工具 | 依賴型別 | 巨集 | 型別匹配 |
|------------|---------|------|---------|
| tsc 6.0 | 完整支援 | 完整支援 | 完整支援 |
| ts-node | 完整支援 | 完整支援 | 完整支援 |
| esbuild | 部分支援 | 不支援 | 實驗性 |
| swc | 不支援 | 不支援 | 不支援 |
| Babel | 實驗性插件 | 不支援 | 不支援 |
| VS Code (1.95+) | 完整 LSP 支援 | 語法反白 | 完整 LSP 支援 |

## 結語

TypeScript 6.0 是型別系統的一次飛躍。依賴型別讓型別可以表達值的精確約束，編譯期巨集讓重複的模式可以被抽象化，型別模式匹配則讓複雜的條件型別變得可讀。對於大型 TypeScript 專案，升級到 6.0 能顯著提升型別安全性和開發效率。

---

**延伸閱讀**

- [TypeScript 6.0 發布公告](https://www.google.com/search?q=TypeScript+6.0+release+notes)
- [依賴型別提案](https://www.google.com/search?q=TypeScript+dependent+types+proposal)
- [TypeScript 巨集系統 RFC](https://www.google.com/search?q=TypeScript+compile+time+macros+RFC)
- [TS 6.0 遷移指南](https://www.google.com/search?q=TypeScript+6.0+migration+guide)
