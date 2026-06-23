use std::f32;

// ---- Tensor ----

#[derive(Clone, Debug)]
pub struct Tensor {
    pub data: Vec<f32>,
    pub shape: Vec<usize>,
}

impl Tensor {
    pub fn new(data: Vec<f32>, shape: Vec<usize>) -> Self {
        let expected: usize = shape.iter().product();
        assert_eq!(data.len(), expected, "data length mismatch shape");
        Tensor { data, shape }
    }

    pub fn zeros(shape: &[usize]) -> Self {
        let len: usize = shape.iter().product();
        Tensor { data: vec![0.0; len], shape: shape.to_vec() }
    }

    pub fn rows(&self) -> usize {
        *self.shape.first().unwrap_or(&0)
    }

    pub fn cols(&self) -> usize {
        *self.shape.get(1).unwrap_or(&0)
    }

    pub fn matmul(&self, other: &Tensor) -> Tensor {
        let m = self.rows();
        let n = self.cols();
        assert_eq!(n, other.rows(), "matmul dimension mismatch");
        let p = other.cols();
        let mut data = vec![0.0f32; m * p];
        for i in 0..m {
            for k in 0..n {
                let aik = self.data[i * n + k];
                for j in 0..p {
                    data[i * p + j] += aik * other.data[k * p + j];
                }
            }
        }
        Tensor::new(data, vec![m, p])
    }

    pub fn add(&self, other: &Tensor) -> Tensor {
        assert_eq!(self.shape, other.shape, "add shape mismatch");
        let data = self.data.iter().zip(&other.data).map(|(a, b)| a + b).collect();
        Tensor::new(data, self.shape.clone())
    }

    pub fn sub(&self, other: &Tensor) -> Tensor {
        assert_eq!(self.shape, other.shape, "sub shape mismatch");
        let data = self.data.iter().zip(&other.data).map(|(a, b)| a - b).collect();
        Tensor::new(data, self.shape.clone())
    }

    pub fn neg(&self) -> Tensor {
        let data = self.data.iter().map(|x| -x).collect();
        Tensor::new(data, self.shape.clone())
    }

    pub fn transpose(&self) -> Tensor {
        let rows = self.rows();
        let cols = self.cols();
        let mut data = vec![0.0f32; rows * cols];
        for i in 0..rows {
            for j in 0..cols {
                data[j * rows + i] = self.data[i * cols + j];
            }
        }
        Tensor::new(data, vec![cols, rows])
    }

    pub fn sum(&self, dim: usize) -> Tensor {
        let n = self.shape[dim];
        let outer: usize = self.shape[..dim].iter().product();
        let inner: usize = self.shape[dim + 1..].iter().product();
        let mut data = vec![0.0f32; outer * inner];
        for i in 0..outer {
            for j in 0..inner {
                let mut s = 0.0;
                for k in 0..n {
                    s += self.data[i * n * inner + k * inner + j];
                }
                data[i * inner + j] = s;
            }
        }
        let mut new_shape = self.shape.clone();
        new_shape.remove(dim);
        Tensor::new(data, new_shape)
    }
}

// ---- Activation functions ----

pub fn relu(t: &Tensor) -> Tensor {
    let data = t.data.iter().map(|&x| x.max(0.0)).collect();
    Tensor::new(data, t.shape.clone())
}

pub fn sigmoid(t: &Tensor) -> Tensor {
    let data = t.data.iter().map(|&x| 1.0 / (1.0 + f32::consts::E.powf(-x))).collect();
    Tensor::new(data, t.shape.clone())
}

pub fn softmax(t: &Tensor) -> Tensor {
    let n = t.cols();
    let m = t.rows();
    let mut data = vec![0.0f32; m * n];
    for i in 0..m {
        let row_start = i * n;
        let max_val = t.data[row_start..row_start + n]
            .iter().cloned().fold(f32::NEG_INFINITY, f32::max);
        let mut sum = 0.0;
        for j in 0..n {
            let v = (t.data[row_start + j] - max_val).exp();
            data[row_start + j] = v;
            sum += v;
        }
        for j in 0..n {
            data[row_start + j] /= sum;
        }
    }
    Tensor::new(data, t.shape.clone())
}

// ---- Linear layer ----

#[derive(Clone, Debug)]
pub struct Linear {
    pub weight: Tensor,
    pub bias: Tensor,
}

impl Linear {
    pub fn new(in_features: usize, out_features: usize) -> Self {
        let scale = (1.0 / in_features as f32).sqrt();
        let mut rng_data = vec![0.0f32; in_features * out_features];
        for v in &mut rng_data {
            *v = (std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos() as f32
                * 0.0001).fract() * 2.0 * scale - scale;
        }
        Linear {
            weight: Tensor::new(rng_data, vec![out_features, in_features]),
            bias: Tensor::zeros(&[out_features]),
        }
    }

    pub fn from_weights(weight_data: Vec<f32>, bias_data: Vec<f32>,
                        in_features: usize, out_features: usize) -> Self {
        Linear {
            weight: Tensor::new(weight_data, vec![out_features, in_features]),
            bias: Tensor::new(bias_data, vec![out_features]),
        }
    }

    pub fn forward(&self, input: &Tensor) -> Tensor {
        assert_eq!(input.cols(), self.weight.cols(),
            "input features mismatch: expected {}, got {}",
            self.weight.cols(), input.cols());
        let z = input.matmul(&self.weight.transpose());
        let mut data = Vec::with_capacity(z.data.len());
        let n = z.cols();
        for (i, val) in z.data.iter().enumerate() {
            data.push(val + self.bias.data[i % n]);
        }
        Tensor::new(data, z.shape.clone())
    }
}

// ---- MLP (2-layer network) ----

#[derive(Clone, Debug)]
pub struct Mlp {
    pub fc1: Linear,
    pub fc2: Linear,
}

impl Mlp {
    pub fn new(input_size: usize, hidden_size: usize, output_size: usize) -> Self {
        Mlp {
            fc1: Linear::new(input_size, hidden_size),
            fc2: Linear::new(hidden_size, output_size),
        }
    }

    pub fn from_weights(
        w1: Vec<f32>, b1: Vec<f32>,
        w2: Vec<f32>, b2: Vec<f32>,
        input_size: usize, hidden_size: usize, output_size: usize,
    ) -> Self {
        Mlp {
            fc1: Linear::from_weights(w1, b1, input_size, hidden_size),
            fc2: Linear::from_weights(w2, b2, hidden_size, output_size),
        }
    }

    pub fn predict(&self, input: &Tensor) -> Tensor {
        let h = relu(&self.fc1.forward(input));
        let logits = self.fc2.forward(&h);
        softmax(&logits)
    }
}

// ---- Loss functions ----

pub fn cross_entropy_loss(predictions: &Tensor, targets: &Tensor) -> f32 {
    let n = predictions.rows();
    let mut loss = 0.0;
    for i in 0..n {
        for j in 0..predictions.cols() {
            let p = predictions.data[i * predictions.cols() + j];
            let t = targets.data[i * predictions.cols() + j];
            loss -= t * (p + 1e-8).ln();
        }
    }
    loss / n as f32
}

// ---- Data utilities ----

pub fn argmax(t: &Tensor) -> Vec<usize> {
    let n = t.cols();
    let m = t.rows();
    let mut result = Vec::with_capacity(m);
    for i in 0..m {
        let row_start = i * n;
        let max_idx = (0..n).max_by(|&a, &b|
            t.data[row_start + a].partial_cmp(&t.data[row_start + b]).unwrap()
        ).unwrap();
        result.push(max_idx);
    }
    result
}

pub fn one_hot(labels: &[usize], num_classes: usize) -> Tensor {
    let mut data = vec![0.0f32; labels.len() * num_classes];
    for (i, &label) in labels.iter().enumerate() {
        assert!(label < num_classes, "label out of range");
        data[i * num_classes + label] = 1.0;
    }
    Tensor::new(data, vec![labels.len(), num_classes])
}

// ---- Pre-trained XOR model ----
//
// 2 input → 4 hidden (relu) → 2 output (softmax)
// w1 shape: [4, 2], b1: [4]
// w2 shape: [2, 4], b2: [2]

pub fn xor_model() -> Mlp {
    let w1 = vec![
         1.0,  1.0,
        -1.0, -1.0,
         1.0, -1.0,
        -1.0,  1.0,
    ];
    let b1 = vec![-1.5, 0.5, 0.0, 0.0];
    let w2 = vec![
         1.0,  1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,  1.0,
    ];
    let b2 = vec![0.0, 0.0];
    Mlp::from_weights(w1, b1, w2, b2, 2, 4, 2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tensor_creation() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]);
        assert_eq!(t.rows(), 2);
        assert_eq!(t.cols(), 2);
    }

    #[test]
    fn test_matmul() {
        let a = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]);
        let b = Tensor::new(vec![5.0, 6.0, 7.0, 8.0], vec![2, 2]);
        let c = a.matmul(&b);
        assert_eq!(c.data, vec![19.0, 22.0, 43.0, 50.0]);
    }

    #[test]
    fn test_matmul_non_square() {
        let a = Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]);
        let b = Tensor::new(vec![7.0, 8.0, 9.0, 10.0, 11.0, 12.0], vec![3, 2]);
        let c = a.matmul(&b);
        assert_eq!(c.shape, vec![2, 2]);
        assert!((c.data[0] - 58.0).abs() < 1e-5, "c[0] = {}", c.data[0]);
        assert!((c.data[1] - 64.0).abs() < 1e-5, "c[1] = {}", c.data[1]);
        assert!((c.data[2] - 139.0).abs() < 1e-5, "c[2] = {}", c.data[2]);
        assert!((c.data[3] - 154.0).abs() < 1e-5, "c[3] = {}", c.data[3]);
    }

    #[test]
    fn test_relu() {
        let t = Tensor::new(vec![-1.0, 0.0, 1.0, -2.0], vec![4]);
        let r = relu(&t);
        assert_eq!(r.data, vec![0.0, 0.0, 1.0, 0.0]);
    }

    #[test]
    fn test_sigmoid() {
        let t = Tensor::new(vec![0.0], vec![1]);
        let s = sigmoid(&t);
        assert!((s.data[0] - 0.5).abs() < 1e-5);
    }

    #[test]
    fn test_softmax() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 1.0, 2.0, 3.0], vec![2, 3]);
        let s = softmax(&t);
        assert!((s.data[0] + s.data[1] + s.data[2] - 1.0).abs() < 1e-5);
        assert!((s.data[3] + s.data[4] + s.data[5] - 1.0).abs() < 1e-5);
    }

    #[test]
    fn test_linear_forward() {
        let linear = Linear::new(4, 2);
        let input = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![1, 4]);
        let output = linear.forward(&input);
        assert_eq!(output.shape, vec![1, 2]);
    }

    #[test]
    fn test_xor_prediction() {
        let model = xor_model();

        let test_cases = vec![
            (vec![0.0, 0.0], 0),
            (vec![0.0, 1.0], 1),
            (vec![1.0, 0.0], 1),
            (vec![1.0, 1.0], 0),
        ];

        for (input_data, expected) in test_cases {
            let input = Tensor::new(input_data.clone(), vec![1, 2]);
            let output = model.predict(&input);
            let predicted = argmax(&output)[0];
            assert_eq!(predicted, expected,
                "XOR({:?}) expected {} got {}", input_data, expected, predicted);
        }
    }

    #[test]
    fn test_cross_entropy() {
        let pred = Tensor::new(vec![0.7, 0.3, 0.2, 0.8], vec![2, 2]);
        let target = Tensor::new(vec![1.0, 0.0, 0.0, 1.0], vec![2, 2]);
        let loss = cross_entropy_loss(&pred, &target);
        assert!(loss > 0.0);
    }

    #[test]
    fn test_one_hot() {
        let t = one_hot(&[0, 1, 2, 1], 3);
        assert_eq!(t.shape, vec![4, 3]);
        assert_eq!(t.data, vec![
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            0.0, 1.0, 0.0,
        ]);
    }

    #[test]
    fn test_tensor_sum() {
        let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]);
        let s = t.sum(0);
        assert_eq!(s.data, vec![4.0, 6.0]);
        assert_eq!(s.shape, vec![2]);
    }

    #[test]
    fn test_batch_inference() {
        let model = xor_model();
        let batch = Tensor::new(vec![
            0.0, 0.0,
            0.0, 1.0,
            1.0, 0.0,
            1.0, 1.0,
        ], vec![4, 2]);
        let outputs = model.predict(&batch);
        let predictions = argmax(&outputs);
        assert_eq!(predictions, vec![0, 1, 1, 0]);
    }
}
