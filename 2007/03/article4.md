# C# 3.0 的 LINQ 革新

## 前言

LINQ 將查詢能力整合進 C#，改變了資料處理的方式。

## LINQ 範例

```csharp
// 查詢語法
var result = from n in numbers
             where n > 0
             orderby n
             select n * 2;

// 方法語法
var result = numbers
    .Where(n => n > 0)
    .OrderBy(n => n)
    .Select(n => n * 2);
```

## 結論

LINQ 展示了大陸整合查詢語言的潛力。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」文章集錦系列。*