use std::cell::RefCell;
use std::collections::VecDeque;

// ---- GPIO ----

#[derive(Clone, Copy, PartialEq, Debug)]
enum PinMode {
    Input,
    Output,
}

#[derive(Clone, Copy, PartialEq, Debug)]
enum PinState {
    Low,
    High,
}

struct GpioPin {
    mode: PinMode,
    state: PinState,
}

impl GpioPin {
    fn new() -> Self {
        GpioPin { mode: PinMode::Input, state: PinState::Low }
    }

    fn set_mode(&mut self, mode: PinMode) {
        self.mode = mode;
        println!("  [GPIO]  mode -> {:?}", self.mode);
    }

    fn set_high(&mut self) {
        assert_eq!(self.mode, PinMode::Output, "pin not in output mode");
        self.state = PinState::High;
        println!("  [GPIO]  set HIGH");
    }

    fn set_low(&mut self) {
        assert_eq!(self.mode, PinMode::Output, "pin not in output mode");
        self.state = PinState::Low;
        println!("  [GPIO]  set LOW");
    }

    fn read(&self) -> PinState {
        assert_eq!(self.mode, PinMode::Input, "pin not in input mode");
        self.state
    }
}

struct GpioPort<const N: usize> {
    pins: [RefCell<GpioPin>; N],
}

impl<const N: usize> GpioPort<N> {
    fn new() -> Self {
        let pins = [0; N].map(|_| RefCell::new(GpioPin::new()));
        GpioPort { pins }
    }

    fn pin(&self, n: usize) -> &RefCell<GpioPin> {
        assert!(n < N, "pin index out of range");
        &self.pins[n]
    }
}

// ---- UART ----

#[derive(Clone, Copy, PartialEq, Debug)]
enum UartMode {
    Polling,
    Interrupt,
}

struct SimUart {
    #[allow(dead_code)]
    mode: UartMode,
    #[allow(dead_code)]
    baud: u32,
    rx_buffer: VecDeque<u8>,
    tx_buffer: VecDeque<u8>,
}

impl SimUart {
    fn new(baud: u32) -> Self {
        SimUart {
            mode: UartMode::Polling,
            baud,
            rx_buffer: VecDeque::new(),
            tx_buffer: VecDeque::new(),
        }
    }

    fn set_mode(&mut self, mode: UartMode) {
        self.mode = mode;
        println!("  [UART]  mode -> {:?}", self.mode);
    }

    fn write_byte(&mut self, byte: u8) {
        self.tx_buffer.push_back(byte);
        println!("  [UART]  TX: 0x{:02x} ('{}')", byte, byte as char);
    }

    fn write_str(&mut self, s: &str) {
        for b in s.bytes() {
            self.write_byte(b);
        }
    }

    fn read_byte(&mut self) -> Option<u8> {
        let byte = self.rx_buffer.pop_front();
        if let Some(b) = byte {
            println!("  [UART]  RX: 0x{:02x} ('{}')", b, b as char);
        }
        byte
    }

    fn inject_rx(&mut self, data: &[u8]) {
        for &b in data {
            self.rx_buffer.push_back(b);
        }
    }
}

// ---- Timer ----

struct SimTimer {
    period_ms: u32,
    elapsed_ms: u32,
    enabled: bool,
    callback: Option<fn()>,
}

impl SimTimer {
    fn new(period_ms: u32) -> Self {
        SimTimer { period_ms, elapsed_ms: 0, enabled: false, callback: None }
    }

    fn start(&mut self) {
        self.enabled = true;
        self.elapsed_ms = 0;
        println!("  [TIMER] started (period: {}ms)", self.period_ms);
    }

    fn tick(&mut self, ms: u32) {
        if !self.enabled {
            return;
        }
        self.elapsed_ms += ms;
        while self.elapsed_ms >= self.period_ms {
            self.elapsed_ms -= self.period_ms;
            println!("  [TIMER] overflow!");
            if let Some(cb) = self.callback {
                cb();
            }
        }
    }

    fn on_overflow(&mut self, cb: fn()) {
        self.callback = Some(cb);
    }
}

// ---- Interrupt Controller ----

struct Nvic {
    pending: VecDeque<u32>,
    enabled: [bool; 32],
}

impl Nvic {
    fn new() -> Self {
        Nvic { pending: VecDeque::new(), enabled: [false; 32] }
    }

    fn enable(&mut self, irq: u32) {
        assert!(irq < 32, "IRQ out of range");
        self.enabled[irq as usize] = true;
        println!("  [NVIC]  IRQ{} enabled", irq);
    }

    fn pend(&mut self, irq: u32) {
        if self.enabled[irq as usize] {
            self.pending.push_back(irq);
            println!("  [NVIC]  IRQ{} pended", irq);
        }
    }

    fn service_next(&mut self) -> Option<u32> {
        self.pending.pop_front()
    }
}

// ---- Peripherals ----

struct Peripherals {
    gpioa: GpioPort<16>,
    uart1: RefCell<SimUart>,
    timer2: RefCell<SimTimer>,
    nvic: RefCell<Nvic>,
}

impl Peripherals {
    fn new() -> Self {
        Peripherals {
            gpioa: GpioPort::new(),
            uart1: RefCell::new(SimUart::new(115_200)),
            timer2: RefCell::new(SimTimer::new(1000)),
            nvic: RefCell::new(Nvic::new()),
        }
    }
}

// ---- Application ----

fn main() {
    println!("=== mini-embedded: Embedded System Patterns Demo ===\n");

    let peri = Peripherals::new();

    println!("--- GPIO: blinking LED ---");
    {
        let led = peri.gpioa.pin(5);
        let mut led = led.borrow_mut();
        led.set_mode(PinMode::Output);
        led.set_high();
        assert_eq!(led.state, PinState::High);
        led.set_low();
        assert_eq!(led.state, PinState::Low);
    }

    println!("\n--- GPIO: reading button ---");
    {
        let btn = peri.gpioa.pin(0);
        let mut btn = btn.borrow_mut();
        btn.set_mode(PinMode::Input);
        btn.state = PinState::High;
        assert_eq!(btn.read(), PinState::High);
    }

    println!("\n--- UART: polling write ---");
    {
        let mut uart = peri.uart1.borrow_mut();
        uart.write_str("Hello from Rust!\n");
    }

    println!("\n--- UART: polling read ---");
    {
        let mut uart = peri.uart1.borrow_mut();
        uart.inject_rx(b"ABC");
        assert_eq!(uart.read_byte(), Some(b'A'));
        assert_eq!(uart.read_byte(), Some(b'B'));
        assert_eq!(uart.read_byte(), Some(b'C'));
        assert_eq!(uart.read_byte(), None);
    }

    println!("\n--- UART: interrupt mode ---");
    {
        let mut uart = peri.uart1.borrow_mut();
        uart.set_mode(UartMode::Interrupt);
    }
    {
        let mut nvic = peri.nvic.borrow_mut();
        nvic.enable(5);
    }

    println!("\n--- Timer: periodic interrupt ---");
    {
        let mut timer = peri.timer2.borrow_mut();
            timer.on_overflow(move || {
            println!("  [ISR]    timer overflow callback");
        });
        timer.start();

        timer.tick(500);
        timer.tick(600);
        timer.tick(400);
        timer.tick(200);
    }

    println!("\n--- NVIC: interrupt handling ---");
    {
        let mut nvic = peri.nvic.borrow_mut();
        nvic.pend(5);
        nvic.pend(5);
        while let Some(irq) = nvic.service_next() {
            println!("  [ISR]    servicing IRQ{}", irq);
        }
    }

    println!("\n--- System info ---");
    println!("  clock:   72 MHz (simulated)");
    println!("  flash:   512 KiB");
    println!("  sram:    128 KiB");
    println!("  uart:    115200 baud");
    println!("  timer:   1000 ms period");

    println!("\n=== demo completed ===");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gpio_output() {
        let port = GpioPort::<16>::new();
        let pin = port.pin(5);
        let mut pin = pin.borrow_mut();
        pin.set_mode(PinMode::Output);
        pin.set_high();
        assert_eq!(pin.state, PinState::High);
        pin.set_low();
        assert_eq!(pin.state, PinState::Low);
    }

    #[test]
    #[should_panic(expected = "not in output mode")]
    fn test_gpio_write_input_panics() {
        let port = GpioPort::<16>::new();
        let pin = port.pin(5);
        let mut pin = pin.borrow_mut();
        pin.set_mode(PinMode::Input);
        pin.set_high();
    }

    #[test]
    fn test_gpio_input() {
        let port = GpioPort::<16>::new();
        let pin = port.pin(0);
        let mut pin = pin.borrow_mut();
        pin.set_mode(PinMode::Input);
        pin.state = PinState::High;
        assert_eq!(pin.read(), PinState::High);
        pin.state = PinState::Low;
        assert_eq!(pin.read(), PinState::Low);
    }

    #[test]
    fn test_uart_polling() {
        let mut uart = SimUart::new(9600);
        uart.inject_rx(b"Rust");
        assert_eq!(uart.read_byte(), Some(b'R'));
        assert_eq!(uart.read_byte(), Some(b'u'));
        assert_eq!(uart.read_byte(), Some(b's'));
        assert_eq!(uart.read_byte(), Some(b't'));
        assert_eq!(uart.read_byte(), None);
    }

    #[test]
    fn test_uart_write() {
        let mut uart = SimUart::new(115200);
        uart.write_byte(b'H');
        uart.write_byte(b'i');
        assert_eq!(uart.tx_buffer.len(), 2);
    }

    #[test]
    fn test_timer_overflow() {
        let mut timer = SimTimer::new(100);
        timer.start();
        timer.tick(50);
        assert_eq!(timer.elapsed_ms, 50);
        timer.tick(60);
        assert!(timer.elapsed_ms < 100);
    }

    #[test]
    fn test_nvic_irq() {
        let mut nvic = Nvic::new();
        nvic.enable(10);
        nvic.pend(10);
        assert_eq!(nvic.service_next(), Some(10));
        assert_eq!(nvic.service_next(), None);
    }

    #[test]
    fn test_nvic_disabled_irq_not_pended() {
        let mut nvic = Nvic::new();
        nvic.pend(5);
        assert_eq!(nvic.service_next(), None);
    }

    #[test]
    fn test_all_peripherals() {
        let peri = Peripherals::new();

        let mut led = peri.gpioa.pin(5).borrow_mut();
        led.set_mode(PinMode::Output);
        led.set_high();

        let mut uart = peri.uart1.borrow_mut();
        uart.inject_rx(b"ok");
        assert_eq!(uart.read_byte(), Some(b'o'));

        let mut timer = peri.timer2.borrow_mut();
        timer.start();
        timer.tick(1500);
    }

    #[test]
    #[should_panic(expected = "pin index out of range")]
    fn test_pin_out_of_range() {
        let port = GpioPort::<8>::new();
        port.pin(8);
    }
}
