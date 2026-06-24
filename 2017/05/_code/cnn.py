import numpy as np


def relu(x):
    return np.maximum(0, x)


def relu_gradient(x):
    return (x > 0).astype(float)


def max_pooling(feature_map, pool_size=2, stride=2):
    c, h, w = feature_map.shape
    out_h = h // stride
    out_w = w // stride
    output = np.zeros((c, out_h, out_w))
    for f in range(c):
        for i in range(out_h):
            for j in range(out_w):
                h_start = i * stride
                w_start = j * stride
                output[f, i, j] = np.max(
                    feature_map[f, h_start:h_start+pool_size, w_start:w_start+pool_size]
                )
    return output


def conv2d(image, kernel, stride=1, padding=0):
    if padding > 0:
        image = np.pad(image, padding, mode='constant')
    kh, kw = kernel.shape
    ih, iw = image.shape
    out_h = (ih - kh) // stride + 1
    out_w = (iw - kw) // stride + 1
    output = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            output[i, j] = np.sum(
                image[i*stride:i*stride+kh, j*stride:j*stride+kw] * kernel
            )
    return output


class SimpleCNN:
    def __init__(self, num_filters=8):
        self.conv1_weights = np.random.randn(num_filters, 3, 3) * 0.1
        self.conv2_weights = np.random.randn(num_filters * 2, 3, 3) * 0.1
        self.num_filters = num_filters

    def forward(self, x):
        self.conv1_out = np.array([relu(conv2d(x, f)) for f in self.conv1_weights])
        self.pool1_out = max_pooling(self.conv1_out, pool_size=2, stride=2)

        self.conv2_out = np.array([relu(conv2d(self.pool1_out[i], f))
                                   for i, f in enumerate(self.conv2_weights[:len(self.pool1_out)])])
        self.pool2_out = max_pooling(self.conv2_out, pool_size=2, stride=2)

        return self.pool2_out

    def extract_features(self, x):
        features = self.forward(x)
        return np.mean(features, axis=(1, 2))


def demo():
    np.random.seed(42)
    print("Creating test image...")
    image = np.random.randn(28, 28).astype(np.float32)
    print(f"Input image shape: {image.shape}")

    print("\nInitializing CNN...")
    cnn = SimpleCNN(num_filters=8)
    print(f"Number of filters in conv1: {len(cnn.conv1_weights)}")

    print("\nRunning forward pass...")
    output = cnn.forward(image)
    print(f"Output shape: {output.shape}")

    features = cnn.extract_features(image)
    print(f"Extracted features shape: {features.shape}")
    print(f"Feature values: {features}")

    print("\nSimple CNN demo completed successfully!")


if __name__ == "__main__":
    demo()