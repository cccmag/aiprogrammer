use std::io;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;

static MODULE_LOADED: AtomicBool = AtomicBool::new(false);

struct MiniDriver {
    name: String,
    irq: u32,
    mmio_base: usize,
    mmio_size: usize,
    device_data: Mutex<Vec<u8>>,
    open_count: Mutex<u32>,
}

impl MiniDriver {
    fn new(name: &str, irq: u32, mmio_base: usize, mmio_size: usize) -> Self {
        Self {
            name: name.to_string(),
            irq,
            mmio_base,
            mmio_size,
            device_data: Mutex::new(vec![0u8; 64]),
            open_count: Mutex::new(0),
        }
    }

    fn read_reg(&self, offset: usize) -> u8 {
        assert!(offset < self.mmio_size, "MMIO offset out of bounds");
        let data = self.device_data.lock().unwrap();
        data[offset]
    }

    fn write_reg(&self, offset: usize, value: u8) {
        assert!(offset < self.mmio_size, "MMIO offset out of bounds");
        let mut data = self.device_data.lock().unwrap();
        data[offset] = value;
        println!("  [MMIO]  write 0x{:02x} -> reg[{:#x}]", value, self.mmio_base + offset);
    }

    fn open(&self) -> io::Result<()> {
        let mut count = self.open_count.lock().unwrap();
        *count += 1;
        println!("  [open]  {} (count: {})", self.name, *count);
        Ok(())
    }

    fn close(&self) {
        let mut count = self.open_count.lock().unwrap();
        *count = if *count > 0 { *count - 1 } else { 0 };
        println!("  [close] {} (count: {})", self.name, *count);
    }

    fn read(&self, buf: &mut [u8]) -> io::Result<usize> {
        let data = self.device_data.lock().unwrap();
        let n = buf.len().min(data.len());
        buf[..n].copy_from_slice(&data[..n]);
        println!("  [read]  {} bytes from {}", n, self.name);
        Ok(n)
    }

    fn write(&self, buf: &[u8]) -> io::Result<usize> {
        let mut data = self.device_data.lock().unwrap();
        let n = buf.len().min(data.len());
        data[..n].copy_from_slice(&buf[..n]);
        println!("  [write] {} bytes to {}", n, self.name);
        Ok(n)
    }

    fn ioctl(&self, cmd: u32, _arg: usize) -> io::Result<usize> {
        match cmd {
            0 => {
                println!("  [ioctl] GET_INFO: irq={}, mmio={:#x}", self.irq, self.mmio_base);
                Ok(self.irq as usize)
            }
            1 => {
                println!("  [ioctl] RESET: device reset");
                let mut data = self.device_data.lock().unwrap();
                data.fill(0);
                Ok(0)
            }
            _ => {
                println!("  [ioctl] unknown cmd={}", cmd);
                Err(io::Error::new(io::ErrorKind::InvalidInput, "unknown ioctl"))
            }
        }
    }
}

fn init_module() -> MiniDriver {
    println!("[init] mini-kmod: loading");

    let driver = MiniDriver::new("mini-kmod", 42, 0xf000_0000, 64);

    println!("[init] registered device: {} (irq={}, mmio={:#x})",
        driver.name, driver.irq, driver.mmio_base);

    MODULE_LOADED.store(true, Ordering::SeqCst);
    driver
}

fn cleanup_module(_driver: &MiniDriver) {
    println!("[exit] mini-kmod: unloading");
    MODULE_LOADED.store(false, Ordering::SeqCst);
    println!("[exit] device unregistered");
}

fn simulate_hardware_interrupt(driver: &MiniDriver) {
    println!("\n--- IRQ {}: hardware interrupt ---", driver.irq);
    for i in 0..4 {
        let val = (i as u8) << 4 | i as u8;
        driver.write_reg(i, val);
    }
    println!("--- interrupt handler done ---\n");
}

fn main() {
    println!("=== mini-kmod: Linux Driver Patterns Demo ===\n");

    let driver = init_module();

    simulate_hardware_interrupt(&driver);

    println!("--- file operations ---");
    driver.open().unwrap();

    let mut buf = [0u8; 8];
    driver.read(&mut buf).unwrap();
    println!("  read buf: {:02x?}", &buf[..8]);

    let out = b"hello\0\0\0";
    driver.write(out).unwrap();

    driver.read(&mut buf).unwrap();
    println!("  read buf: {:02x?} ('{}')", &buf[..8],
        String::from_utf8_lossy(&buf[..8]).trim_end_matches('\0'));

    driver.ioctl(0, 0).unwrap();
    driver.ioctl(1, 0).unwrap();

    driver.close();

    println!("\n--- platform device model ---");
    println!("  device:    {}", driver.name);
    println!("  irq:       {}", driver.irq);
    println!("  mmio_base: {:#x}", driver.mmio_base);
    println!("  mmio_size: {}", driver.mmio_size);

    let reg0 = driver.read_reg(0);
    println!("  reg[0]:    0x{:02x}", reg0);

    cleanup_module(&driver);

    println!("\n=== demo completed ===");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_module_init_exit() {
        let drv = init_module();
        assert_eq!(drv.name, "mini-kmod");
        assert_eq!(drv.irq, 42);
        cleanup_module(&drv);
        assert!(!MODULE_LOADED.load(Ordering::SeqCst));
    }

    #[test]
    fn test_file_operations() {
        let drv = init_module();

        drv.open().unwrap();
        drv.open().unwrap();
        drv.close();
        drv.close();

        cleanup_module(&drv);
    }

    #[test]
    fn test_read_write() {
        let drv = init_module();

        drv.open().unwrap();

        let out = b"Rust Drv";
        drv.write(out).unwrap();

        let mut buf = [0u8; 8];
        drv.read(&mut buf).unwrap();
        assert_eq!(&buf, out);

        drv.close();
        cleanup_module(&drv);
    }

    #[test]
    fn test_mmio_register() {
        let drv = MiniDriver::new("test", 0, 0x1000, 16);

        drv.write_reg(4, 0xab);
        assert_eq!(drv.read_reg(4), 0xab);

        drv.write_reg(4, 0xcd);
        assert_eq!(drv.read_reg(4), 0xcd);
    }

    #[test]
    fn test_ioctl() {
        let drv = MiniDriver::new("test", 99, 0x2000, 16);

        let info = drv.ioctl(0, 0).unwrap();
        assert_eq!(info, 99);

        drv.ioctl(1, 0).unwrap();

        assert!(drv.ioctl(99, 0).is_err());
    }

    #[test]
    fn test_register_out_of_bounds() {
        let drv = MiniDriver::new("test", 0, 0, 4);
        assert_eq!(drv.read_reg(3), 0);
    }

    #[test]
    #[should_panic(expected = "MMIO offset out of bounds")]
    fn test_register_out_of_bounds_panics() {
        let drv = MiniDriver::new("test", 0, 0, 4);
        drv.read_reg(4);
    }

    #[test]
    fn test_hardware_interrupt() {
        let drv = MiniDriver::new("test", 7, 0x3000, 16);
        drv.write_reg(0, 0x00);

        for i in 0..4 {
            drv.write_reg(i, (i as u8) << 4 | i as u8);
        }

        assert_eq!(drv.read_reg(0), 0x00);
        assert_eq!(drv.read_reg(1), 0x11);
        assert_eq!(drv.read_reg(2), 0x22);
        assert_eq!(drv.read_reg(3), 0x33);
    }
}
