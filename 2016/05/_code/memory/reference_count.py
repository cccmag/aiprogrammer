# Reference counting implementation

class RefCountedObject:
    def __init__(self, name):
        self.name = name
        self.refcount = 0
        print(f"Created {name}")

    def add_ref(self):
        self.refcount += 1
        print(f"  {self.name} refcount: {self.refcount}")
        return self

    def release(self):
        self.refcount -= 1
        print(f"  {self.name} refcount: {self.refcount}")
        if self.refcount <= 0:
            print(f"  GC: Collecting {self.name}")
            return True
        return False

class RefCountGC:
    def __init__(self):
        self.objects = {}

    def new_object(self, name):
        obj = RefCountedObject(name)
        self.objects[name] = obj
        return obj.add_ref()

    def reference(self, obj):
        return obj.add_ref()

    def release(self, obj):
        if obj.release():
            del self.objects[obj.name]

if __name__ == "__main__":
    gc = RefCountGC()

    print("Creating object...")
    obj1 = gc.new_object("Object1")

    print("\nCreating reference...")
    obj2 = gc.reference(obj1)

    print("\nReleasing reference...")
    gc.release(obj1)

    print("\nReleasing final reference...")
    gc.release(obj2)

    print("\n--- Testing circular reference ---")
    # Circular reference handling requires cycle GC