# Mutex implementation and demonstration

import threading

class SimpleMutex:
    def __init__(self):
        self.locked = False
        self.thread = None
        self.queue = []

    def acquire(self):
        thread = threading.current_thread()
        while self.locked and self.thread != thread:
            event = threading.Event()
            self.queue.append(event)
            event.wait()
            self.queue.remove(event)
        self.locked = True
        self.thread = thread

    def release(self):
        self.locked = False
        self.thread = None
        if self.queue:
            self.queue[0].set()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *args):
        self.release()

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = SimpleMutex()

    def deposit(self, amount):
        with self.lock:
            new_balance = self.balance + amount
            self.balance = new_balance

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False

    def get_balance(self):
        with self.lock:
            return self.balance

def worker(account, n, amount, is_deposit):
    for i in range(n):
        if is_deposit:
            account.deposit(amount)
        else:
            account.withdraw(amount)

if __name__ == "__main__":
    account = BankAccount(1000)

    threads = []

    for i in range(5):
        t1 = threading.Thread(target=worker, args=(account, 100, 10, True))
        t2 = threading.Thread(target=worker, args=(account, 100, 10, False))
        threads.extend([t1, t2])

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"Final balance: {account.get_balance()}")