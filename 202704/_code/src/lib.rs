use std::cell::RefCell;
use std::rc::Rc;

// ---- Tensor ----

#[derive(Clone)]
pub struct TensorData {
    pub data: Vec<f32>,
    pub shape: Vec<usize>,
    pub grad: Option<Vec<f32>>,
}

pub type SharedTensor = Rc<RefCell<TensorData>>;

pub fn tensor(data: Vec<f32>, shape: Vec<usize>) -> SharedTensor {
    Rc::new(RefCell::new(TensorData {
        data,
        shape,
        grad: None,
    }))
}

pub fn zeros(shape: &[usize]) -> SharedTensor {
    let len: usize = shape.iter().product();
    tensor(vec![0.0; len], shape.to_vec())
}

pub fn randn(shape: &[usize]) -> SharedTensor {
    use std::f32::consts::PI;
    let len: usize = shape.iter().product();
    // Box-Muller transform for normal distribution
    let mut rng = 42u32;
    let data: Vec<f32> = (0..len)
        .map(|_i| {
            rng = rng.wrapping_mul(1_103_515_245).wrapping_add(12_345);
            let u1 = (rng as f32) / (u32::MAX as f32);
            rng = rng.wrapping_mul(1_103_515_245).wrapping_add(12_345);
            let u2 = (rng as f32) / (u32::MAX as f32);
            ((-2.0 * u1.ln()).sqrt() * (2.0 * PI * u2).cos()) * 0.1
        })
        .collect();
    tensor(data, shape.to_vec())
}

// ---- Basic ops ----

pub fn matmul(a: &SharedTensor, b: &SharedTensor) -> SharedTensor {
    let a = a.borrow();
    let b = b.borrow();
    assert_eq!(a.shape.len(), 2);
    assert_eq!(b.shape.len(), 2);
    assert_eq!(a.shape[1], b.shape[0]);

    let m = a.shape[0];
    let k = a.shape[1];
    let n = b.shape[1];
    let mut result = vec![0.0; m * n];

    for i in 0..m {
        for j in 0..n {
            let mut sum = 0.0;
            for t in 0..k {
                sum += a.data[i * k + t] * b.data[t * n + j];
            }
            result[i * n + j] = sum;
        }
    }

    tensor(result, vec![m, n])
}

pub fn add(a: &SharedTensor, b: &SharedTensor) -> SharedTensor {
    let a = a.borrow();
    let b = b.borrow();
    let data: Vec<f32> = if a.shape == b.shape {
        a.data.iter().zip(b.data.iter()).map(|(x, y)| x + y).collect()
    } else if a.shape.len() == 2 && b.shape.len() == 2 && a.shape[0] == b.shape[0] {
        a.data.iter().zip(b.data.iter()).map(|(x, y)| x + y).collect()
    } else if a.shape.len() == 2 && b.shape.len() == 2 && b.shape[0] == 1 && b.shape[1] == a.shape[1] {
        // Broadcasting bias: a is (n, d), b is (1, d)
        a.data.iter().enumerate().map(|(i, x)| {
            let col = i % a.shape[1];
            x + b.data[col]
        }).collect()
    } else {
        panic!("add shape mismatch: {:?} vs {:?}", a.shape, b.shape);
    };
    tensor(data, a.shape.clone())
}

pub fn sub(a: &SharedTensor, b: &SharedTensor) -> SharedTensor {
    let a = a.borrow();
    let b = b.borrow();
    assert_eq!(a.shape, b.shape);
    let data: Vec<f32> = a.data.iter().zip(b.data.iter()).map(|(x, y)| x - y).collect();
    tensor(data, a.shape.clone())
}

pub fn mul(a: &SharedTensor, b: &SharedTensor) -> SharedTensor {
    let a = a.borrow();
    let b = b.borrow();
    assert_eq!(a.shape, b.shape);
    let data: Vec<f32> = a.data.iter().zip(b.data.iter()).map(|(x, y)| x * y).collect();
    tensor(data, a.shape.clone())
}

pub fn scale(t: &SharedTensor, s: f32) -> SharedTensor {
    let t = t.borrow();
    let data: Vec<f32> = t.data.iter().map(|x| x * s).collect();
    tensor(data, t.shape.clone())
}

// ---- Activations ----

pub fn relu(t: &SharedTensor) -> SharedTensor {
    let t = t.borrow();
    let data: Vec<f32> = t.data.iter().map(|x| x.max(0.0)).collect();
    tensor(data, t.shape.clone())
}

pub fn softmax(t: &SharedTensor) -> SharedTensor {
    let t = t.borrow();
    let n = t.shape[0];
    let c = t.shape[1];
    let mut data = vec![0.0; n * c];
    for i in 0..n {
        let row_start = i * c;
        let max_val = t.data[row_start..row_start + c]
            .iter()
            .cloned()
            .fold(f32::NEG_INFINITY, f32::max);
        let mut sum = 0.0;
        for j in 0..c {
            let e = (t.data[row_start + j] - max_val).exp();
            data[row_start + j] = e;
            sum += e;
        }
        for j in 0..c {
            data[row_start + j] /= sum;
        }
    }
    tensor(data, t.shape.clone())
}

// ---- Loss ----

pub fn cross_entropy_loss(pred: &SharedTensor, target: &SharedTensor) -> SharedTensor {
    let pred = pred.borrow();
    let target = target.borrow();
    assert_eq!(pred.shape, target.shape);
    let n = pred.shape[0];
    let c = pred.shape[1];
    let mut loss = 0.0;
    for i in 0..n {
        for j in 0..c {
            let t = target.data[i * c + j];
            if t > 0.5 {
                loss -= (pred.data[i * c + j].max(1e-7)).ln();
            }
        }
    }
    tensor(vec![loss / n as f32], vec![1])
}

// ---- Layer ----

pub struct Linear {
    pub w: SharedTensor,
    pub b: SharedTensor,
}

impl Linear {
    pub fn new(in_features: usize, out_features: usize) -> Self {
        Linear {
            w: randn(&[in_features, out_features]),
            b: zeros(&[1, out_features]),
        }
    }

    pub fn forward(&self, x: &SharedTensor) -> SharedTensor {
        let z = matmul(x, &self.w);
        add(&z, &self.b)
    }

    pub fn params(&self) -> Vec<SharedTensor> {
        vec![self.w.clone(), self.b.clone()]
    }
}

// ---- Optimizer ----

pub struct SGD {
    params: Vec<SharedTensor>,
    lr: f32,
}

impl SGD {
    pub fn new(params: Vec<SharedTensor>, lr: f32) -> Self {
        SGD { params, lr }
    }

    pub fn step(&self, grads: &[Vec<f32>]) {
        for (param, grad) in self.params.iter().zip(grads.iter()) {
            let mut param = param.borrow_mut();
            assert_eq!(param.data.len(), grad.len());
            for i in 0..param.data.len() {
                param.data[i] -= self.lr * grad[i];
            }
        }
    }
}

// ---- Manual gradients for a 2-layer net (cross-entropy + softmax) ----

/// Compute forward pass and return (h, a, logits, loss)
pub fn forward_two_layer(
    x: &SharedTensor,
    l1: &Linear,
    l2: &Linear,
    target: &SharedTensor,
) -> (SharedTensor, SharedTensor, SharedTensor, SharedTensor) {
    let h = l1.forward(x);            // h = x@w1 + b1
    let a = relu(&h);                 // a = relu(h)
    let logits = l2.forward(&a);      // logits = a@w2 + b2
    let loss = cross_entropy_loss(&softmax(&logits), target);
    (h, a, logits, loss)
}

/// Manual backward pass for 2-layer net: softmax + cross-entropy
pub fn backward_two_layer(
    x: &SharedTensor,
    h: &SharedTensor,
    a: &SharedTensor,
    _l1: &Linear,
    l2: &Linear,
    logits: &SharedTensor,
    target: &SharedTensor,
) -> [Vec<f32>; 4] {
    let x = x.borrow();
    let h = h.borrow();
    let a = a.borrow();
    let target = target.borrow();
    let logits = logits.borrow();
    let w2 = l2.w.borrow();

    let n = x.shape[0];
    let d = x.shape[1];
    let h_dim = w2.shape[0];
    let c = w2.shape[1];

    // Softmax of logits
    let mut soft = vec![0.0; n * c];
    for i in 0..n {
        let row_start = i * c;
        let max_val = logits.data[row_start..row_start + c]
            .iter()
            .cloned()
            .fold(f32::NEG_INFINITY, f32::max);
        let mut sum = 0.0;
        for j in 0..c {
            let e = (logits.data[row_start + j] - max_val).exp();
            soft[row_start + j] = e;
            sum += e;
        }
        for j in 0..c {
            soft[row_start + j] /= sum;
        }
    }

    // dL/dlogits = (softmax - target) / n
    let mut dlogits = vec![0.0; n * c];
    for i in 0..n {
        for j in 0..c {
            dlogits[i * c + j] = (soft[i * c + j] - target.data[i * c + j]) / n as f32;
        }
    }

    // dL/dw2 = a^T @ dlogits
    let mut dw2 = vec![0.0; h_dim * c];
    for i in 0..h_dim {
        for j in 0..c {
            let mut sum = 0.0;
            for k in 0..n {
                sum += a.data[k * h_dim + i] * dlogits[k * c + j];
            }
            dw2[i * c + j] = sum;
        }
    }

    // db2 = sum(dlogits, axis=0)
    let mut db2 = vec![0.0; c];
    for i in 0..n {
        for j in 0..c {
            db2[j] += dlogits[i * c + j];
        }
    }

    // dL/da = dlogits @ w2^T
    let mut da = vec![0.0; n * h_dim];
    for i in 0..n {
        for j in 0..h_dim {
            let mut sum = 0.0;
            for k in 0..c {
                sum += dlogits[i * c + k] * w2.data[j * c + k];
            }
            da[i * h_dim + j] = sum;
        }
    }

    // dL/dh = da * (h > 0)  (ReLU backward with pre-activation h)
    let mut dh = vec![0.0; n * h_dim];
    for i in 0..n * h_dim {
        dh[i] = if h.data[i] > 0.0 { da[i] } else { 0.0 };
    }

    // dL/dw1 = x^T @ dh
    let mut dw1 = vec![0.0; d * h_dim];
    for i in 0..d {
        for j in 0..h_dim {
            let mut sum = 0.0;
            for k in 0..n {
                sum += x.data[k * d + i] * dh[k * h_dim + j];
            }
            dw1[i * h_dim + j] = sum;
        }
    }

    // db1 = sum(dh, axis=0)
    let mut db1 = vec![0.0; h_dim];
    for i in 0..n {
        for j in 0..h_dim {
            db1[j] += dh[i * h_dim + j];
        }
    }

    [dw1, db1, dw2, db2]
}

// ---- Accuracy ----

pub fn accuracy(pred: &SharedTensor, target: &SharedTensor) -> f32 {
    let pred = pred.borrow();
    let target = target.borrow();
    let n = pred.shape[0];
    let c = pred.shape[1];
    let mut correct = 0;
    for i in 0..n {
        let pred_class = (0..c)
            .max_by(|&a, &b| pred.data[i * c + a].partial_cmp(&pred.data[i * c + b]).unwrap())
            .unwrap();
        let target_class = (0..c)
            .max_by(|&a, &b| target.data[i * c + a].partial_cmp(&target.data[i * c + b]).unwrap())
            .unwrap();
        if pred_class == target_class {
            correct += 1;
        }
    }
    correct as f32 / n as f32
}

// ---- Data generation ----

pub fn make_spiral_data(n: usize) -> (SharedTensor, SharedTensor) {
    let mut x = Vec::with_capacity(n * 3 * 2);
    let mut y = Vec::with_capacity(n * 3 * 3);
    let mut rng = 12345u32;

    for class in 0..3 {
        let r_start = class as f32 * 4.0;
        for i in 0..n {
            let frac = i as f32 / n as f32;
            let angle = frac * 4.0 * std::f32::consts::PI + r_start;
            let radius = 0.5 + frac * 0.8;
            let noise_x = (rng as f32 / u32::MAX as f32 - 0.5) * 0.05;
            rng = rng.wrapping_mul(1103515245).wrapping_add(12345);
            let noise_y = (rng as f32 / u32::MAX as f32 - 0.5) * 0.05;
            rng = rng.wrapping_mul(1103515245).wrapping_add(12345);
            x.push(radius * angle.cos() + noise_x);
            x.push(radius * angle.sin() + noise_y);
            for c in 0..3 {
                y.push(if c == class { 1.0 } else { 0.0 });
            }
        }
    }
    (tensor(x, vec![n * 3, 2]), tensor(y, vec![n * 3, 3]))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tensor_creation() {
        let t = tensor(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]);
        assert_eq!(t.borrow().shape, vec![2, 2]);
        assert_eq!(t.borrow().data[0], 1.0);
    }

    #[test]
    fn test_matmul() {
        let a = tensor(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]);
        let b = tensor(vec![5.0, 6.0, 7.0, 8.0], vec![2, 2]);
        let c = matmul(&a, &b);
        let c = c.borrow();
        assert!((c.data[0] - 19.0).abs() < 1e-6);
        assert!((c.data[1] - 22.0).abs() < 1e-6);
        assert!((c.data[2] - 43.0).abs() < 1e-6);
        assert!((c.data[3] - 50.0).abs() < 1e-6);
    }

    #[test]
    fn test_relu() {
        let t = tensor(vec![-1.0, 0.0, 2.0, -3.0], vec![4]);
        let r = relu(&t);
        let r = r.borrow();
        assert_eq!(r.data, vec![0.0, 0.0, 2.0, 0.0]);
    }

    #[test]
    fn test_softmax() {
        let t = tensor(vec![1.0, 2.0, 3.0], vec![1, 3]);
        let s = softmax(&t);
        let s = s.borrow();
        let sum: f32 = s.data.iter().sum();
        assert!((sum - 1.0).abs() < 1e-6);
    }

    #[test]
    fn test_linear_forward() {
        let layer = Linear::new(3, 2);
        let x = tensor(vec![1.0, 2.0, 3.0], vec![1, 3]);
        let out = layer.forward(&x);
        assert_eq!(out.borrow().shape, vec![1, 2]);
    }

    #[test]
    fn test_training_step() {
        let n = 10;
        let (x, y) = make_spiral_data(n);
        let l1 = Linear::new(2, 16);
        let l2 = Linear::new(16, 3);
        let sgd = SGD::new(vec![l1.w.clone(), l1.b.clone(), l2.w.clone(), l2.b.clone()], 0.1);

        let (h, a, logits, loss) = forward_two_layer(&x, &l1, &l2, &y);
        let loss_val = loss.borrow().data[0];

        let grads = backward_two_layer(&x, &h, &a, &l1, &l2, &logits, &y);
        sgd.step(&grads);

        let (_, _, _, new_loss) = forward_two_layer(&x, &l1, &l2, &y);
        let new_loss_val = new_loss.borrow().data[0];

        // Loss should decrease after step
        assert!(
            new_loss_val < loss_val + 0.01,
            "loss improved {loss_val} -> {new_loss_val}"
        );
    }

    #[test]
    fn test_accuracy() {
        let pred = tensor(vec![0.8, 0.1, 0.1, 0.2, 0.7, 0.1], vec![2, 3]);
        let target = tensor(vec![1.0, 0.0, 0.0, 0.0, 1.0, 0.0], vec![2, 3]);
        let acc = accuracy(&pred, &target);
        assert!((acc - 1.0).abs() < 1e-6);
    }

    #[test]
    fn test_spiral_data_shape() {
        let (x, y) = make_spiral_data(5);
        assert_eq!(x.borrow().shape, vec![15, 2]);
        assert_eq!(y.borrow().shape, vec![15, 3]);
    }
}
