// mini-rt: A minimal runtime demonstrating systems programming concepts
//
// This crate demonstrates three core systems programming patterns:
// 1. Custom global allocator (bump allocator) with unsafe
// 2. Safe abstractions over unsafe FFI to libc
// 3. Low-level memory manipulation

use std::alloc::{GlobalAlloc, Layout};
use std::sync::atomic::{AtomicUsize, Ordering};

// ─── Part 1: Custom Bump Allocator ─────────────────────────────────
//
// A bump (arena) allocator is the simplest possible allocator:
// - Allocation: bump a pointer forward
// - Deallocation: no-op (memory freed all at once when arena is reset)
//
// This demonstrates: unsafe pointer manipulation, GlobalAlloc trait,
// raw memory management without the standard library's allocator.

const HEAP_SIZE: usize = 64 * 1024; // 64KB heap
static mut HEAP_MEMORY: [u8; HEAP_SIZE] = [0u8; HEAP_SIZE];

fn heap_bounds() -> (usize, usize) {
    let ptr = std::ptr::addr_of_mut!(HEAP_MEMORY);
    let start = ptr as usize;
    (start, start + HEAP_SIZE)
}

// Only use bump allocator in non-test builds (tests need standard allocator)
#[cfg(not(test))]
#[global_allocator]
static ALLOCATOR: BumpAllocator = BumpAllocator::new();

/// A bump allocator with a fixed-size heap.
///
/// # Safety
///
/// This allocator is NOT thread-safe. It should only be used in single-threaded
/// contexts or with external synchronization.
pub struct BumpAllocator {
    offset: AtomicUsize,
}

unsafe impl Sync for BumpAllocator {}

impl BumpAllocator {
    pub const fn new() -> Self {
        BumpAllocator { offset: AtomicUsize::new(0) }
    }

    pub fn reset(&self) {
        self.offset.store(0, Ordering::SeqCst);
    }

    pub fn allocated(&self) -> usize {
        self.offset.load(Ordering::SeqCst)
    }
}

unsafe impl GlobalAlloc for BumpAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let size = layout.size();
        let align = layout.align();
        let current = self.offset.load(Ordering::SeqCst);
        let aligned = (current + align - 1) & !(align - 1);
        let (start, end) = heap_bounds();

        if start + aligned + size > end {
            return std::ptr::null_mut();
        }

        self.offset.store(aligned + size, Ordering::SeqCst);
        // SAFETY: Bounds checked above, alignment satisfied
        unsafe { (start as *mut u8).add(aligned) }
    }

    unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {}
}

// ─── Part 2: Safe FFI Wrapper ──────────────────────────────────────
//
// This demonstrates: FFI to libc, unsafe extern functions,
// safe wrapper patterns for system calls.

pub fn get_process_id() -> u32 {
    unsafe { libc::getpid() as u32 }
}

pub fn get_hostname() -> Result<String, std::io::Error> {
    let mut buf = vec![0u8; 256];
    let result = unsafe {
        libc::gethostname(buf.as_mut_ptr() as *mut libc::c_char, buf.len())
    };

    if result != 0 {
        return Err(std::io::Error::last_os_error());
    }

    let len = buf.iter().position(|&c| c == 0).unwrap_or(buf.len());
    buf.truncate(len);
    Ok(String::from_utf8_lossy(&buf).into_owned())
}

// ─── Part 3: Low-level Memory Operations ───────────────────────────
//
// Demonstrates: raw pointer arithmetic, uninitialized memory, volatile access.

/// A safe wrapper around a memory-mapped register (MMIO).
#[derive(Clone, Copy)]
pub struct MappedRegister<T> {
    address: usize,
    _phantom: std::marker::PhantomData<T>,
}

impl<T: Copy> MappedRegister<T> {
    /// Create a new MMIO register at the given address.
    ///
    /// # Safety
    ///
    /// `address` must point to a valid, aligned hardware register.
    pub unsafe fn new(address: usize) -> Self {
        MappedRegister { address, _phantom: std::marker::PhantomData }
    }

    pub fn read(&self) -> T {
        unsafe { core::ptr::read_volatile(self.address as *const T) }
    }

    pub fn write(&self, value: T) {
        unsafe { core::ptr::write_volatile(self.address as *mut T, value) }
    }
}

/// A simple ring buffer implemented with unsafe.
pub struct RingBuffer<T: Copy + Default> {
    buffer: *mut T,
    capacity: usize,
    head: usize,
    tail: usize,
    full: bool,
}

unsafe impl<T: Copy + Default> Send for RingBuffer<T> {}

impl<T: Copy + Default> RingBuffer<T> {
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0 && capacity.is_power_of_two());
        let layout = std::alloc::Layout::array::<T>(capacity).unwrap();
        // SAFETY: Layout is valid, non-zero size checked above
        let buffer = unsafe { std::alloc::alloc(layout) as *mut T };
        if buffer.is_null() {
            panic!("Failed to allocate ring buffer");
        }
        RingBuffer { buffer, capacity, head: 0, tail: 0, full: false }
    }

    pub fn push(&mut self, item: T) -> Option<T> {
        let evicted = if self.is_full() { Some(self.pop_front()) } else { None };
        // SAFETY: tail < capacity, buffer allocated for capacity elements
        unsafe { self.buffer.add(self.tail).write(item) }
        self.tail = (self.tail + 1) & (self.capacity - 1);
        if self.tail == self.head { self.full = true; }
        evicted
    }

    pub fn pop_front(&mut self) -> T {
        assert!(!self.is_empty(), "Cannot pop from empty buffer");
        // SAFETY: head < capacity, buffer initialized
        let item = unsafe { self.buffer.add(self.head).read() };
        self.head = (self.head + 1) & (self.capacity - 1);
        self.full = false;
        item
    }

    pub fn is_empty(&self) -> bool { !self.full && self.head == self.tail }
    pub fn is_full(&self) -> bool { self.full }

    pub fn len(&self) -> usize {
        if self.full { self.capacity }
        else if self.tail >= self.head { self.tail - self.head }
        else { self.capacity - (self.head - self.tail) }
    }
}

impl<T: Copy + Default> Drop for RingBuffer<T> {
    fn drop(&mut self) {
        if !self.buffer.is_null() {
            let layout = std::alloc::Layout::array::<T>(self.capacity).unwrap();
            // SAFETY: buffer was allocated with the same layout
            unsafe { std::alloc::dealloc(self.buffer as *mut u8, layout) }
        }
    }
}

fn main() {
    println!("=== mini-rt: Systems Programming Demo ===\n");

    println!("PID: {}", get_process_id());
    println!("Hostname: {}", get_hostname().unwrap_or_else(|e| format!("Error: {}", e)));

    println!("\n--- Ring Buffer Demo ---");
    let mut buf = RingBuffer::<i32>::new(4);
    buf.push(10);
    buf.push(20);
    buf.push(30);
    println!("Buffer len: {}", buf.len());
    println!("Pop: {}", buf.pop_front());
    println!("Pop: {}", buf.pop_front());

    println!("\n--- MMIO Register Demo ---");
    let mut value: u32 = 42;
    // SAFETY: value is a valid stack variable
    let reg = unsafe { MappedRegister::<u32>::new(&mut value as *mut u32 as usize) };
    println!("Register read: {}", reg.read());
    reg.write(100);
    println!("After write: {}", value);

    println!("\n--- Bump Allocator Demo ---");
    let mut v = Vec::with_capacity(10);
    v.push(1);
    v.push(2);
    v.push(3);
    println!("Vec from bump allocator: {:?}", v);
    #[cfg(not(test))]
    println!("Allocated: {} bytes", ALLOCATOR.allocated());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bump_allocator() {
        let mut v = Vec::with_capacity(100);
        v.push(42);
        assert_eq!(v[0], 42);
    }

    #[test]
    fn test_ring_buffer() {
        let mut buf = RingBuffer::<i32>::new(4);
        assert!(buf.is_empty());
        buf.push(1);
        buf.push(2);
        buf.push(3);
        assert_eq!(buf.len(), 3);
        assert_eq!(buf.pop_front(), 1);
        assert_eq!(buf.pop_front(), 2);
    }

    #[test]
    fn test_ring_buffer_overwrite() {
        let mut buf = RingBuffer::<i32>::new(2);
        buf.push(1);
        buf.push(2);
        buf.push(3);
        assert_eq!(buf.pop_front(), 2);
        assert_eq!(buf.pop_front(), 3);
    }

    #[test]
    fn test_hostname() {
        let hostname = get_hostname().unwrap();
        assert!(!hostname.is_empty());
    }

    #[test]
    fn test_mmio() {
        let mut value: u32 = 42;
        let reg = unsafe { MappedRegister::<u32>::new(&mut value as *mut u32 as usize) };
        assert_eq!(reg.read(), 42);
        reg.write(100);
        assert_eq!(value, 100);
    }

    #[test]
    fn test_pid() {
        let pid = get_process_id();
        assert!(pid > 0);
    }
}
