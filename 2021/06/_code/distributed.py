import numpy as np

def allreduce(rank, size, values):
    result = values[rank]
    for _ in range(size - 1):
        result += values[(rank + 1) % size]
    return result / size

def ring_allreduce(rank, size, local_gradients):
    accumulated = np.array(local_gradients[rank], dtype=float)

    for step in range(size - 1):
        accumulated = accumulated + local_gradients[(rank + step + 1) % size]

    return accumulated / size

class SimpleModel:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros(layer_sizes[i+1])
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, x):
        self.activations = [x]
        current = x
        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            current = np.dot(current, w) + b
            if i < len(self.weights) - 1:
                current = np.maximum(0, current)
            self.activations.append(current)
        return current

    def backward(self, y_pred, y_true, lr):
        grad = y_pred - y_true

        for i in reversed(range(len(self.weights))):
            grad_w = np.dot(self.activations[i].T, grad)
            grad_b = np.sum(grad, axis=0)

            if i > 0:
                grad = np.dot(grad, self.weights[i].T)
                grad = grad * (self.activations[i] > 0).astype(float)

            self.weights[i] -= lr * grad_w
            self.biases[i] -= lr * grad_b

class GradientCheckpointing:
    def __init__(self, model):
        self.model = model
        self.checkpoint_indices = []

    def set_checkpoints(self, indices):
        self.checkpoint_indices = sorted(indices)

    def forward_with_checkpoint(self, x):
        activations = [x]
        current = x

        for i in range(len(self.model.weights)):
            current = np.dot(current, self.model.weights[i]) + self.model.biases[i]

            if i in self.checkpoint_indices:
                activations.append(current.copy())

            if i < len(self.model.weights) - 1:
                current = np.maximum(0, current)

        return current, activations

    def backward_with_checkpoint(self, y_pred, y_true, activations, lr):
        grad = y_pred - y_true

        for i in reversed(range(len(self.model.weights))):
            grad_w = np.dot(activations[i].T, grad)
            grad_b = np.sum(grad, axis=0)

            if i > 0:
                grad = np.dot(grad, self.model.weights[i].T)
                grad = grad * (activations[i] > 0).astype(float)

            self.model.weights[i] -= lr * grad_w
            self.model.biases[i] -= lr * grad_b

class ZeROStage1Simulator:
    def __init__(self, num_nodes, param_size):
        self.num_nodes = num_nodes
        self.param_size = param_size
        self.shard_size = param_size // num_nodes

    def shard_optimizer_state(self, optimizer_state):
        shards = []
        for i in range(self.num_nodes):
            start = i * self.shard_size
            end = start + self.shard_size
            if i == self.num_nodes - 1:
                end = self.param_size
            shards.append(optimizer_state[start:end])
        return shards

    def update_local_params(self, local_params, local_grads, local_momentum, lr=0.001):
        local_momentum = 0.9 * local_momentum + (1 - 0.9) * local_grads
        local_params = local_params - lr * local_momentum
        return local_params, local_momentum

class DataParallelSimulator:
    def __init__(self, num_gpus, model_size, batch_size):
        self.num_gpus = num_gpus
        self.batch_per_gpu = batch_size // num_gpus
        self.models = []
        for _ in range(num_gpus):
            self.models.append(SimpleModel(model_size))

    def train_step(self, x_data, y_data, lr=0.01):
        local_losses = []

        for gpu_id in range(self.num_gpus):
            start_idx = gpu_id * self.batch_per_gpu
            end_idx = start_idx + self.batch_per_gpu

            x_batch = x_data[start_idx:end_idx]
            y_batch = y_data[start_idx:end_idx]

            y_pred = self.models[gpu_id].forward(x_batch)
            loss = np.mean((y_pred - y_batch) ** 2)

            self.models[gpu_id].backward(y_pred, y_batch, lr)

            local_losses.append(loss)

        avg_loss = np.mean(local_losses)
        print(f"Average loss: {avg_loss:.4f}")
        return avg_loss

def demo():
    np.random.seed(42)

    print("=== AllReduce Demo ===")
    size = 4
    values = [np.array([1.0, 2.0, 3.0]) for _ in range(size)]
    results = [allreduce(r, size, values) for r in range(size)]
    print("AllReduce results:", results[0])

    print("\n=== Ring-AllReduce Demo ===")
    local_grads = [np.array([1.0, 2.0, 3.0]) * (r + 1) for r in range(size)]
    reduced = ring_allreduce(0, size, local_grads)
    print("Ring-AllReduce result at rank 0:", reduced)

    print("\n=== Gradient Checkpointing Demo ===")
    model = SimpleModel([4, 8, 4])
    checkpointing = GradientCheckpointing(model)
    checkpointing.set_checkpoints([1, 3])

    x = np.random.randn(2, 4)
    y_true = np.random.randn(2, 4)

    y_pred, activations = checkpointing.forward_with_checkpoint(x)
    print("Forward with checkpoints")
    print("  Activations stored at indices:", checkpointing.checkpoint_indices)
    print("  Input shape:", activations[0].shape)
    print("  Saved activation shape:", activations[1].shape if len(activations) > 1 else "N/A")
    print("  Output shape:", y_pred.shape)

    print("\n=== ZeRO Stage 1 Simulator ===")
    zero_sim = ZeROStage1Simulator(num_nodes=4, param_size=100)
    optimizer_state = np.random.randn(100) * 0.01
    shards = zero_sim.shard_optimizer_state(optimizer_state)
    print(f"Optimizer state split into {len(shards)} shards, sizes:", [len(s) for s in shards])

    print("\n=== Data Parallel Simulator ===")
    dp_sim = DataParallelSimulator(num_gpus=2, model_size=[4, 8, 4], batch_size=8)
    x_data = np.random.randn(8, 4)
    y_data = np.random.randn(8, 4)

    for step in range(3):
        loss = dp_sim.train_step(x_data, y_data, lr=0.1)

    print("\nDemo OK")

if __name__ == "__main__":
    demo()