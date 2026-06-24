# TypeScript 3.6：更嚴格的生成器與迭代器

## 前言

TypeScript 3.6 於 2019 年 8 月正式發布。這個版本專注於提升生成器（Generator）和迭代器（Iterator）的型別安全性和精確度。本文將詳細解析這些改進。

## 生成器型別的改進

### 問題背景

在 TypeScript 3.5 及之前，生成器的型別處理不夠精確：

```typescript
// 舊版 TypeScript 的推斷
function* gen() {
    yield 1;
    yield 2;
    yield 3;
}

// TypeScript 3.5 的推斷
// const g: Generator<number, void, unknown>
```

### TypeScript 3.6 的改進

```typescript
// TypeScript 3.6 的更精確推斷
function* gen() {
    yield 1;
    yield 2;
    yield 3;
}

// 推斷結果：
// {
//     next(): IteratorResult<number>;
//     return(): IteratorResult<number>;
//     throw(e: unknown): IteratorResult<number>;
//     [Symbol.iterator](): IteratorResult<number>;
// }
```

### 迭代結果型別

```typescript
// 精確的 IteratorResult 型別
function* numbers(): Generator<number> {
    yield 1;
    yield 2;
    yield 3;
}

const iter = numbers();

// next() 返回精確的型別
const result1 = iter.next();
// result1: { value: number | undefined, done: boolean }

if (!result1.done) {
    console.log(result1.value);  // number（正確推斷）
}
```

---

## 迭代器協議

### AsyncIterator 和 AsyncGenerator

TypeScript 3.6 新增了對非同步迭代的完整支援：

```typescript
// 非同步生成器
async function* asyncGen(): AsyncGenerator<number> {
    for (let i = 0; i < 5; i++) {
        await new Promise(resolve => setTimeout(resolve, 100));
        yield i;
    }
}

// 使用 for-await-of
async function main() {
    for await (const value of asyncGen()) {
        console.log(value);
    }
}
```

### 符號類型改進

```typescript
// 更好的 Symbol 推斷
const sym = Symbol("description");
type SymbolType = typeof sym;
// type SymbolType = unique symbol

// Symbol.iterator 的型別
interface Iterable<T> {
    [Symbol.iterator](): Iterator<T>;
}

interface AsyncIterable<T> {
    [Symbol.asyncIterator](): AsyncIterator<T>;
}
```

---

## 更嚴格的型別檢查

### 生成器拋出錯誤的型別

```typescript
function* genWithThrow(): Generator<number, void, never> {
    try {
        yield 1;
    } finally {
        // throw now allowed here
        throw new Error("error");
    }
}

// next() 的型別現在是精確的
const g = genWithThrow();
const result = g.next();
// result: { value: number | undefined, done: boolean }
```

### 迭代器的 return 和 throw 方法

```typescript
interface Iterator<T, TReturn = unknown, TNext = unknown> {
    next(...args: [] | [TNext]): IteratorResult<T, TReturn>;
    return?(value?: TReturn): IteratorResult<T, TReturn>;
    throw?(e?: unknown): IteratorResult<T, TReturn>;
}
```

---

## 實際應用

### 自訂迭代器類別

```typescript
class RangeIterator implements Iterator<number> {
    private current: number;
    private readonly end: number;

    constructor(start: number, end: number) {
        this.current = start;
        this.end = end;
    }

    next(): IteratorResult<number> {
        if (this.current < this.end) {
            return { value: this.current++, done: false };
        }
        return { value: undefined, done: true };
    }
}

function range(start: number, end: number): IterableIterator<number> {
    return new RangeIterator(start, end);
}

for (const num of range(1, 5)) {
    console.log(num);  // 1, 2, 3, 4
}
```

### 產生器推導

```typescript
// TypeScript 3.6 現在可以正確推斷
function* foo() {
    yield* [1, 2, 3];
}

// 推斷結果
const iter = foo();
// iter: Generator<number, void, unknown>
```

---

## 其他改進

### 1. 建構函式參數屬性

```typescript
class Person {
    constructor(
        public readonly name: string,
        private age: number
    ) {}
}

const p = new Person("Alice", 30);
console.log(p.name);  // "Alice"
```

### 2. 更好的 JSDoc 支援

```typescript
/**
 * @param {string} name - 名字
 * @returns {number} 年齡
 */
function getAge(name: string): number {
    // ...
}
```

---

## 遷移指南

### 向後相容性

TypeScript 3.6 完全向後相容。大多數變更是漸進的，不會破壞現有代碼。

### 建議

1. 升級 TypeScript：`npm install -D typescript@3.6`
2. 運行現有測試確保沒有回歸
3. 利用新的嚴格檢查發現潜在問題

---

## 結語

TypeScript 3.6 的迭代器改進使得框架和庫的型別定義更加精確。雖然這些改變比較底層，但對於需要處理生成器和迭代器的開發者來說，是重要的進步。

---

**延伸閱讀**

- [TypeScript 3.6 Release Notes](https://www.google.com/search?q=TypeScript+3.6+release+notes)
- [Iterators and Generators in TypeScript](https://www.google.com/search?q=TypeScript+iterators+generators)
- [TypeScript Async Iterators](https://www.google.com/search?q=TypeScript+async+iterators)