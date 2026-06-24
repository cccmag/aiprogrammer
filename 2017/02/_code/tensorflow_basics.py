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