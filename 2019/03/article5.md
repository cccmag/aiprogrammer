# 模型可視化

## Keras 模型視覺化

### 模型結構

```python
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import plot_model

model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(784,), name='input'),
    layers.Dense(32, activation='relu', name='hidden1'),
    layers.Dense(16, activation='relu', name='hidden2'),
    layers.Dense(10, activation='softmax', name='output')
])

model.summary()
```

### 輸出模型圖

```python
plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)
```

## Netron 模型視覺化

```python
model.save('model.h5')

import netron
netron.start('model.h5')
```

## 訓練歷史視覺化

```python
import matplotlib.pyplot as plt

history = model.fit(
    x_train, y_train,
    epochs=20,
    validation_split=0.2
)

def plot_training_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(history.history['loss'], label='Training Loss')
    ax1.plot(history.history['val_loss'], label='Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Loss over Epochs')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(history.history['accuracy'], label='Training Accuracy')
    ax2.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Accuracy over Epochs')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

plot_training_history(history)
```

## 權重分佈

```python
import numpy as np

def plot_weight_distributions(model):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i, layer in enumerate(model.layers):
        if layer.kernel is not None:
            weights = layer.kernel.numpy().flatten()
            axes[i].hist(weights, bins=50, alpha=0.7, color='blue')
            axes[i].set_title(f'{layer.name}\n(shape: {layer.kernel.shape})')
            axes[i].set_xlabel('Weight Value')
            axes[i].set_ylabel('Frequency')
            axes[i].grid(True)

    plt.tight_layout()
    plt.show()

plot_weight_distributions(model)
```

## 中間層輸出

```python
import matplotlib.pyplot as plt

layer_outputs = [layer.output for layer in model.layers[:3]]
activation_model = keras.Model(inputs=model.input, outputs=layer_outputs)

sample = x_test[:1]
activations = activation_model.predict(sample)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, activation in enumerate(activations):
    axes[i].imshow(activation[0].reshape(-1, 1), cmap='viridis', aspect='auto')
    axes[i].set_title(f'Layer {i} Output')
    axes[i].set_xlabel('Neuron')
    axes[i].set_ylabel('Activation')

plt.tight_layout()
plt.show()
```

## 濾波器視覺化

```python
def visualize_filters(model, layer_name, num_filters=16):
    layer = model.get_layer(layer_name)
    filters, biases = layer.get_weights()

    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    axes = axes.flatten()

    for i in range(min(num_filters, len(filters[0]))):
        filter_values = filters[:, 0, i]
        axes[i].plot(filter_values)
        axes[i].set_title(f'Filter {i}')
        axes[i].grid(True)

    plt.tight_layout()
    plt.show()

visualize_filters(model, 'hidden1')
```

## Grad-CAM 熱力圖

```python
try:
    import tf_keras_vis

    from tf_keras_vis.activation_maximization import ActivationMaximization
    from tf_keras_vis.activation_maximization.visualizers import ScorecamView

    def plot_grad_cam(model, image, class_idx):
        def loss(output):
            return output[0][class_idx]

        from tf_keras_vis.gradcam import Gradcam
        from tf_keras_vis.utils.model_modifiers import ReplaceToLinear

        gradcam = Gradcam(model, model_modifier=ReplaceToLinear(), clone=True)
        cam = gradcam(loss, image)

        plt.imshow(image.reshape(28, 28), cmap='gray')
        plt.imshow(cam[0], cmap='jet', alpha=0.5)
        plt.title(f'Grad-CAM for class {class_idx}')
        plt.show()
except ImportError:
    print("tf_keras_vis 未安裝")
```

## t-SNE 特徵視覺化

```python
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

intermediate_model = keras.Model(
    inputs=model.input,
    outputs=model.layers[-2].output
)

features = intermediate_model.predict(x_test[:1000])
labels = y_test[:1000]

pca_result = PCA(n_components=2).fit_transform(features)
tsne_result = TSNE(n_components=2, random_state=42).fit_transform(features)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.scatter(pca_result[:, 0], pca_result[:, 1], c=labels, cmap='tab10', alpha=0.6)
ax1.set_title('PCA Visualization')
ax1.set_xlabel('PC1')
ax1.set_ylabel('PC2')

ax2.scatter(tsne_result[:, 0], tsne_result[:, 1], c=labels, cmap='tab10', alpha=0.6)
ax2.set_title('t-SNE Visualization')
ax2.set_xlabel('t-SNE 1')
ax2.set_ylabel('t-SNE 2')

plt.tight_layout()
plt.show()
```

## 參考資源

- https://www.google.com/search?q=Keras+model+visualization+plot_model+summary+2019
- https://www.google.com/search?q=neural+network+weight+distribution+histogram+2019
- https://www.google.com/search?q=t-SNE+feature+visualization+neural+network+2019