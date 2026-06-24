#!/usr/bin/env python3
"""DCGAN implementation for MNIST digit generation - simplified demo"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

LATENT_DIM = 100
IMAGE_SIZE = 28
CHANNELS = 1
G_FEATURES = 32
D_FEATURES = 32
EPOCHS = 5
BATCH_SIZE = 64
LEARNING_RATE = 0.0002

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(LATENT_DIM, G_FEATURES * 4, 4, 1, 0, bias=False),
            nn.BatchNorm2d(G_FEATURES * 4),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES * 4, G_FEATURES * 2, 3, 2, 1, bias=False),
            nn.BatchNorm2d(G_FEATURES * 2),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES * 2, G_FEATURES, 4, 2, 1, bias=False),
            nn.BatchNorm2d(G_FEATURES),
            nn.ReLU(True),
            nn.ConvTranspose2d(G_FEATURES, CHANNELS, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(CHANNELS, D_FEATURES, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES, D_FEATURES * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(D_FEATURES * 2),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES * 2, D_FEATURES * 4, 3, 2, 1, bias=False),
            nn.BatchNorm2d(D_FEATURES * 4),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(D_FEATURES * 4, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input).view(-1, 1).squeeze(1)

def train_step(G, D, criterion, optimizer_G, optimizer_D, device):
    real_images = torch.randn(BATCH_SIZE, CHANNELS, IMAGE_SIZE, IMAGE_SIZE).to(device)
    real_labels = torch.ones(BATCH_SIZE).to(device)
    fake_labels = torch.zeros(BATCH_SIZE).to(device)

    noise = torch.randn(BATCH_SIZE, LATENT_DIM, 1, 1).to(device)
    fake_images = G(noise)

    output_real = D(real_images)
    output_fake = D(fake_images.detach())

    loss_D = criterion(output_real, real_labels) + criterion(output_fake, fake_labels)

    optimizer_D.zero_grad()
    loss_D.backward()
    optimizer_D.step()

    output_fake = D(fake_images)
    loss_G = criterion(output_fake, real_labels)

    optimizer_G.zero_grad()
    loss_G.backward()
    optimizer_G.step()

    return loss_D.item(), loss_G.item()

def demo():
    print("DCGAN for MNIST Digit Generation")
    print("=" * 50)

    device = torch.device("cpu")

    G = Generator().to(device)
    D = Discriminator().to(device)

    criterion = nn.BCELoss()
    optimizer_G = optim.Adam(G.parameters(), lr=LEARNING_RATE, betas=(0.5, 0.999))
    optimizer_D = optim.Adam(D.parameters(), lr=LEARNING_RATE, betas=(0.5, 0.999))

    print(f"Device: {device}")
    print(f"Latent dimension: {LATENT_DIM}")
    print(f"Epochs: {EPOCHS}")
    print()

    print("Training GAN (simplified demo with random data)...")
    for epoch in range(EPOCHS):
        loss_D, loss_G = train_step(G, D, criterion, optimizer_G, optimizer_D, device)
        if (epoch + 1) % 1 == 0:
            print(f"Epoch [{epoch+1}/{EPOCHS}] Loss D: {loss_D:.4f} Loss G: {loss_G:.4f}")

    noise = torch.randn(4, LATENT_DIM, 1, 1).to(device)
    generated_images = G(noise).cpu().detach().numpy()

    print()
    print("Generated images shape:", generated_images.shape)
    print("Sample values - min:", generated_images.min(), "max:", generated_images.max())
    print("Demo completed successfully!")

if __name__ == "__main__":
    demo()