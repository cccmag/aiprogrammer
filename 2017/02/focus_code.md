# TensorFlow 1.0 快速上手

## 程式實作目錄

本期程式中包含 TensorFlow 1.0 的基礎使用範例：

1. **TensorFlow 基礎**：`tensorflow_basics.py`
2. **Keras 順序模型**：`keras_model.py`
3. **自訂訓練循環**：`custom_training.py`

## 執行方式

```bash
cd _code/
python3 tensorflow_basics.py
python3 keras_model.py
python3 custom_training.py
```

或執行 `bash test.sh` 來運行所有範例。

---

## TensorFlow 基礎

### tensorflow_basics.py

```python
#!/usr/bin/env python3
"""TensorFlow 1.0 基礎操作示範"""

def demo():
    print("=" * 60)
    print("TensorFlow 1.0 基礎操作示範")
    print("=" * 60)

    print("\n注意：TensorFlow 1.0 使用靜態計算圖")
    print("需要通過 Session 來執行計算")

    print("\n1. 基本計算：")
    print("   import tensorflow as tf")
    print("   a = tf.constant(2.0)")
    print("   b = tf.constant(3.0)")
    print("   c = a + b")
    print("   with tf.Session() as sess:")
    print("       print(sess.run(c))  # 輸出: 5.0")

    print("\n2. Placeholder 和 feed_dict：")
    print("   x = tf.placeholder(tf.float32)")
    print("   y = x * 2")
    print("   with tf.Session() as sess:")
    print("       result = sess.run(y, feed_dict={x: [1, 2, 3]})")
    print("       # 輸出: [2.0, 4.0, 6.0]")

    print("\n3. 變數：")
    print("   W = tf.Variable(tf.random_normal([784, 10]))")
    print("   b = tf.Variable(tf.zeros([10]))")
    print("   sess.run(tf.global_variables_initializer())")

    print("\n4. tf.layers 高層 API：")
    print("   x = tf.placeholder(tf.float32, shape=[None, 784])")
    print("   h = tf.layers.dense(x, 128, activation=tf.nn.relu)")
    print("   y = tf.layers.dense(h, 10, activation=tf.nn.softmax)")

if __name__ == "__main__":
    demo()
```

## Keras 模型

### keras_model.py

```python
#!/usr/bin/env python3
"""Keras 順序模型示範"""

def demo():
    print("=" * 60)
    print("Keras 順序模型示範")
    print("=" * 60)

    print("\nKeras 提供了兩種模型建構方式：")
    print("1. Sequential：簡單的層次堆疊")
    print("2. Functional API：更靈活的多輸入/輸出")

    print("\nSequential 模型範例：")
    print("   from keras.models import Sequential")
    print("   from keras.layers import Dense")
    print("")
    print("   model = Sequential([")
    print("       Dense(128, activation='relu', input_shape=(784,)),")
    print("       Dense(64, activation='relu'),")
    print("       Dense(10, activation='softmax')")
    print("   ])")

    print("\n編譯和訓練：")
    print("   model.compile(")
    print("       optimizer='adam',")
    print("       loss='categorical_crossentropy',")
    print("       metrics=['accuracy']")
    print("   )")
    print("   model.fit(x_train, y_train, epochs=10, batch_size=32)")

    print("\n預測：")
    print("   predictions = model.predict(x_test)")

if __name__ == "__main__":
    demo()
```

## 自訂訓練循環

### custom_training.py

```python
#!/usr/bin/env python3
"""TensorFlow 自訂訓練循環示範"""

def demo():
    print("=" * 60)
    print("TensorFlow 自訂訓練循環示範")
    print("=" * 60)

    print("\n什麼時候需要自訂訓練？")
    print("- 需要更精確的控制訓練過程")
    print("- 實現自訂損失函數或正規化")
    print("- 研究新穎的訓練技巧")

    print("\n基本自訂訓練循環：")
    print("   optimizer = tf.train.AdamOptimizer(learning_rate=0.001)")
    print("   ")
    print("   for epoch in range(num_epochs):")
    print("       for batch in dataset:")
    print("           with tf.GradientTape() as tape:")
    print("               predictions = model(x)")
    print("               loss = compute_loss(y, predictions)")
    print("       gradients = tape.gradient(loss, model.variables)")
    print("       optimizer.apply_gradients(zip(gradients, model.variables))")

    print("\ntf.GradientTape (TensorFlow 2.x style):")
    print("   記錄運算以便自動微分")

    print("\n注意：TensorFlow 1.x 和 2.x 語法有差異")
    print("本範例展示的是概念，非可直接執行代碼")

if __name__ == "__main__":
    demo()
```

---

## 延伸閱讀

- [TensorFlow 官方網站](https://www.google.com/search?q=TensorFlow+official+website+tutorial)
- [Keras+官方文檔](https://www.google.com/search?q=Keras+official+documentation)
- [TensorFlow+1.0+快速上手](https://www.google.com/search?q=TensorFlow+1.0+tutorial+get+started)

---

*本期程式實作到此結束。*