import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, TensorDataset
import math


def demo():
    # ── 1. Tensor 基礎與裝置管理 ──
    print("=== 1. Tensor Ops ===")
    x = torch.linspace(0, 2 * math.pi, 100)
    y = torch.sin(x) + 0.1 * torch.randn(x.size())
    print(f"x: {x.shape}, y: {y.shape}")

    # 矩陣運算
    A = torch.randn(3, 4)
    B = torch.randn(4, 5)
    C = A.mm(B)
    print(f"matmul: {A.shape} x {B.shape} = {C.shape}")

    # 形狀操作
    t = torch.arange(12).reshape(3, 4)
    print(f"reshape: {t.shape}")

    # ── 2. Autograd ──
    print("\n=== 2. Autograd ===")
    a = torch.tensor([2.0, 3.0], requires_grad=True)
    b = torch.tensor([4.0, 5.0], requires_grad=True)
    loss = ((a * b) ** 2).sum()
    loss.backward()
    print(f"da/dloss: {a.grad}")
    print(f"db/dloss: {b.grad}")

    # 停止梯度追蹤
    with torch.no_grad():
        c = a * b
    print(f"no_grad: {c.requires_grad}")

    # ── 3. nn.Module ──
    print("\n=== 3. nn.Module ===")

    class SineNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(1, 32),
                nn.ReLU(),
                nn.Linear(32, 32),
                nn.ReLU(),
                nn.Linear(32, 1),
            )

        def forward(self, x):
            return self.net(x)

    model = SineNet()
    print(f"Model parameters: {sum(p.numel() for p in model.parameters())}")

    # 自訂層
    class CustomLinear(nn.Module):
        def __init__(self, in_features, out_features):
            super().__init__()
            self.weight = nn.Parameter(torch.randn(out_features, in_features))
            self.bias = nn.Parameter(torch.zeros(out_features))

        def forward(self, x):
            return F.linear(x, self.weight, self.bias)

    model2 = nn.Sequential(CustomLinear(1, 32), nn.ReLU(), nn.Linear(32, 1))

    # ── 4. DataLoader ──
    print("\n=== 4. DataLoader ===")
    X = torch.linspace(0, 2 * math.pi, 200).unsqueeze(1)
    Y = torch.sin(X) + 0.05 * torch.randn(X.size())
    dataset = TensorDataset(X, Y)
    loader = DataLoader(dataset, batch_size=16, shuffle=True)
    print(f"Batches: {len(loader)}, batch size: {loader.batch_size}")

    # ── 5. 最佳化器與學習率排程 ──
    print("\n=== 5. Optimizer & Scheduler ===")
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
    print(f"Initial lr: {scheduler.get_last_lr()[0]:.6f}")
    # 先進行一步最佳化，再步進排程器
    optimizer.zero_grad()
    loss = model(X[:16]).sum()
    loss.backward()
    optimizer.step()
    scheduler.step()
    print(f"After 1 step: {scheduler.get_last_lr()[0]:.6f}")

    # 還原排程器
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

    # ── 6. 完整訓練迴圈 ──
    print("\n=== 6. Training Loop ===")
    model.train()
    criterion = nn.MSELoss()
    losses = []
    for epoch in range(200):
        epoch_loss = 0.0
        for xb, yb in loader:
            pred = model(xb)
            loss = criterion(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        scheduler.step()
        avg_loss = epoch_loss / len(loader)
        losses.append(avg_loss)
        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch+1:3d}, Loss: {avg_loss:.6f}, LR: {scheduler.get_last_lr()[0]:.6f}")

    # ── 7. 模型儲存與載入 ──
    print("\n=== 7. Save & Load ===")
    torch.save(model.state_dict(), "/tmp/sinenet.pth")
    model2 = SineNet()
    model2.load_state_dict(torch.load("/tmp/sinenet.pth"))
    model2.eval()
    with torch.no_grad():
        test_x = torch.tensor([[0.5], [1.0], [1.5]])
        preds = model2(test_x)
        print(f"Test predictions: {preds.squeeze().tolist()}")

    print("\n=== All done ===")
    return losses


if __name__ == "__main__":
    demo()
