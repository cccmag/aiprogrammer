# C# 3.0 與 LINQ：查詢語言的革新

## 前言

2007 年 11 月，微軟發布了 .NET Framework 3.5 和 C# 3.0，其中最引人注目的創新是 Language Integrated Query（LINQ）—— 一種將查詢能力直接整合到程式語言中的革命性功能。

## LINQ 的誕生背景

### 2007 年的資料存取問題

當時的開發者面對多樣化的資料來源：

```
┌────────────────────────────────────────────────────────┐
│           2007 年資料存取的挑戰                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  關聯式資料庫：                                        │
│  - SQL Server, MySQL, Oracle                         │
│  - 需要撰寫 SQL 查詢                                   │
│                                                        │
│  物件導向世界：                                        │
│  - 記憶體中的集合                                      │
│  - 需要 LINQ 之前的迭代處理                            │
│                                                        │
│  XML 文件：                                            │
│  - XPath, XQuery                                     │
│  - 與 SQL 完全不同的語法                               │
│                                                        │
│  問題：                                                │
│  - 開發者需要學習多種查詢語言                          │
│  - 缺乏型別安全                                        │
│  - 難以重構                                            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## C# 3.0 的新特性

### 1. Lambda 運算式

```csharp
// 匿名方法的簡化語法
// C# 2.0
list.FindAll(delegate(int x) { return x > 0; });

// C# 3.0 Lambda
list.FindAll(x => x > 0);

// 更多範例
list.Select(x => x.Name)
list.Where(x => x.Age > 18)
    .OrderBy(x => x.Name)
    .Take(10);
```

### 2. 型別推斷

```csharp
// var 關鍵字
var name = "John";        // 推斷為 string
var age = 25;             // 推斷為 int
var items = new List<int>(); // 推斷為 List<int>

// 無需明確標註型別
var query = from p in products
            where p.Price > 100
            select p;
```

### 3. 物件初始化運算式

```csharp
// 傳統方式
var person = new Person();
person.Name = "John";
person.Age = 30;

// C# 3.0 物件初始化
var person = new Person { Name = "John", Age = 30 };

// 含建構式的初始化
var person = new Person("John") { Age = 30 };
```

### 4. 匿名型別

```csharp
// 根據初始化運算式推斷型別
var person = new {
    Name = "John",
    Age = 30,
    City = "Taipei"
};

// 非常適合用於 LINQ 投影
var results = from p in products
              select new {
                  p.Name,
                  p.Price,
                  DiscountedPrice = p.Price * 0.9
              };
```

### 5. 擴充方法

```csharp
// 為現有型別新增方法
public static class StringExtensions
{
    public static bool IsEmail(this string str)
    {
        return str.Contains("@");
    }
}

// 使用擴充方法
string email = "test@example.com";
if (email.IsEmail()) { /* ... */ }
```

## LINQ 語法

### Query Syntax vs Method Syntax

```csharp
// Query Syntax（查詢語法）
var query = from p in products
            where p.Category == "Electronics"
            orderby p.Price descending
            select p.Name;

// Method Syntax（方法語法）
var query = products
    .Where(p => p.Category == "Electronics")
    .OrderByDescending(p => p.Price)
    .Select(p => p.Name);

// 兩者可以混合使用
var results = (from p in products
               where p.Price > 100
               select p)
              .Take(10);
```

### 完整範例

```csharp
using System.Linq;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Category { get; set; }
    public decimal Price { get; set; }
}

public class LINQExamples
{
    public void BasicQueries()
    {
        var products = GetProducts();

        // 過濾
        var expensiveItems = products
            .Where(p => p.Price > 1000);

        // 投影
        var productNames = products
            .Select(p => p.Name);

        // 聚合
        var totalValue = products
            .Sum(p => p.Price);

        // 分組
        var byCategory = products
            .GroupBy(p => p.Category);

        // 巢狀查詢
        var result = from p in products
                     where p.Price ==
                           (from p2 in products
                            select p2.Price).Max()
                     select p;
    }
}
```

## LINQ to SQL

### 與資料庫的整合

```csharp
// LINQ to SQL 範例
[Table(Name = "Products")]
public class Product
{
    [Column(IsPrimaryKey = true)]
    public int ProductID { get; set; }

    [Column]
    public string ProductName { get; set; }

    [Column]
    public decimal UnitPrice { get; set; }
}

// 查詢
DataContext db = new DataContext(connString);
Table<Product> products = db.GetTable<Product>();

var expensiveProducts =
    from p in products
    where p.UnitPrice > 50
    orderby p.UnitPrice descending
    select p;

foreach (var p in expensiveProducts)
{
    Console.WriteLine("{0}: {1:C}", p.ProductName, p.UnitPrice);
}
```

## 對產業的影響

### LINQ 的歷史意義

```
┌────────────────────────────────────────────────────────┐
│           LINQ 對 .NET 生態的影響                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 統一的查詢方式                                     │
│     └─ SQL、物件、XML 使用相同語法                      │
│                                                        │
│  2. 編譯時型別檢查                                     │
│     └─ 減少執行期錯誤                                  │
│                                                        │
│  3. IntelliSense 支援                                 │
│     └─ 查詢時有程式碼自動完成                          │
│                                                        │
│  4. 可測試性                                           │
│     └─ 易於 Mock                                      │
│                                                        │
│  5. 為 Entity Framework 鋪路                          │
│     └─ 影響未來的 ORM 發展                             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 結論

C# 3.0 和 LINQ 的出現，標誌著微軟在語言整合查詢方面的重要創新。將查詢語法直接嵌入程式語言的設計，影響了後續許多語言和框架的發展。

---

## 延伸閱讀

- [C# 3.0 新特性](https://www.google.com/search?q=C+3.0+new+features)
- [LINQ 介紹](https://www.google.com/search?q=LINQ+language+integrated+query)
- [.NET 3.5 發布](https://www.google.com/search?q=.NET+3.5+released+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」文章集錦系列。*