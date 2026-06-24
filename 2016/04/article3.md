# Scala 與 Akka Actor 模型

## Actor 模型簡介

Actor 模型是一種並行計算的數學模型，每個 Actor 是獨立的運算單元，透過訊息傳遞進行通訊。Actor 的特點：

- **封閉狀態**：每個 Actor 的狀態只能由自己修改
- **無共享狀態**：Actor 之間不通過共享記憶體通信
- **非同步訊息傳遞**：Actor 透過發送和接收訊息協作

## Akka 介紹

Akka 是 Scala/JVM 的 Actor 實現，提供：

- 輕量級執行緒（百萬級 Actor）
- 容錯機制（監督策略）
- 位置透明性（Actor 可在網路任意節點）
- 持久化（Event sourcing）

## 基本 Actor 實現

```scala
import akka.actor._

// 定義訊息類型
case class Greet(name: String)
case class GreetResult(message: String)

// 定義 Actor
class GreetingActor extends Actor {
  def receive = {
    case Greet(name) =>
      val message = s"Hello, $name!"
      println(message)
      sender() ! GreetResult(message)
  }
}

// 使用 Actor
val system = ActorSystem("MySystem")
val greeter = system.actorOf(Props[GreetingActor], "greeter")

greeter ! Greet("World")  // 非同步發送
```

## 監督策略

Akka 的監督策略讓 Actor 在失敗時能優雅恢復：

```scala
class SupervisedActor extends Actor {
  def receive = {
    case ex: Exception => throw ex
  }

  // 監督子 Actor 的失敗
  override def supervisorStrategy: SupervisorStrategy =
    OneForOneStrategy(maxNrOfRetries = 3, withinTimeRange = 1.minute) {
      case _: ArithmeticException => Resume
      case _: NullPointerException => Restart
      case _: Exception => Stop
    }
}
```

## Router 與群組

```scala
// 建立 Router
val router = system.actorOf(
  Props[WorkerActor].withRouter(RoundRobinRouter(nrOfInstances = 5)),
  "worker-router"
)

// 向所有 worker 發送訊息
(1 to 10).foreach(i => router ! Work(i))
```

## 分散式 Akka

Akka Cluster 讓 Actor 跨網路運行：

```scala
// 設定 Cluster
val config = ConfigFactory.parseString("""
  akka {
    actor {
      provider = "akka.cluster.ClusterActorRefProvider"
    }
    cluster {
      seed-nodes = [
        "akka.tcp://MySystem@host1:2551",
        "akka.tcp://MySystem@host2:2551"
      ]
    }
  }
""")

val system = ActorSystem("MySystem", config)
```

## 實戰：即時資料處理管道

```scala
class DataPipeline extends Actor {
  var buffer = Vector.empty[DataPoint]

  def receive = {
    case dp: DataPoint =>
      buffer = buffer :+ dp
      if (buffer.size >= batchSize) {
        processBatch(buffer)
        buffer = Vector.empty
      }

    case Flush =>
      if (buffer.nonEmpty) {
        processBatch(buffer)
        buffer = Vector.empty
      }
  }

  def processBatch(data: Vector[DataPoint]): Unit = {
    // 批次處理
    data.foreach(dp => analyze(dp))
  }
}
```

## 延伸閱讀

- [Google 搜尋：Akka Actor model tutorial](https://www.google.com/search?q=Akka+Actor+model+tutorial)
- [Google 搜尋：Scala distributed systems](https://www.google.com/search?q=Scala+distributed+systems)