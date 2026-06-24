#!/usr/bin/env node
"use strict";

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
  getAttribute(name) { return this.attrs[name]; }
  setAttribute(name, val) { this.attrs[name] = val; }
  get innerText() {
    return this.children.map(c => typeof c === "string" ? c : c.innerText).join("");
  }
  set innerText(t) { this.children = [t]; }
  get outerHTML() {
    let a = Object.entries(this.attrs).map(([k, v]) => ` ${k}="${v}"`).join("");
    if (["br", "input", "img"].includes(this.tag)) return `<${this.tag}${a}>`;
    return `<${this.tag}${a}>${this.children.map(c => typeof c === "string" ? c : c.outerHTML).join("")}</${this.tag}>`;
  }
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

const validators = {
  required(v) { return v != null && v !== ""; },
  email(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); },
  minlen(v, n) { return typeof v === "string" && v.length >= n; },
  maxlen(v, n) { return typeof v === "string" && v.length <= n; },
  numeric(v) { return !isNaN(parseFloat(v)) && isFinite(v); },
  pattern(v, re) { return re.test(v); }
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

function demo() {
  const root = new VNode("div", { id: "app" });
  const h1 = new VNode("h1", { class: "title" }, ["前端開發實戰"]);
  const form = new VNode("form", { id: "login" });
  form.appendChild(new VNode("input", { type: "text", name: "username", placeholder: "帳號" }));
  form.appendChild(new VNode("input", { type: "email", name: "email", placeholder: "Email" }));
  form.appendChild(new VNode("button", { type: "submit" }, ["登入"]));
  root.appendChild(h1);
  root.appendChild(form);

  console.log("=== Virtual DOM Tree ===");
  console.log(root.outerHTML);

  console.log("\n=== Query Selector Demo ===");
  console.log("querySelector('#login'):", root.querySelector("#login").tag);
  console.log("querySelectorAll('input'):", root.querySelectorAll("input").length);

  const css = `
    .title { color: #333; font-size: 24px; }
    #login { margin: 20px; padding: 10px; }
    input { border: 1px solid #ccc; }
  `;
  const rules = parseCSS(css);
  console.log("\n=== CSS Parse Demo ===");
  console.log("Parsed rules:", rules.length);
  const style = computeStyle(root.querySelector("h1"), rules);
  console.log("Computed style for h1:", JSON.stringify(style));

  console.log("\n=== Form Validation Demo ===");
  const fields = [
    { name: "username", value: "", rules: [{ type: "required", message: "帳號為必填" }] },
    { name: "email", value: "bad-email", rules: [{ type: "required", message: "Email 為必填" }, { type: "email", message: "Email 格式不正確" }] }
  ];
  const errs = validateForm(fields);
  console.log("Validation errors:", errs.length);
  errs.forEach(e => console.log(`  ${e.field}: ${e.message}`));

  console.log("\n=== All Demos Passed ===");
}

if (require.main === module) demo();
