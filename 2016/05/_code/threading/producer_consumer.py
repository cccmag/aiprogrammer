# Producer-Consumer problem solution

import threading
import time
import random

class Buffer:
    def __init__(self, size=10):
        self.size = size
        self.buffer = []
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def produce(self, item):
        with self.not_full:
            while len(self.buffer) >= self.size:
                self.not_full.wait()
            self.buffer.append(item)
            self.not_empty.notify()

    def consume(self):
        with self.not_empty:
            while not self.buffer:
                self.not_empty.wait()
            item = self.buffer.pop(0)
            self.not_full.notify()
            return item

def producer(buffer, count, producer_id):
    for i in range(count):
        item = f"P{producer_id}-{i}"
        time.sleep(random.random() * 0.1)
        buffer.produce(item)
        print(f"Producer {producer_id} produced: {item}")

def consumer(buffer, count, consumer_id):
    for i in range(count):
        time.sleep(random.random() * 0.1)
        item = buffer.consume()
        print(f"Consumer {consumer_id} consumed: {item}")

if __name__ == "__main__":
    buffer = Buffer(5)
    num_items = 5

    producers = []
    consumers = []

    for i in range(2):
        t = threading.Thread(target=producer, args=(buffer, num_items, i))
        producers.append(t)

    for i in range(2):
        t = threading.Thread(target=consumer, args=(buffer, num_items, i))
        consumers.append(t)

    for t in producers + consumers:
        t.start()

    for t in producers + consumers:
        t.join()

    print("\nAll producers and consumers finished!")
    print(f"Buffer size: {len(buffer.buffer)}")