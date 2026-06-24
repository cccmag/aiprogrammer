"""
PyTorch CNN 模型建構示範 — MNIST 手寫數字分類
"""
import torch

def demo():
    print("=== PyTorch CNN Model Building Demo ===\n")

    print("1. 資料集")
    print("   - MNIST: 28x28 灰階手寫數字影像")
    print("   - 10 類（0-9）")
    print("   - 訓練：60,000 張，測試：10,000 張")

    print("\n2. 模型架構：SimpleCNN")
    print("   Conv2d(1, 32, 3x3, padding=1) -> ReLU -> MaxPool(2x2)")
    print("   Conv2d(32, 64, 3x3, padding=1) -> ReLU -> MaxPool(2x2)")
    print("   Flatten -> Linear(64*7*7, 128) -> ReLU -> Dropout")
    print("   Linear(128, 10) -> Softmax")

    print("\n3. 訓練設定")
    print("   - Loss: CrossEntropyLoss")
    print("   - Optimizer: Adam (lr=0.001)")
    print("   - Epochs: 10")
    print("   - Batch Size: 64")

    print("\n4. 預期結果")
    print("   - 測試準確率：> 99%")

    print("\n5. 程式碼結構")
    print("""
import torch
import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = CNN()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
""")

    print("=== Demo Complete ===")

if __name__ == "__main__":
    demo()