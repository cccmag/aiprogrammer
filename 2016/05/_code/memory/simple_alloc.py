# Simple memory allocator

class SimpleAllocator:
    def __init__(self, size=1024):
        self.memory = bytearray(size)
        self.allocated = [False] * size
        self.size = size

    def allocate(self, n):
        """First-fit allocation"""
        start = 0
        count = 0
        for i in range(self.size):
            if not self.allocated[i]:
                count += 1
                if count >= n:
                    for j in range(start, i + 1):
                        self.allocated[j] = True
                    return start
            else:
                start = i + 1
                count = 0
        return -1

    def free(self, addr, n):
        """Free allocated memory"""
        for i in range(addr, addr + n):
            self.allocated[i] = False

    def dump(self):
        """Print memory status"""
        print("Memory allocation status:")
        for i in range(self.size):
            status = "X" if self.allocated[i] else "_"
            if i % 64 == 0:
                print(f"\n{i:04d}: ", end="")
            print(status, end="")
        print()

if __name__ == "__main__":
    alloc = SimpleAllocator(128)

    print("Initial state:")
    alloc.dump()

    addr1 = alloc.allocate(10)
    print(f"\nAllocated 10 bytes at {addr1}")

    addr2 = alloc.allocate(20)
    print(f"Allocated 20 bytes at {addr2}")

    alloc.dump()

    alloc.free(addr1, 10)
    print(f"\nFreed 10 bytes at {addr1}")

    alloc.dump()