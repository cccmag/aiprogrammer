# npm 2.0 登場：更好的依賴管理

## 前言

npm 2.0 帶來了更智慧的依賴管理機制，解決了長期困擾開發者的「依賴地獄」問題。

## 扁平化依賴樹

```bash
# npm 1.x：嵌套的 node_modules
node_modules/
  └── express/
      └── node_modules/
          └── accepts/

# npm 2.x：扁平化
node_modules/
  ├── express/
  └── accepts/
```

## 新功能

```bash
# 安裝可選依賴
npm install --save-optional package-name

# 安裝開發依賴
npm install --save-dev testing-library

# 查看依賴樹
npm ls

# 查看過時套件
npm outdated
```

## package.json 版本語法

```json
{
  "dependencies": {
    "express": "^4.13.0",     // ^：相容版本
    "lodash": "~4.0.0",       // ~：修補版本
    "ansi": "2.0.0",          // 精確版本
    "optimist": ">=0.6.0"    // 最小版本
  }
}
```

---

## 延伸閱讀

- [npm 2.0 發布說明](https://www.google.com/search?q=npm+2.0+released+2015)
- [npm 依賴管理詳解](https://www.google.com/search?q=npm+dependencies+management)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*