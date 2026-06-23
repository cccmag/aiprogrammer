// ---- WASM-compatible computation kernel ----
//
// All functions here are designed to compile under
// wasm32-unknown-unknown with no_std if needed.
// In native builds they work as regular Rust functions.

const PAGE_SIZE: usize = 65536;

static mut LINEAR_MEMORY: [u8; PAGE_SIZE] = [0u8; PAGE_SIZE];

pub fn memory_read(offset: usize, len: usize) -> Vec<u8> {
    assert!(offset + len <= PAGE_SIZE, "WASM memory read out of bounds");
    let mut out = vec![0u8; len];
    unsafe {
        out.copy_from_slice(&LINEAR_MEMORY[offset..offset + len]);
    }
    out
}

pub fn memory_write(offset: usize, data: &[u8]) {
    assert!(offset + data.len() <= PAGE_SIZE, "WASM memory write out of bounds");
    unsafe {
        LINEAR_MEMORY[offset..offset + data.len()].copy_from_slice(data);
    }
}

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

pub fn factorial(n: u32) -> u64 {
    (1..=n).fold(1u64, |acc, x| acc * x as u64)
}

pub fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let (mut a, mut b) = (0u64, 1u64);
            for _ in 2..=n {
                let next = a + b;
                a = b;
                b = next;
            }
            b
        }
    }
}

pub fn is_prime(n: u32) -> bool {
    if n < 2 {
        return false;
    }
    if n % 2 == 0 {
        return n == 2;
    }
    let mut i = 3u32;
    while i * i <= n {
        if n % i == 0 {
            return false;
        }
        i += 2;
    }
    true
}

pub fn dot_product(a: &[f64], b: &[f64]) -> f64 {
    assert_eq!(a.len(), b.len(), "vectors must have same length");
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

pub fn matrix_multiply(a: &[f64], b: &[f64], m: usize, n: usize, p: usize) -> Vec<f64> {
    assert_eq!(a.len(), m * n, "matrix A dimensions mismatch");
    assert_eq!(b.len(), n * p, "matrix B dimensions mismatch");
    let mut result = vec![0.0f64; m * p];
    for i in 0..m {
        for k in 0..n {
            let aik = a[i * n + k];
            for j in 0..p {
                result[i * p + j] += aik * b[k * p + j];
            }
        }
    }
    result
}

pub fn grayscale(pixels: &[u8]) -> Vec<u8> {
    assert_eq!(pixels.len() % 4, 0, "expected RGBA pixel data");
    pixels
        .chunks_exact(4)
        .map(|rgba| {
            let r = rgba[0] as u32;
            let g = rgba[1] as u32;
            let b = rgba[2] as u32;
            let gray = (r * 77 + g * 150 + b * 29) / 256;
            [gray as u8, gray as u8, gray as u8, rgba[3]]
        })
        .flatten()
        .collect()
}

pub fn brightness(pixels: &[u8], delta: i32) -> Vec<u8> {
    assert_eq!(pixels.len() % 4, 0, "expected RGBA pixel data");
    pixels
        .chunks_exact(4)
        .map(|rgba| {
            let r = (rgba[0] as i32 + delta).clamp(0, 255) as u8;
            let g = (rgba[1] as i32 + delta).clamp(0, 255) as u8;
            let b = (rgba[2] as i32 + delta).clamp(0, 255) as u8;
            [r, g, b, rgba[3]]
        })
        .flatten()
        .collect()
}

pub fn count_words(text: &str) -> usize {
    text.split_whitespace().count()
}

pub fn base64_encode(data: &[u8]) -> String {
    const CHARS: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut out = Vec::new();
    for chunk in data.chunks(3) {
        let n = chunk.len();
        let mut b = [0u8; 3];
        b[..n].copy_from_slice(chunk);
        let triple = (b[0] as u32) << 16 | (b[1] as u32) << 8 | b[2] as u32;
        out.push(CHARS[((triple >> 18) & 0x3f) as usize]);
        out.push(CHARS[((triple >> 12) & 0x3f) as usize]);
        out.push(if n > 1 { CHARS[((triple >> 6) & 0x3f) as usize] } else { b'=' });
        out.push(if n > 2 { CHARS[(triple & 0x3f) as usize] } else { b'=' });
    }
    String::from_utf8(out).unwrap()
}

fn base64_char_index(c: u8) -> Option<u8> {
    match c {
        b'A'..=b'Z' => Some(c - b'A'),
        b'a'..=b'z' => Some(c - b'a' + 26),
        b'0'..=b'9' => Some(c - b'0' + 52),
        b'+' => Some(62),
        b'/' => Some(63),
        _ => None,
    }
}

pub fn base64_decode(s: &str) -> Result<Vec<u8>, String> {
    let s = s.trim_end_matches('=');
    let bytes: Vec<u8> = s.bytes().collect();
    let mut out = Vec::with_capacity(bytes.len() / 4 * 3);
    for chunk in bytes.chunks(4) {
        let n = chunk.len();
        if n < 2 {
            return Err("invalid base64 input".to_string());
        }
        let mut vals = [0u8; 4];
        for (i, &b) in chunk.iter().enumerate() {
            vals[i] = base64_char_index(b).ok_or_else(|| format!("invalid char '{}'", b as char))?;
        }
        let triple = (vals[0] as u32) << 18 | (vals[1] as u32) << 12
            | (vals[2] as u32) << 6 | vals[3] as u32;
        out.push((triple >> 16) as u8);
        if n > 2 {
            out.push((triple >> 8) as u8);
        }
        if n > 3 {
            out.push(triple as u8);
        }
    }
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
    }

    #[test]
    fn test_factorial() {
        assert_eq!(factorial(0), 1);
        assert_eq!(factorial(5), 120);
        assert_eq!(factorial(10), 3_628_800);
    }

    #[test]
    fn test_fibonacci() {
        assert_eq!(fibonacci(0), 0);
        assert_eq!(fibonacci(1), 1);
        assert_eq!(fibonacci(10), 55);
        assert_eq!(fibonacci(20), 6765);
    }

    #[test]
    fn test_is_prime() {
        assert!(!is_prime(0));
        assert!(!is_prime(1));
        assert!(is_prime(2));
        assert!(is_prime(7));
        assert!(!is_prime(9));
        assert!(is_prime(97));
    }

    #[test]
    fn test_dot_product() {
        let a = vec![1.0, 2.0, 3.0];
        let b = vec![4.0, 5.0, 6.0];
        assert_eq!(dot_product(&a, &b), 32.0);
    }

    #[test]
    fn test_matrix_multiply() {
        let a = vec![1.0, 2.0, 3.0, 4.0];
        let b = vec![5.0, 6.0, 7.0, 8.0];
        let c = matrix_multiply(&a, &b, 2, 2, 2);
        assert_eq!(c, vec![19.0, 22.0, 43.0, 50.0]);
    }

    #[test]
    fn test_grayscale() {
        let rgba = vec![255, 0, 0, 255, 0, 255, 0, 255];
        let gray = grayscale(&rgba);
        assert_eq!(gray.len(), 8);
        assert_eq!(gray[0], gray[1], "R == G for pixel 0");
        assert_eq!(gray[1], gray[2], "G == B for pixel 0");
        assert_eq!(gray[4], gray[5], "R == G for pixel 1");
        assert_eq!(gray[5], gray[6], "G == B for pixel 1");
        assert_eq!(gray[3], 255);
        assert_eq!(gray[7], 255);
    }

    #[test]
    fn test_brightness() {
        let rgba = vec![100, 100, 100, 255];
        let bright = brightness(&rgba, 50);
        assert_eq!(bright[0], 150);
        let dark = brightness(&rgba, -200);
        assert_eq!(dark[0], 0);
        let clamped = brightness(&rgba, 999);
        assert_eq!(clamped[0], 255);
    }

    #[test]
    fn test_count_words() {
        assert_eq!(count_words("hello world"), 2);
        assert_eq!(count_words(""), 0);
        assert_eq!(count_words("a b c d"), 4);
    }

    #[test]
    fn test_base64_roundtrip() {
        let data = b"hello world";
        let encoded = base64_encode(data);
        let decoded = base64_decode(&encoded).unwrap();
        assert_eq!(decoded, data);
    }

    #[test]
    fn test_base64_encode() {
        assert_eq!(base64_encode(b"f"), "Zg==");
        assert_eq!(base64_encode(b"fo"), "Zm8=");
        assert_eq!(base64_encode(b"foo"), "Zm9v");
        assert_eq!(base64_encode(b"foob"), "Zm9vYg==");
    }

    #[test]
    fn test_memory_read_write() {
        let data = b"WASM linear memory";
        memory_write(256, data);
        let read = memory_read(256, data.len());
        assert_eq!(read, data);
    }

    #[test]
    #[should_panic(expected = "WASM memory write out of bounds")]
    fn test_memory_write_oob() {
        memory_write(PAGE_SIZE - 1, b"too big");
    }

    #[test]
    fn test_memory_isolation() {
        memory_write(128, b"hello");
        memory_write(256, b"world");
        let r1 = memory_read(128, 5);
        let r2 = memory_read(256, 5);
        assert_eq!(r1, b"hello");
        assert_eq!(r2, b"world");
    }
}
