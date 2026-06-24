# npm 3.0 展望

## 前言

npm 3.0 預計帶來更智慧的依賴管理和更快的安裝速度。

## 主要改進

### 扁平化依賴樹

```bash
# npm 2.x
node_modules/
  └─ express/
      └─ node_modules/
          └─ accepts/

# npm 3.x
node_modules/
  ├─ express/
  └─ accepts/
```

### 平行安裝

```bash
# npm 3.0 支援平行下載
npm install --parallel
```

### 離線支援

```bash
npm install --offline  # 使用本地快取
```

---

## 延伸閱讀

- [npm 3.0 開發進展](https://www.google.com/search?q=npm+3.0+development+2015)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」文章之一。*