#!/usr/bin/env python3
"""PyTorch Lightning Demo: MNIST Classification"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl


class LitMNIST(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        return self.fc3(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log('train_loss', loss, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        val_loss = F.cross_entropy(y_hat, y)
        self.log('val_loss', val_loss, prog_bar=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log('test_loss', loss, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)


def generate_mock_data(num_samples=1000):
    train_data = []
    for _ in range(num_samples):
        x = torch.randn(1, 28, 28)
        y = torch.randint(0, 10, (1,)).item()
        train_data.append((x, y))
    return train_data


class MockDataModule(pl.LightningDataModule):
    def __init__(self, num_samples=1000, batch_size=32):
        super().__init__()
        self.num_samples = num_samples
        self.batch_size = batch_size

    def setup(self, stage=None):
        self.train_dataset = generate_mock_data(self.num_samples)

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True
        )

    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset[:100],
            batch_size=self.batch_size
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_dataset[:100],
            batch_size=self.batch_size
        )


def demo():
    print("=" * 60)
    print("PyTorch Lightning Demo - MNIST Classification")
    print("=" * 60)

    model = LitMNIST()
    print(f"\nModel parameters: {sum(p.numel() for p in model.parameters()):,}")

    data_module = MockDataModule(num_samples=500, batch_size=32)

    print("\nSimulating training steps...")
    trainer = pl.Trainer(
        max_epochs=2,
        logger=False,
        enable_progress_bar=False
    )

    trainer.fit(model, data_module)

    print("\nModel structure:")
    print(model)

    print("\n" + "=" * 60)
    print("Lightning demo completed!")
    print("=" * 60)


if __name__ == '__main__':
    demo()