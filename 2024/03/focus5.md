# 事件處理與表單驗證

## 事件處理基礎

事件是使用者與網頁互動的核心機制。點擊、鍵盤輸入、滑鼠移動、表單提交——這些都是事件。

### addEventListener

現代事件監聽的標準方式：

```javascript
const btn = document.querySelector("#myBtn");

btn.addEventListener("click", () => {
  console.log("按鈕被點擊了！");
});
```

可以同時綁定多個監聽器，移除時需要傳入相同的函式參考。

### removeEventListener

```javascript
function handleClick() {
  console.log("點擊");
}
btn.addEventListener("click", handleClick);
btn.removeEventListener("click", handleClick);
```

---

## 事件物件

事件處理器會收到一個事件物件，包含事件的詳細資訊：

```javascript
element.addEventListener("click", (event) => {
  console.log(event.type);       // "click"
  console.log(event.target);     // 觸發事件的元素
  console.log(event.currentTarget); // 綁定監聽器的元素
  console.log(event.clientX);    // 滑鼠 X 座標
  console.log(event.clientY);    // 滑鼠 Y 座標
});
```

### 常用事件物件屬性

| 屬性 | 說明 |
|------|------|
| type | 事件類型 |
| target | 實際觸發事件的元素 |
| currentTarget | 綁定監聽器的元素 |
| preventDefault() | 阻止瀏覽器預設行為 |
| stopPropagation() | 停止事件傳播 |

### 阻止預設行為

```javascript
form.addEventListener("submit", (e) => {
  e.preventDefault(); // 防止頁面重新整理
  // 處理表單資料
});
```

### 停止事件傳播

```javascript
child.addEventListener("click", (e) => {
  e.stopPropagation(); // 不讓事件冒泡到父元素
});
```

---

## 事件傳播機制

DOM 事件傳播分為三個階段：

1. **捕獲階段**：事件從 document 向下傳播到目標元素
2. **目標階段**：事件到達目標元素
3. **冒泡階段**：事件從目標元素向上傳播回 document

```javascript
// 在捕獲階段監聽
parent.addEventListener("click", handler, true);
// 在冒泡階段監聽（預設）
parent.addEventListener("click", handler, false);
```

---

## 事件委派

事件委派利用事件冒泡機制，在父層監聽子元素的事件：

```javascript
// 不推薦：為每個 li 綁定監聽器
document.querySelectorAll("li").forEach(li => {
  li.addEventListener("click", () => handleClick(li));
});

// 推薦：事件委派，只綁定一個監聽器
document.querySelector("ul").addEventListener("click", (e) => {
  const li = e.target.closest("li");
  if (li) handleClick(li);
});
```

---

## 表單驗證實作

### 基本驗證流程

```javascript
const form = document.querySelector("#register-form");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const errors = validate();
  if (errors.length > 0) {
    showErrors(errors);
  } else {
    submitForm();
  }
});

function validate() {
  const errors = [];
  const username = form.querySelector("#username").value.trim();
  const email = form.querySelector("#email").value.trim();
  const password = form.querySelector("#password").value;

  if (!username) errors.push("帳號為必填");
  if (username.length < 3) errors.push("帳號至少 3 個字元");
  if (!email) errors.push("Email 為必填");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.push("Email 格式不正確");
  }
  if (!password) errors.push("密碼為必填");
  if (password.length < 6) errors.push("密碼至少 6 個字元");

  return errors;
}
```

### 即時驗證

在輸入時提供即時回饋：

```javascript
const emailInput = document.querySelector("#email");

emailInput.addEventListener("blur", () => {
  validateField(emailInput);
});

emailInput.addEventListener("input", () => {
  if (emailInput.dataset.touched) {
    validateField(emailInput);
  }
});

function validateField(input) {
  input.dataset.touched = "true";
  const errorEl = input.nextElementSibling;
  const value = input.value.trim();

  if (input.required && !value) {
    showError(input, errorEl, "此欄位為必填");
  } else if (input.type === "email" && !isValidEmail(value)) {
    showError(input, errorEl, "Email 格式不正確");
  } else {
    clearError(input, errorEl);
  }
}
```

---

## 常見事件類型

### 滑鼠事件

| 事件 | 說明 |
|------|------|
| click | 點擊 |
| dblclick | 雙擊 |
| mouseenter | 滑鼠進入 |
| mouseleave | 滑鼠離開 |
| mousemove | 滑鼠移動 |

### 鍵盤事件

```javascript
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") submitForm();
  if (e.key === "Escape") closeModal();
});
```

### 表單事件

| 事件 | 說明 |
|------|------|
| submit | 表單提交 |
| reset | 表單重置 |
| change | 值改變 |
| input | 即時輸入 |
| focus | 獲得焦點 |
| blur | 失去焦點 |

---

## 延伸閱讀

- [MDN: 事件參考](https://www.google.com/search?q=MDN+Event+reference)
- [JavaScript 事件處理](https://www.google.com/search?q=JavaScript+event+handling)
- [表單驗證最佳實踐](https://www.google.com/search?q=form+validation+best+practices)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列之一。*
