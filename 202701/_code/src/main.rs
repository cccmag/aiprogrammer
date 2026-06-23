use mini_ml::*;

fn main() {
    println!("=== mini-ml: ML Inference Engine Demo ===\n");

    println!("--- tensor operations ---");
    let a = Tensor::new(vec![1.0, 2.0, 3.0, 4.0], vec![2, 2]);
    let b = Tensor::new(vec![5.0, 6.0, 7.0, 8.0], vec![2, 2]);
    let c = a.matmul(&b);
    println!("  matmul:  [{:>4}, {:>4}]", c.data[0], c.data[1]);
    println!("           [{:>4}, {:>4}]", c.data[2], c.data[3]);

    let t = Tensor::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], vec![2, 3]);
    let tt = t.transpose();
    println!("  transpose: shape [{}, {}]", tt.rows(), tt.cols());

    println!("\n--- activation functions ---");
    let x = Tensor::new(vec![-2.0, -1.0, 0.0, 1.0, 2.0], vec![5]);
    let r = relu(&x);
    let s = sigmoid(&x);
    println!("  x:        {:?}", x.data);
    println!("  relu(x):  {:?}", r.data);
    println!("  sigmoid:  {:?}", s.data);

    println!("\n--- softmax ---");
    let logits = Tensor::new(vec![2.0, 1.0, 0.1], vec![1, 3]);
    let probs = softmax(&logits);
    println!("  logits:  {:?}", logits.data);
    println!("  probs:   {:?}", probs.data);
    println!("  sum:     {}", probs.data.iter().sum::<f32>());

    println!("\n--- linear layer ---");
    let linear = Linear::new(4, 3);
    let input = Tensor::new(vec![0.5, -0.3, 0.8, 0.1], vec![1, 4]);
    let out = linear.forward(&input);
    println!("  input(4) -> linear -> output(3): {:?}", out.data);
    let r_out = relu(&out);
    println!("  after relu: {:?}", r_out.data);

    println!("\n--- XOR model inference ---");
    let model = xor_model();

    let inputs = vec![
        (vec![0.0, 0.0], 0),
        (vec![0.0, 1.0], 1),
        (vec![1.0, 0.0], 1),
        (vec![1.0, 1.0], 0),
    ];

    for (data, expected) in &inputs {
        let input = Tensor::new(data.clone(), vec![1, 2]);
        let output = model.predict(&input);
        let predicted = argmax(&output)[0];
        let confidence = output.data.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
        let correct = if predicted == *expected { "✓" } else { "✗" };
        println!("  XOR({:>4}, {:>4}) -> {} (conf: {:.4}) {}",
            data[0], data[1], predicted, confidence, correct);
    }

    println!("\n--- batch inference ---");
    let batch = Tensor::new(vec![
        0.0, 0.0,
        0.0, 1.0,
        1.0, 0.0,
        1.0, 1.0,
    ], vec![4, 2]);
    let outputs = model.predict(&batch);
    let predictions = argmax(&outputs);
    println!("  batch predictions: {:?}", predictions);

    println!("\n--- cross-entropy loss ---");
    let pred = Tensor::new(vec![0.8, 0.2, 0.3, 0.7], vec![2, 2]);
    let target = Tensor::new(vec![1.0, 0.0, 0.0, 1.0], vec![2, 2]);
    let loss = cross_entropy_loss(&pred, &target);
    println!("  loss: {:.6}", loss);

    println!("\n=== demo completed ===");
}
