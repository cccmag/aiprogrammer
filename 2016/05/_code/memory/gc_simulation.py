# Mark-Sweep GC simulation

class GCObject:
    def __init__(self, name, refs=None):
        self.name = name
        self.refs = refs or []
        self.marked = False

class MarkSweepGC:
    def __init__(self):
        self.heap = []
        self.roots = []

    def allocate(self, name, refs=None):
        obj = GCObject(name, refs)
        self.heap.append(obj)
        return obj

    def add_root(self, obj):
        self.roots.append(obj)

    def mark(self):
        """Mark all reachable objects from roots"""
        stack = list(self.roots)
        while stack:
            obj = stack.pop()
            if not obj.marked:
                obj.marked = True
                stack.extend(obj.refs)

    def sweep(self):
        """Sweep unmarked objects"""
        collected = []
        survivors = []
        for obj in self.heap:
            if obj.marked:
                obj.marked = False
                survivors.append(obj)
            else:
                collected.append(obj)
        self.heap = survivors
        return collected

    def collect(self):
        print("Starting GC...")
        self.mark()
        collected = self.sweep()
        print(f"Collected {len(collected)} objects: {[o.name for o in collected]}")
        return collected

    def show_state(self):
        for obj in self.heap:
            refs = [r.name for r in obj.refs]
            print(f"  {obj.name}: refs={refs}, marked={obj.marked}")

if __name__ == "__main__":
    gc = MarkSweepGC()

    # Create some objects
    a = gc.allocate("A")
    b = gc.allocate("B")
    c = gc.allocate("C")
    d = gc.allocate("D")

    # Set up references: A -> B -> C, A -> D
    a.refs = [b, d]
    b.refs = [c]

    # A is root
    gc.add_root(a)

    print("Before GC:")
    gc.show_state()
    gc.collect()

    print("\nAfter GC:")
    gc.show_state()

    print("\n--- After removing B reference ---")
    a.refs = [d]
    gc.collect()

    print("\nFinal state:")
    gc.show_state()