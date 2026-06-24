"""
Keras 模型建構示範 — MNIST 手寫數字分類
"""
import numpy as np

def demo():
    print("=== Keras Model Building Demo ===\n")

    print("1. 資料準備")
    print("   - MNIST 資料集：28x28 灰階影像，共 10 類（0-9）")
    print("   - 訓練集：60,000 張")
    print("   - 測試集：10,000 張")

    print("\n2. 模型架構")
    print("   Input: 784 維向量 (28x28 flatten)")
    print("   Dense(512, relu) -> BatchNorm -> Dropout(0.2)")
    print("   Dense(256, relu) -> BatchNorm -> Dropout(0.2)")
    print("   Dense(128, relu) -> BatchNorm -> Dropout(0.2)")
    print("   Dense(10, softmax)")

    print("\n3. 編譯設定")
    print("   Optimizer: Adam (lr=0.001)")
    print("   Loss: Categorical Crossentropy")
    print("   Metrics: Accuracy")

    print("\n4. 訓練設定")
    print("   Epochs: 30")
    print("   Batch Size: 128")
    print("   Validation Split: 20%")
    print("   Callbacks: EarlyStopping, ModelCheckpoint")

    print("\n5. 預期結果")
    print("   - 訓練準確率：> 98%")
    print("   - 測試準確率：> 97%")

    print("\n6. 程式碼結構")
    print("""
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization

model = Sequential([
    Dense(512, activation='relu', input_shape=(784,)),
    BatchNormalization(),
    Dropout(0.2),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),
    Dense(128, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=30, batch_size=128, validation_split=0.2)
""")

    print("=== Demo Complete ===")

if __name__ == "__main__":
    demo()