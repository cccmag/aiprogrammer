#!/usr/bin/env python3
"""Optimizer comparison demonstration"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)

def demo():
    print("Optimizer Comparison Demo")
    print("=" * 50)

    torch.manual_seed(42)
    np.random.seed(42)

    x_train = torch.randn(200, 10)
    y_train = torch.randn(200, 1)

    train_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(x_train, y_train),
        batch_size=32,
        shuffle=True
    )

    optimizers = {
        'SGD': lambda m: optim.SGD(m.parameters(), lr=0.05),
        'SGD+Momentum': lambda m: optim.SGD(m.parameters(), lr=0.05, momentum=0.9),
        'Adam': lambda m: optim.Adam(m.parameters(), lr=0.01),
        'RMSprop': lambda m: optim.RMSprop(m.parameters(), lr=0.01),
    }

    results = {}

    print("\nTraining with different optimizers...")
    for name, opt_fn in optimizers.items():
        model = SimpleModel()
        optimizer = opt_fn(model)
        criterion = nn.MSELoss()

        losses = []
        for epoch in range(30):
            epoch_loss = 0
            for batch in train_loader:
                x, y = batch
                pred = model(x)
                loss = criterion(pred, y)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()
            losses.append(epoch_loss / len(train_loader))

        results[name] = losses
        print(f"  {name}: Final loss = {losses[-1]:.4f}")

    print("\nKey Observations:")
    print("- Adam typically converges fastest")
    print("- SGD + Momentum often achieves lower final loss")
    print("- RMSprop works well for RNN tasks")

    print("\nDemo completed!")

if __name__ == "__main__":
    demo()