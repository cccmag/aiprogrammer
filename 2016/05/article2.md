# Go 語言的並發模型

## Go 的並發哲學

Go 的並發模型以「不要透過共享記憶體來通信；而是透過通信來共享記憶體」為指導原則。

## Goroutine

輕量級的執行緒：

```go
func main() {
    // 啟動 goroutine
    go sayHello("World")
    go sayHello("Go")

    // 等待
    time.Sleep(time.Second)
}

func sayHello(msg string) {
    fmt.Println("Hello,", msg)
}
```

## Channel

Goroutine 之間的通信方式：

```go
func main() {
    // 創建 channel
    ch := make(chan string)

    // 發送
    go func() {
        ch <- "Hello from goroutine"
    }()

    // 接收
    msg := <-ch
    fmt.Println(msg)
}
```

## Buffered Channel

帶緩衝的 channel：

```go
// 容量為 10 的 buffered channel
ch := make(chan int, 10)
```

## Select

多路復用 channel 操作：

```go
select {
case msg1 := <-ch1:
    fmt.Println("Received from ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("Received from ch2:", msg2)
case <-time.After(time.Second):
    fmt.Println("Timeout")
}
```

## Worker Pool

經典的並發模式：

```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, j)
        results <- j * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // 啟動 worker
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    // 發送任務
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)

    // 收集結果
    for a := 1; a <= 5; a++ {
        <-results
    }
}
```

延伸閱讀：
- [Google 搜尋：Go concurrent programming](https://www.google.com/search?q=Go+concurrent+programming)
- [Google 搜尋：Go channels tutorial](https://www.google.com/search?q=Go+channels+tutorial)