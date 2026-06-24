# 主題四：Scala — 融合物件導向與函式式

## Scala 的誕生

Scala 由 Martin Odersky 於 2001 年在 EPFL（瑞士洛桑聯邦理工學院）開始開發，2004 年正式對外發布。Scala 的名稱來自「**Sca**lable **La**nguage」——一種可擴展的語言，設計用於解決從小型腳本到大型企業系統的各種問題。

Martin Odersky 是 Java 泛型和註解處理器的先驅，他的目標是創造一種語言，結合物件導向和函式式程式設計的最佳實踐。

## 融合兩種範式

Scala 最顯著的特點是無縫融合了物件導向和函式式程式設計：

### 一切皆為物件

在 Scala 中，連續值也是物件。沒有 Java 中的基本類型（primitive types）和引用類型（reference types）之分。

```scala
// 方法也是物件
val add = (x: Int, y: Int) => x + y
val result = add(1, 2)  // result = 3

// 函式作為參數
def applyTwice(f: Int => Int, x: Int): Int = f(f(x))
val result = applyTwice(x => x * 2, 5)  // 20
```

### 案例類別與模式匹配

案例類別（Case Classes）自動生成equals、hashCode、toString 和 copy 方法，非常適合建模不可變資料。

```scala
// 定義案例類別
case class Person(name: String, age: Int)

// 模式匹配
def describe(person: Person): String = person match {
  case Person("Alice", 30) => "Alice is 30 years old"
  case Person(name, age) if age < 18 => s"$name is a minor"
  case Person(name, _) => s"$name is an adult"
}
```

### 語法糖：apply 與 update

Scala 允許你定義 apply 和 update 方法，提供優雅的語法：

```scala
class ArrayOps(val items: Array[Int]) {
  def apply(index: Int): Int = items(index)
  def update(index: Int, value: Int): Unit = items(index) = value
}

val arr = new ArrayOps(Array(1, 2, 3))
val x = arr(0)    // 相當於 arr.apply(0)
arr(0) = 42       // 相當於 arr.update(0, 42)
```

## 強大的類型系統

Scala 的類型系統極為強大，支援：

### 泛型

```scala
class Stack[T] {
  private var elements: List[T] = Nil
  def push(x: T): Unit = elements = x :: elements
  def pop(): T = {
    val currentTop = elements.head
    elements = elements.tail
    currentTop
  }
  def top: T = elements.head
}
```

### 型態約束

```scala
// 上界：T 必須是 Comparable 的子類
def max[T <: Comparable[T]](a: T, b: T): T =
  if (a.compareTo(b) > 0) a else b

// 視圖約束：支援隱式轉換
def square[T <% Numeric[T]](x: T): T = x * x
```

### 抽象類型成員

```scala
trait Container {
  type T
  def items: List[T]
  def add(item: T): Container
}
```

## 並發與 Akka

Scala 生態中最著名的並發框架是 Akka，實現了 Actor 模型：

```scala
import akka.actor._

// 定義 Actor
class HelloActor extends Actor {
  def receive = {
    case name: String =>
      println(s"Hello, $name!")
      sender() ! s"Hello, $name!"
    case _ =>
      println("Unknown message")
  }
}

// 建立和使用了 Actor
val system = ActorSystem("HelloSystem")
val helloActor = system.actorOf(Props[HelloActor], name = "hello")

helloActor ! "World"  // 發送非同步訊息
```

Akka 的 Actor 模型使得構建分散式和容錯系統變得優雅且可靠。

## 函式式集合

Scala 的集合庫充分體現了函式式設計：

```scala
val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

// map: 轉換每個元素
val squares = numbers.map(x => x * x)

// filter: 篩選元素
val evens = numbers.filter(_ % 2 == 0)

// reduce: 聚合運算
val sum = numbers.reduce(_ + _)

// flatMap: 扁平化映射
val words = List("Hello", "World")
val chars = words.flatMap(_.toList)

// 函式組合
val result = numbers
  .filter(_ > 3)
  .map(_ * 2)
  .take(3)
```

## 使用場景

Scala 在以下領域特別受歡迎：

### 大資料處理

Apache Spark 使用 Scala 作為主要 API。Spark 的 DataFrame 和 Dataset API 都基於 Scala 的函式式集合。

### 網路服務

PayPal、LinkedIn、Twitter 等公司使用 Scala 建構高效能網路服務。Play Framework 是 Scala 生態中最受歡迎的 Web 框架。

### 分散式系統

Scala 的類型安全和函式式特性使其成為建構可靠分散式系統的理想選擇。

## SBT：Scala 的建構工具

SBT（Simple Build Tool）是 Scala 專案的標準建構工具：

```scala
// build.sbt
name := "my-project"

version := "1.0"

scalaVersion := "2.11.8"

libraryDependencies ++= Seq(
  "com.typesafe.play" %% "play-json" % "2.5.0",
  "org.scalatest" %% "scalatest" % "3.0.0" % "test"
)
```

## 小結

Scala 展示了如何將物件導向和函式式程式設計融合在一種語言中。從強大的類型系統到優雅的集合操作，從 Actor 模型到函式式回應式程式，Scala 提供了豐富的工具來解決各種問題。

下一篇文章中，我們將深入探討函式式程式設計的核心概念——不可變性與資料結構。