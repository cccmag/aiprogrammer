use mini_dl::*;

fn main() {
    println!("=== mini-dl: Deep Learning from Scratch in Rust ===\n");

    // Generate spiral dataset: 100 points per class, 3 classes
    let n = 100;
    let (x, y) = make_spiral_data(n);
    let n_total = n * 3;
    println!("Dataset: {n_total} samples, input_dim=2, classes=3");

    // Model: 2 -> 32 -> 3
    let l1 = Linear::new(2, 32);
    let l2 = Linear::new(32, 3);
    let sgd = SGD::new(
        vec![l1.w.clone(), l1.b.clone(), l2.w.clone(), l2.b.clone()],
        0.5,
    );

    let epochs = 1000;
    for epoch in 0..epochs {
        let (h, a, logits, loss) = forward_two_layer(&x, &l1, &l2, &y);
        let loss_val = loss.borrow().data[0];
        let acc = accuracy(&softmax(&logits), &y);

        let grads = backward_two_layer(&x, &h, &a, &l1, &l2, &logits, &y);
        sgd.step(&grads);

        if epoch % 100 == 0 || epoch == epochs - 1 {
            println!("epoch {:3}  loss={:.6}  acc={:.2}%", epoch, loss_val, acc * 100.0);
        }
    }

    println!("\n=== training completed ===");
}
