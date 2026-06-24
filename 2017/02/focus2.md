# 計算圖與 Session：TensorFlow 核心概念

## 前言

理解計算圖和 Session 是掌握 TensorFlow 的關鍵。與傳統程式設計的「立即執行」模式不同，TensorFlow 採用了「先建構後執行」的計算模型。本篇文章深入解析這些核心概念。

## 計算圖概念

### 什麼是計算圖？

計算圖是一種有向圖，用來表示計算任務：

```
節點（Node）：運算操作
邊（Edge）：張量（資料）在節點間流動

a ──┐
    ├── Add ──→ c
b ──┘
```

### TensorFlow 的計算圖

```python
import tensorflow as tf

# 這行代碼只是「定義」計算，不會立即執行
a = tf.constant(2.0)
b = tf.constant(3.0)
c = a + b  # 這裡的 c 是一個操作，不是結果

print(c)  # Tensor("add:0", shape=(), dtype=float32)
# 输出是張量的描述，不是具體的數值
```

### 計算圖的組成

```
TensorFlow 計算圖：
├── 節點（Operation）
│   ├── 常數：tf.constant
│   ├── 變數：tf.Variable
│   ├── 佔位符：tf.placeholder
│   └── 運算：tf.add, tf.matmul, ...
└── 邊（Tensor）
    ├── 張量流動
    └── 依賴關係
```

## Session 執行

### 為什麼需要 Session？

計算圖只是定義了計算，必須透過 Session 才能實際執行：

```python
import tensorflow as tf

# 建立計算圖
a = tf.constant(2.0)
b = tf.constant(3.0)
c = a + b

# 建立 Session 並執行
with tf.Session() as sess:
    result = sess.run(c)
    print(result)  # 5.0
```

### Session 的底層運作

```python
# Session 建立連接到 TensorFlow 運行時
# sess.run() 觸發圖的執行

with tf.Session() as sess:
    # sess.run() 的參數
    # fetches: 要獲取的張量或操作
    # feed_dict: 輸入資料

    # 執行單一節點
    result = sess.run(c)

    # 執行多個節點
    a, b = sess.run([node_a, node_b])

    # 使用 feed_dict 動態輸入
    x = tf.placeholder(tf.float32)
    y = x * 2

    result = sess.run(y, feed_dict={x: [1.0, 2.0, 3.0]})
    print(result)  # [2.0, 4.0, 6.0]
```

### 圖管理

```python
# 預設圖
print(tf.get_default_graph())

# 建立新圖
g = tf.Graph()

# 在指定圖中操作
with g.as_default():
    a = tf.constant(1.0)
    b = tf.constant(2.0)
    c = a + b

# 切換預設圖
with tf.Session(graph=g) as sess:
    result = sess.run(c)
    print(result)
```

## Placeholder 與餵送資料

### Placeholder 的用途

Placeholder 是圖中的「空洞」，用於接收外部資料：

```python
import tensorflow as tf

# 定義具有 placeholder 的計算圖
x = tf.placeholder(tf.float32, shape=[None, 784])
y_true = tf.placeholder(tf.float32, shape=[None, 10])

W = tf.Variable(tf.random_normal([784, 10]))
b = tf.Variable(tf.zeros([10]))
y_pred = tf.nn.softmax(tf.matmul(x, W) + b)

# 使用 feed_dict 餵送資料
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_true * tf.log(y_pred), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# 訓練時餵送資料
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in range(1000):
        # 每次餵送一個 batch
        batch_x, batch_y = get_next_batch(i)
        sess.run(train_step, feed_dict={
            x: batch_x,
            y_true: batch_y
        })
```

### 餵送資料的資料類型

```python
# 張量
tf.placeholder(tf.float32)

# 陣列
tf.placeholder(tf.int32, shape=[None, 100])

# 稀疏矩陣
tf.sparse_placeholder(tf.float32)

# 字串
tf.placeholder(tf.string)
```

## 變數與狀態

### Variable 的生命週期

```python
# 建立變數
W = tf.Variable(tf.random_normal([784, 10]), name='weights')
b = tf.Variable(tf.zeros([10]), name='biases')

# 使用變數前必須初始化
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    # 存取變數值
    print(sess.run(W))

    # 訓練時更新
    sess.run(train_step)
```

### 變數儲存與恢復

```python
# 建立 Saver
saver = tf.train.Saver()

# 儲存模型
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # 訓練...
    save_path = saver.save(sess, '/tmp/model.ckpt')

# 恢復模型
with tf.Session() as sess:
    saver.restore(sess, '/tmp/model.ckpt')
    print(sess.run(y_pred, feed_dict={x: test_data}))
```

## 圖最佳化與執行

### 自動最佳化

TensorFlow 會自動最佳化計算圖：

1. **節點融合**：將多個操作合併
2. **常量摺疊**：編譯時計算常量表達式
3. **記憶體最佳化**：重用記憶體緩衝區

### 設備指定

```python
# 指定在 CPU 上執行
with tf.device('/cpu:0'):
    a = tf.constant([1.0, 2.0])
    b = tf.constant([3.0, 4.0])
    c = a + b

# 指定在 GPU 上執行
with tf.device('/gpu:0'):
    result = tf.matmul(matrix_a, matrix_b)
```

### GPU 設定

```python
# 設定 GPU 記憶體成長
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

# 限制 GPU 使用量
config.gpu_options.per_process_gpu_memory_fraction = 0.5
```

## 結論

計算圖和 Session 是 TensorFlow 的核心概念：

- **計算圖**：定義了計算的「藍圖」
- **Session**：執行計算圖的「引擎」
- **Placeholder**：動態輸入資料的「入口」
- **Variable**：在圖執行過程中保持狀態

理解這些概念對於有效地使用 TensorFlow 至關重要。雖然後來 TensorFlow 引入了 Eager Execution 模式簡化了開發流程，但計算圖的設計理念仍然值得深入理解。

---

## 延伸閱讀

- [TensorFlow+計算圖+教程](https://www.google.com/search?q=TensorFlow+computational+graph+tutorial)
- [TensorFlow+Session+使用](https://www.google.com/search?q=TensorFlow+Session+usage)
- [TensorFlow+placeholder+feed_dict](https://www.google.com/search?q=TensorFlow+placeholder+feed_dict)
- [TensorFlow+變數+初始化](https://www.google.com/search?q=TensorFlow+variable+initialization)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」焦點系列之一。*