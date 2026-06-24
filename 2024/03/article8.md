# 表單驗證實戰

## 為什麼需要表單驗證

表單驗證確保使用者提交的資料符合預期格式和規則。驗證分為兩個層次：

- **前端驗證**：即時回饋使用者，提升使用體驗
- **後端驗證**：確保資料安全，防止惡意輸入

前端驗證不能替代後端驗證，但可以大幅提升使用者體驗。

---

## HTML5 內建驗證

### HTML5 驗證屬性

HTML5 提供了多種驗證屬性，無需 JavaScript：

```html
<form id="register">
  <input type="text" name="username" required minlength="3" maxlength="20"
         pattern="[A-Za-z0-9]+" title="只能包含英數字">
  <input type="email" name="email" required>
  <input type="password" name="password" required minlength="6">
  <input type="number" name="age" min="18" max="120">
  <input type="url" name="website">
  <button type="submit">註冊</button>
</form>
```

### 驗證樣式

使用 CSS 偽類控制驗證狀態樣式：

```css
input:valid {
  border-color: #28a745;
}
input:invalid {
  border-color: #dc3545;
}
input:focus:invalid {
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.25);
}
```

---

## JavaScript 自訂驗證

### 驗證引擎

建立一個可重用的驗證引擎：

```javascript
class FormValidator {
  constructor(form, rules) {
    this.form = form;
    this.rules = rules;
    this.errors = new Map();
    this.form.addEventListener("submit", (e) => this.handleSubmit(e));
    this.bindInputEvents();
  }

  bindInputEvents() {
    this.rules.forEach((fieldRules, fieldName) => {
      const input = this.form.querySelector(`[name="${fieldName}"]`);
      if (!input) return;

      input.addEventListener("blur", () => {
        this.validateField(fieldName);
      });
      input.addEventListener("input", () => {
        if (this.errors.has(fieldName)) {
          this.validateField(fieldName);
        }
      });
    });
  }

  validateField(fieldName) {
    const input = this.form.querySelector(`[name="${fieldName}"]`);
    if (!input) return true;

    const fieldRules = this.rules.get(fieldName);
    const value = input.value.trim();
    const errorEl = this.form.querySelector(`#${fieldName}-error`);
    let isValid = true;

    for (const rule of fieldRules) {
      const error = rule.validate(value, input);
      if (error) {
        this.errors.set(fieldName, error);
        input.classList.add("is-invalid");
        if (errorEl) errorEl.textContent = error;
        isValid = false;
        break;
      }
    }

    if (isValid) {
      this.errors.delete(fieldName);
      input.classList.remove("is-invalid");
      if (errorEl) errorEl.textContent = "";
    }
    return isValid;
  }

  handleSubmit(e) {
    e.preventDefault();
    let isValid = true;

    this.rules.forEach((_, fieldName) => {
      if (!this.validateField(fieldName)) isValid = false;
    });

    if (isValid) {
      this.onSuccess(new FormData(this.form));
    }
  }

  onSuccess(data) {
    console.log("表單驗證通過，提交資料...");
    // 實際提交
  }
}
```

### 驗證規則

```javascript
const rules = new Map([
  ["username", [
    { validate: (v) => !v && "帳號為必填" },
    { validate: (v) => v && v.length < 3 && "帳號至少 3 個字元" },
    { validate: (v) => v && !/^[A-Za-z0-9]+$/.test(v) && "只能使用英數字" },
  ]],
  ["email", [
    { validate: (v) => !v && "Email 為必填" },
    { validate: (v) => v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) && "Email 格式不正確" },
  ]],
  ["password", [
    { validate: (v) => !v && "密碼為必填" },
    { validate: (v) => v && v.length < 6 && "密碼至少 6 個字元" },
    { validate: (v) => v && !/[A-Z]/.test(v) && "密碼需包含大寫字母" },
    { validate: (v) => v && !/\d/.test(v) && "密碼需包含數字" },
  ]],
  ["confirmPassword", [
    { validate: (v) => !v && "請確認密碼" },
    { validate: (v, input) => {
      const pw = input.form.querySelector("[name='password']").value;
      return v !== pw && "密碼不一致";
    }},
  ]],
]);

const validator = new FormValidator(
  document.querySelector("#register"),
  rules
);
```

---

## 即時回饋 UI

### 錯誤訊息顯示

```html
<div class="form-group">
  <label for="email">Email</label>
  <input type="email" name="email" id="email" required>
  <div id="email-error" class="error-message" role="alert"></div>
</div>
```

### 成功與錯誤樣式

```css
.form-group { margin-bottom: 1rem; }
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-group input.is-invalid {
  border-color: #dc3545;
}
.form-group input.is-valid {
  border-color: #28a745;
}
.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  min-height: 1.25rem;
}
```

---

## 完整表單驗證流程

```
使用者輸入
    │
    ▼
即時驗證（input / blur 事件）
    │
    ├── 通過 → 清除錯誤訊息，標記為有效
    └── 失敗 → 顯示錯誤訊息，標記為無效
    │
    ▼
提交表單
    │
    ▼
完整驗證（所有欄位）
    │
    ├── 全部通過 → 提交資料
    └── 有錯誤 → 聚焦第一個錯誤欄位，顯示所有錯誤
```

---

## 延伸閱讀

- [MDN: 表單驗證](https://www.google.com/search?q=MDN+form+validation)
- [HTML5 表單驗證指南](https://www.google.com/search?q=HTML5+form+validation+guide)
- [Constraint Validation API](https://www.google.com/search?q=JavaScript+constraint+validation+API)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」精選文章之一。*
