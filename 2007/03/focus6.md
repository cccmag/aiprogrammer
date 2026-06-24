# 函數式語言的興起

## 前言

2007 年，函數式編程概念開始進入主流語言，Haskell 和 Scala 獲得關注。

## Haskell 的特色

```haskell
-- Haskell 純函數式範例
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- 高階函數
square :: [Integer] -> [Integer]
square xs = map (\x -> x * x) xs
```

## Scala 的崛起

Scala 在 JVM 上結合了物件導向和函數式編程：

```scala
// Scala 範例
val numbers = List(1, 2, 3, 4, 5)
val sum = numbers.reduce(_ + _)

// 模式匹配
def describe(x: Any) = x match {
    case 1 => "one"
    case "hello" => "greeting"
    case _ => "unknown"
}
```

## 影響

函數式編程的概念（純函式、不可變性、高階函數）開始影響主流語言的設計。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」本期焦點系列文章。*