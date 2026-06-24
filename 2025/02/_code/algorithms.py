"""AI 程式人雜誌 — 資料結構與演算法基礎實戰"""

class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()
    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]
    def is_empty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)

class Queue:
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.pop(0)
    def is_empty(self):
        return len(self.items) == 0
    def size(self):
        return len(self.items)

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def fibonacci_dp(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

def demo():
    print("=" * 50)
    print("AI 程式人雜誌 — 資料結構與演算法基礎實戰")
    print("=" * 50)

    print("\n1. Stack 堆疊 (LIFO)")
    s = Stack()
    for i in range(1, 6):
        s.push(i)
        print(f"   push({i}) -> size={s.size()}")
    while not s.is_empty():
        print(f"   pop() -> {s.pop()}, size={s.size()}")

    print("\n2. Queue 佇列 (FIFO)")
    q = Queue()
    for c in "ABCDE":
        q.enqueue(c)
        print(f"   enqueue({c}) -> size={q.size()}")
    while not q.is_empty():
        print(f"   dequeue() -> {q.dequeue()}, size={q.size()}")

    print("\n3. Binary Search 二分搜尋")
    arr = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72]
    targets = [23, 1, 72]
    for t in targets:
        idx = binary_search(arr, t)
        if idx != -1:
            print(f"   binary_search({arr}, {t}) -> index {idx}")
        else:
            print(f"   binary_search({arr}, {t}) -> 未找到")

    print("\n4. Quicksort 快速排序")
    unsorted = [3, 6, 8, 10, 1, 2, 1, 4, 5, 9]
    sorted_arr = quicksort(unsorted)
    print(f"   排序前: {unsorted}")
    print(f"   排序後: {sorted_arr}")

    print("\n5. Fibonacci DP 費氏數列 (動態規劃)")
    for n in range(10):
        print(f"   fib({n}) = {fibonacci_dp(n)}")

    print("\n" + "=" * 50)
    print("所有演算法執行成功！")

if __name__ == "__main__":
    demo()
