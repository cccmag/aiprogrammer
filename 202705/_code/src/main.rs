use wasm_component::*;

fn main() {
    println!("=== WASM Component Model Demo ===\n");

    // Instantiate guest (the WASM component)
    let guest = WasmGuest;

    // Instantiate host (provides imports to the guest)
    let host = ConsoleLogger;

    // Create runtime (simulates wasmtime loading the component)
    let runtime = HostRuntime::new(guest, host);

    // Create input data
    let input = Matrix::new(vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 2, 3);
    let weight = Matrix::new(vec![0.1, 0.2, 0.3, 0.4, 0.5, 0.6], 3, 2);
    let bias = Matrix::new(vec![0.01, 0.02, 0.01, 0.02], 2, 2);

    println!("Input matrix ({}x{}):", input.rows, input.cols);
    println!("{}", input);

    println!("Weight matrix ({}x{}):", weight.rows, weight.cols);
    println!("{}", weight);

    // Run inference pipeline inside the "WASM component"
    match runtime.run_inference(&input, &weight, &bias) {
        Ok(output) => {
            println!("\nOutput matrix ({}x{}):", output.rows, output.cols);
            println!("{}", output);
        }
        Err(e) => {
            eprintln!("Inference failed: {e}");
        }
    }

    // Demonstrate component composition
    println!("\n--- Component Composition ---");
    let comp_a = WasmGuest;
    let comp_b = WasmGuest;
    let pipeline = Pipeline::new(comp_a, comp_b);

    let a = Matrix::new(vec![1.0, 0.0, 0.0, 1.0], 2, 2);
    let b = Matrix::new(vec![4.0, 3.0, 2.0, 1.0], 2, 2);
    let composed = pipeline.compose(&a, &b).unwrap();
    println!("Composed result (identity matmul then relu):\n{}", composed);
}
