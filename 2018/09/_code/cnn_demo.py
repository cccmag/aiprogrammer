"""
CNN 模型訓練示範 — CIFAR-10 影像分類
"""
import torch

def demo():
    print("=== CNN Model Training Demo ===\n")

    print("1. 資料集：CIFAR-10")
    print("   - 32x32 RGB 彩色圖像")
    print("   - 10 類：airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck")
    print("   - 訓練：50,000 張，測試：10,000 張")

    print("\n2. 模型架構：SimpleCNN")
    print("   Conv2d(3, 32, 3x3, padding=1) -> ReLU -> MaxPool(2x2)")
    print("   Conv2d(32, 64, 3x3, padding=1) -> ReLU -> MaxPool(2x2)")
    print("   Conv2d(64, 128, 3x3, padding=1) -> ReLU -> MaxPool(2x2)")
    print("   Flatten -> Dense(128*4*4, 256) -> ReLU -> Dropout(0.5)")
    print("   Dense(256, 10) -> Softmax")

    print("\n3. 訓練設定")
    print("   - Loss: CrossEntropyLoss")
    print("   - Optimizer: Adam (lr=0.001, weight_decay=1e-4)")
    print("   - Epochs: 50")
    print("   - Batch Size: 64")
    print("   - LR Schedule: StepLR (step=10, gamma=0.5)")

    print("\n4. 預期結果")
    print("   - 測試準確率：75-85%")

    print("\n5. 程式碼結構")
    print("""
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * 4 * 4)
        x = self.dropout(F.relu(self.fc1(x)))
        return self.fc2(x)
""")

    print("=== Demo Complete ===")

if __name__ == "__main__":
    demo()