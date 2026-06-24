# TypeScript 2.0 登場：非空類型與更好的推斷

## 前言

2017 年 9 月，微軟發布了 TypeScript 2.0，這是 TypeScript 語言發展史上最重要的版本之一。這個版本引入了多項革命性的特性，大幅提升了型別系統的表達能力和安全性。

## 非空類型 (Non-Nullable Types)

TypeScript 2.0 最重要的新特性是對 null 和 undefined 的更好處理。

### 嚴格的空值檢查

```typescript
// TypeScript 2.0 之前
function greet(name: string) {
    // name 可能是 null 或 undefined
    console.log("Hello, " + name.toUpperCase()); // 危險！
}

// TypeScript 2.0 以後
function greet(name: string) {
    // 現在 name 明確是 string，不是 null/undefined
    console.log("Hello, " + name.toUpperCase());
}
```

### --strictNullChecks 選項

```bash
# 啟用嚴格空值檢查
tsc --strictNullChecks
```

```typescript
// 啟用 strictNullChecks 後
let name: string = null;  // 錯誤：不能將 null 賦值給 string
let name: string | null = null;  // 正確：明確標記可能為 null

function greet(name: string | null) {
    if (name !== null) {
        console.log("Hello, " + name.toUpperCase());  // 現在安全了
    }
}
```

### 可選鏈 (Optional Chaining)

```typescript
// 處理可能不存在的屬性
interface User {
    address?: {
        street?: string;
        city?: string;
    };
}

function getStreet(user: User): string | undefined {
    return user?.address?.street;
}
```

## 更好的類型推斷

### 乾燥類型 (Discriminated Unions)

```typescript
interface Square {
    kind: "square";
    size: number;
}

interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}

interface Circle {
    kind: "circle";
    radius: number;
}

type Shape = Square | Rectangle | Circle;

function area(shape: Shape): number {
    switch (shape.kind) {
        case "square":
            return shape.size ** 2;
        case "rectangle":
            return shape.width * shape.height;
        case "circle":
            return Math.PI * shape.radius ** 2;
    }
}
```

### 衛士類型 (Type Guards)

```typescript
function isRectangle(shape: Shape): shape is Rectangle {
    return shape.kind === "rectangle";
}

function processShape(shape: Shape) {
    if (isRectangle(shape)) {
        // TypeScript 知道這是 Rectangle
        console.log(shape.width, shape.height);
    }
}
```

## 控制流分析

TypeScript 2.0 增強了控制流分析，可以更準確地推斷變數類型：

```typescript
let value: string | number | boolean;

value = "hello";
console.log(value.toUpperCase());  // value 是 string

value = 42;
console.log(value.toFixed(2));  // value 是 number

value = true;
console.log(value ? "yes" : "no");  // value 是 boolean
```

## 索引類型 (Index Types)

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

interface User {
    name: string;
    age: number;
}

const user: User = { name: "John", age: 30 };

const name = getProperty(user, "name");  // string
const age = getProperty(user, "age");    // number
// getProperty(user, "email");  // 錯誤：不在 keyof User 中
```

## 映射類型

```typescript
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

type Partial<T> = {
    [P in keyof T]?: T[P];
};

type OptionalUser = Partial<User>;
type FrozenUser = Readonly<User>;
```

## 實用程式類型 (Utility Types)

TypeScript 2.1 引入了多個實用程式類型：

```typescript
interface User {
    id: number;
    name: string;
    email: string;
}

// Partial - 所有屬性可選
type UpdateUser = Partial<User>;

// Required - 所有屬性必填
type CompleteUser = Required<User>;

// Pick - 選擇部分屬性
type UserPreview = Pick<User, "id" | "name">;

// Omit - 排除部分屬性
type UserUpdate = Omit<User, "id">;

// Record - 建立特定鍵類型的物件
type UserRoles = Record<string, string>;
```

## 對大型專案的影響

```typescript
// 在 Angular、Vue、React 等框架中的應用

// Angular 中的使用
@Component({
    selector: 'app-user',
    template: '<div>{{ user.name }}</div>'
})
class UserComponent {
    @Input() user: User;  // 完整的類型安全保障
}

// React 中的使用
interface Props {
    users: User[];
    onSelect: (user: User) => void;
}

function UserList({ users, onSelect }: Props) {
    return (
        <ul>
            {users.map(user => (
                <li onClick={() => onSelect(user)}>
                    {user.name}
                </li>
            ))}
        </ul>
    );
}
```

## 遷移指南

### 逐步啟用 strictNullChecks

```json
// tsconfig.json
{
    "compilerOptions": {
        "strictNullChecks": true,
        "noImplicitAny": true,
        "strictFunctionTypes": true
    }
}
```

### 常見錯誤修復

```typescript
// 錯誤 1：null 值處理
// 之前
function getLength(s: string | null) {
    return s.length;  // 可能錯誤
}

// 之後
function getLength(s: string | null) {
    if (s === null) return 0;
    return s.length;
}

// 錯誤 2：Promise 返回值
// 之前
async function fetchData(): Promise<any> {
    return fetch("/api/data").then(r => r.json());
}

// 之後
async function fetchData(): Promise<Data> {
    return fetch("/api/data").then(r => r.json());
}
```

## 結論

TypeScript 2.0 的發布標誌著 TypeScript 成為一個成熟的工業級語言。非空類型、控制流分析和更好的推斷，使得大型專案的開發更加安全高效。對於深度學習和 AI 應用的前端開發，TypeScript 提供了更好的開發體驗和安全保障。

---

**延伸閱讀**

- [TypeScript 2.0 Release Notes](https://www.google.com/search?q=TypeScript+2.0+release+notes)
- [TypeScript strictNullChecks Guide](https://www.google.com/search?q=TypeScript+strictNullChecks)
- [Advanced TypeScript Types](https://www.google.com/search?q=Advanced+TypeScript+types+tutorial)