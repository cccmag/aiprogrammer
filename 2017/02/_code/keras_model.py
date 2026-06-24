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