use mini_wasm::*;

fn main() {
    println!("=== mini-wasm: WebAssembly Computation Kernel Demo ===\n");

    println!("--- arithmetic ---");
    println!("  add(2, 3)      = {}", add(2, 3));
    println!("  factorial(10)  = {}", factorial(10));
    println!("  fibonacci(20)  = {}", fibonacci(20));
    println!("  is_prime(97)   = {}", is_prime(97));
    println!("  is_prime(100)  = {}", is_prime(100));

    println!("\n--- linear algebra ---");
    let a = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
    let b = vec![7.0, 8.0, 9.0, 10.0, 11.0, 12.0];
    println!("  dot_product    = {}", dot_product(&a[..3], &b[..3]));
    let c = matrix_multiply(&a, &b, 2, 3, 2);
    println!("  matrix (2x2)   = {:?}", c);

    println!("\n--- image processing (simulated RGBA) ---");
    let pixel = vec![100u8, 150, 200, 255];
    let gray = grayscale(&pixel);
    println!("  grayscale      = ({}, {}, {}, {})",
        gray[0], gray[1], gray[2], gray[3]);
    let bright = brightness(&pixel, 80);
    println!("  brightness(+80)= ({}, {}, {}, {})",
        bright[0], bright[1], bright[2], bright[3]);

    println!("\n--- string processing ---");
    println!("  count_words    = {}", count_words("Rust compiles to WebAssembly"));
    let encoded = base64_encode(b"Rust + WASM");
    let decoded = base64_decode(&encoded).unwrap();
    println!("  base64 encode  = {}", encoded);
    println!("  base64 decode  = {}", String::from_utf8_lossy(&decoded));

    println!("\n--- linear memory ---");
    let msg = b"Hello from WASM linear memory!";
    memory_write(0, msg);
    let read = memory_read(0, msg.len());
    println!("  memory[0..{}]   = '{}'", msg.len(), String::from_utf8_lossy(&read));

    println!("\n=== demo completed ===");
}
