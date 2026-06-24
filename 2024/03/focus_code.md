# 前端開發完整實作

## 前言

前端開發涉及 HTML 結構、CSS 樣式與 JavaScript 互動邏輯。本篇文章將透過一個自製的虛擬 DOM 實作，完整示範 DOM 操作、CSS 解析與表單驗證三大核心功能。所有程式碼皆可在 Node.js 環境中執行，無需瀏覽器。

---

## 原始碼

完整的 JavaScript 實作請參考：[_code/frontend_demo.js](_code/frontend_demo.js)

```javascript
class VNode {
  constructor(tag, attrs, children) {
    this.tag = tag;
    this.attrs = attrs || {};
    this.children = children || [];
    this.parent = null;
  }
  appendChild(child) {
    child.parent = this;
    this.children.push(child);
  }
  querySelector(sel) {
    if (matchSelector(this, sel)) return this;
    for (const c of this.children) {
      if (c instanceof VNode) {
        const r = c.querySelector(sel);
        if (r) return r;
      }
    }
    return null;
  }
  querySelectorAll(sel, acc) {
    acc = acc || [];
    if (matchSelector(this, sel)) acc.push(this);
    for (const c of this.children) {
      if (c instanceof VNode) c.querySelectorAll(sel, acc);
    }
    return acc;
  }
  // ... 其他方法
}

function matchSelector(el, sel) {
  if (sel === "*") return true;
  if (sel.startsWith("#")) return el.attrs.id === sel.slice(1);
  if (sel.startsWith(".")) return (el.attrs.class || "").split(/\s+/).includes(sel.slice(1));
  let tag = sel, id, cls;
  let m = sel.match(/^(\w+)?(?:#(\w+))?(?:\.(\w+))?/);
  if (m) { tag = m[1] || el.tag; id = m[2]; cls = m[3]; }
  if (el.tag !== tag) return false;
  if (id && el.attrs.id !== id) return false;
  if (cls && !(el.attrs.class || "").split(/\s+/).includes(cls)) return false;
  return true;
}
```

### CSS 解析引擎

```javascript
function parseCSS(cssText) {
  const rules = [];
  const blockRe = /([^{]+)\{([^}]+)\}/g;
  let m;
  while ((m = blockRe.exec(cssText)) !== null) {
    const selector = m[1].trim();
    const decls = {};
    m[2].split(";").filter(Boolean).forEach(d => {
      const [prop, val] = d.split(":").map(s => s.trim());
      if (prop && val) decls[prop] = val;
    });
    rules.push({ selector, decls });
  }
  return rules;
}

function computeStyle(el, rules) {
  const style = {};
  for (const r of rules) {
    if (matchSelector(el, r.selector)) Object.assign(style, r.decls);
  }
  return style;
}
```

### 表單驗證系統

```javascript
const validators = {
  required(v) { return v != null && v !== ""; },
  email(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); },
  minlen(v, n) { return typeof v === "string" && v.length >= n; },
  maxlen(v, n) { return typeof v === "string" && v.length <= n; },
};

function validateForm(fields) {
  const errors = [];
  for (const f of fields) {
    for (const rule of f.rules) {
      const fn = validators[rule.type];
      if (!fn) continue;
      const valid = rule.param !== undefined ? fn(f.value, rule.param) : fn(f.value);
      if (!valid) errors.push({ field: f.name, message: rule.message });
    }
  }
  return errors;
}
```

---

## 執行結果

```
=== Virtual DOM Tree ===
<div id="app"><h1 class="title">前端開發實戰</h1><form id="login"><input type="text" name="username" placeholder="帳號"><input type="email" name="email" placeholder="Email"><button type="submit">登入</button></form></div>

=== Query Selector Demo ===
querySelector('#login'): form
querySelectorAll('input'): 2

=== CSS Parse Demo ===
Parsed rules: 3
Computed style for h1: {"color":"#333","font-size":"24px"}

=== Form Validation Demo ===
Validation errors: 2
  username: 帳號為必填
  email: Email 格式不正確

=== All Demos Passed ===
```

---

## 實作說明

### VNode 虛擬節點

VNode 類別模擬了瀏覽器的 DOM 節點。每個節點包含 tag（標籤名）、attrs（屬性）、children（子節點）和 parent（父節點）。支援 appendChild、querySelector、querySelectorAll、getAttribute 等標準 DOM 方法。

### CSS 選擇器比對

matchSelector 函式實作了基本的 CSS 選擇器比對，支援標籤選擇器（div）、ID 選擇器（#app）、類別選擇器（.title）以及複合選擇器（h1.title）。parseCSS 將 CSS 文字解析為規則列表，computeStyle 根據規則計算元素的樣式。

### 表單驗證

驗證系統支援 required、email、minlen、maxlen 等規則。validateForm 接收欄位定義陣列，返回錯誤列表。每個欄位可關聯多個驗證規則，實現彈性的表單驗證組合。

---

## 延伸閱讀

- [MDN Web Docs: DOM](https://www.google.com/search?q=MDN+DOM+JavaScript)
- [CSS Selectors 參考](https://www.google.com/search?q=CSS+selectors+reference)
- [JavaScript 表單驗證](https://www.google.com/search?q=JavaScript+form+validation)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列補充文章。*
