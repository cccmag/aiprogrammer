import torch
import time


def demo():
    print("=" * 60)
    print("GPU 訓練範例")
    print("=" * 60)

    if not torch.cuda.is_available():
        print("\n警告：CUDA 不可用，將在 CPU 上執行（速度較慢）")
        device = torch.device("cpu")
    else:
        device = torch.device("cuda")
        print(f"\n[1] GPU 資訊")
        print(f"    裝置: {torch.cuda.get_device_name(0)}")
        print(f"    CUDA 版本: {torch.version.cuda}")

    print("\n[2] 簡單類神經網路訓練")
    print("    建立模型...")

    model = torch.nn.Sequential(
        torch.nn.Linear(784, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, 10)
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = torch.nn.CrossEntropyLoss()

    batch_size = 128
    x = torch.randn(batch_size, 784).to(device)
    y = torch.randint(0, 10, (batch_size,)).to(device)

    print(f"    輸入形狀: {x.shape}")
    print(f"    目標形狀: {y.shape}")

    print("\n[3] 訓練步驟")

    for step in range(3):
        start = time.time()

        optimizer.zero_grad()
        output = model(x)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()

        elapsed = (time.time() - start) * 1000
        print(f"    Step {step+1}: loss={loss.item():.4f}, time={elapsed:.2f}ms")

    print("\n[4] 混合精度測試（如果可用）")

    try:
        from torch.cuda.amp import autocast, GradScaler

        scaler = GradScaler()
        print("    AMP 可用，測試中...")

        x_large = torch.randn(256, 784).to(device)
        y_large = torch.randint(0, 10, (256,)).to(device)

        with autocast():
            output = model(x_large)
            loss = criterion(output, y_large)

        scaler.scale(loss).backward()
        print("    AMP 測試成功")
    except ImportError:
        print("    AMP 不可用（需要 PyTorch 1.6+）")

    if torch.cuda.is_available():
        print("\n[5] 記憶體使用")
        allocated = torch.cuda.memory_allocated(0) / 1024**2
        cached = torch.cuda.memory_reserved(0) / 1024**2
        print(f"    已分配: {allocated:.2f} MB")
        print(f"    快取: {cached:.2f} MB")

    print("\n" + "=" * 60)
    print("訓練範例完成")
    print("=" * 60)


if __name__ == "__main__":
    demo()