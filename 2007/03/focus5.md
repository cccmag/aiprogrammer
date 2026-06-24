# .NET 與 C# 的發展

## 前言

微軟的 .NET 平台在 2007 年持續創新，C# 3.0 正在開發中。

## C# 3.0 的創新

```csharp
// C# 3.0 新特性
// Lambda 運算式
var numbers = new[] { 1, 2, 3, 4, 5 };
var evens = numbers.Where(n => n % 2 == 0);

// LINQ 查詢
var result = from n in numbers
             where n > 2
             select n * 2;

// 匿名型別
var person = new { Name = "John", Age = 30 };
```

## LINQ 的意義

LINQ 將查詢能力整合進語言，改變了資料處理的方式。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」本期焦點系列文章。*