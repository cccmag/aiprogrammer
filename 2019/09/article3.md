# TypeScript 3.7：可選鏈與空位合併運算子

## 前言

TypeScript 3.7 進入了最終候選階段，即將正式發布。這個版本帶來了兩個重要的新語法：可選鏈和空位合併運算子。

## 可選鏈

### 操作符

```typescript
// 之前的寫法
const street = user && user.address && user.address.street;

// 使用可選鏈
const street = user?.address?.street;
```

---

## 空位合併運算子

### 操作符

```typescript
// 之前
const name = user.nickname || user.name;

// 使用空位合併
const name = user.nickname ?? user.name;
```

---

## 結語

TypeScript 3.7 的新語法借鑒了其他語言的成功經驗，讓空值處理更加簡潔優雅。

---

**延伸閱讀**

- [TypeScript 3.7](https://www.google.com/search?q=TypeScript+3.7+release+notes)