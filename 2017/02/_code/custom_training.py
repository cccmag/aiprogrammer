#!/usr/bin/env python3
"""TensorFlow 自訂訓練循環示範"""

def demo():
    print("=" * 60)
    print("TensorFlow 自訂訓練循環示範")
    print("=" * 60)

    print("\n什麼時候需要自訂訓練？")
    print("- 需要更精確的控制訓練過程")
    print("- 需要自訂損失函數或正規化")
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