# console.log 與除錯技巧

## console.log 的各種用法

### 基本輸出

```javascript
// 基本輸出
console.log('Hello World');

// 多個參數
console.log('數字:', 42, '字串:', 'hello');

// 格式化輸出
console.log('名稱: %s, 年齡: %d', 'Alice', 30);
console.log('百分比: %d%%', 75);
```

### 格式化輸出樣式

```javascript
// 使用樣式
console.log(
  '%c紅色大字',
  'color: red; font-size: 24px; font-weight: bold'
);

console.log(
  '%c標題 %c內容',
  'color: blue; font-size: 20px;',
  'color: green; font-size: 14px;'
);
```

### 特殊方法

```javascript
const data = { name: 'Alice', age: 30 };
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];

// 表格輸出（適合陣列）
console.table(users);

// 物件展開
console.dir(data, { depth: null, colors: true });

// 分組輸出
console.group('使用者資訊');
console.log('姓名:', 'Alice');
console.log('年齡:', 30);
console.groupEnd();

// 計數
console.count('點擊'); // 點擊: 1
console.count('點擊'); // 點擊: 2
console.countReset('點擊');

// 計時
console.time('資料處理');
// 執行耗時操作
console.timeEnd('資料處理'); // 資料處理: 12.345ms

// 追蹤呼叫堆疊
function func1() { func2(); }
function func2() { console.trace('呼叫追蹤'); }
func1();

// 警告與錯誤
console.warn('這是一個警告');
console.error('這是一個錯誤');
console.assert(1 === 2, '條件不成立'); // 僅在條件為 false 時輸出
```

## 瀏覽器除錯

### 中斷點除錯

在瀏覽器中，按 F12 開啟開發者工具 → Sources 分頁：

1. 在程式碼行號處點擊設定中斷點
2. 重新載入頁面觸發中斷
3. 使用右側面板檢查變數值

**常用功能鍵：**
- **F10**：逐步執行（跳過函數）
- **F11**：逐步進入（進入函數）
- **Shift+F11**：跳出函數
- **F8**：繼續執行

### Watch 與 Scope

在 Sources 面板中：
- **Watch**：監控特定表達式的值
- **Scope**：查看當前作用域的所有變數
- **Call Stack**：查看函數呼叫鏈
- **Breakpoints**：管理所有中斷點

### Conditional Breakpoints

右鍵點擊行號，選擇「Add Conditional Breakpoint」：

```javascript
// 只在特定條件下中斷
for (let i = 0; i < 100; i++) {
  // 當 i 等於 50 時中斷
  process(i);
}
```

## Node.js 除錯

### 內建除錯器

```bash
# 啟動除錯器
node inspect script.js

# 常用命令
# n: next（下一步）
# s: step in（進入函數）
# o: step out（跳出函數）
# c: continue（繼續執行）
# repl: 進入互動式模式
# watch('變數名'): 監控變數
# .exit: 離開除錯器
```

### VS Code 除錯

在 VS Code 中按 F5 啟動除錯。設定中斷點後：

```javascript
// 編寫測試用的程式碼
function calculateTotal(items) {
  // 在此處設定中斷點
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total;
}

const cart = [
  { price: 100, quantity: 2 },
  { price: 50, quantity: 3 }
];

const result = calculateTotal(cart);
console.log('總計:', result);
```

### Node Inspector

```bash
# 啟動遠端除錯
node --inspect-brk script.js

# 在瀏覽器中打開 chrome://inspect
# 點擊 Remote Target 下的 inspect 連結
```

## 實用除錯技巧

### Log Points

無需修改程式碼即可輸出日誌：

```javascript
// VS Code 中：右鍵行號 → Add Log Point
// 輸入要輸出的表達式，如：`i = ${i}`
for (let i = 0; i < 5; i++) {
  // 不修改程式碼，但會自動輸出 i 的值
}
```

### 黑盒子腳本

在 Sources 面板中，右鍵選擇「Blackbox Script」跳過第三方庫的除錯，聚焦在自己的程式碼。

## 結語

除錯是程式設計中最重要的技能之一。從簡單的 console.log 到瀏覽器中斷點除錯，再到 VS Code 的整合除錯環境，掌握這些工具能讓你快速定位問題。

---

**延伸閱讀**

- [Chrome DevTools 除錯](https://www.google.com/search?q=Chrome+DevTools+debugging)
- [Node.js 除錯指南](https://www.google.com/search?q=Node.js+debugging+guide)
- [VS Code 除錯](https://www.google.com/search?q=VS+Code+debugging+JavaScript)
