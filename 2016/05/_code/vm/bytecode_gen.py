# Bytecode generator for simple VM

class BytecodeGen:
    def __init__(self):
        self.bytecode = []
        self.labels = {}

    def emit(self, op, *args):
        self.bytecode.append((op, *args))
        return len(self.bytecode) - 1

    def iconst(self, value):
        return self.emit('ICONST', value)

    def iadd(self):
        return self.emit('IADD')

    def isub(self):
        return self.emit('ISUB')

    def imul(self):
        return self.emit('IMUL')

    def ilt(self):
        return self.emit('ILT')

    def br(self, label):
        return self.emit('BR', label)

    def brt(self, label):
        return self.emit('BRT', label)

    def brf(self, label):
        return self.emit('BRF', label)

    def label(self, name):
        self.labels[name] = len(self.bytecode)
        return len(self.bytecode)

    def load(self, idx):
        return self.emit('LOAD', idx)

    def store(self, idx):
        return self.emit('STORE', idx)

    def dup(self):
        return self.emit('DUP')

    def pop(self):
        return self.emit('POP')

    def halt(self):
        return self.emit('HALT')

def gen_factorial():
    gen = BytecodeGen()

    gen.iconst(1)
    gen.store(0)
    gen.iconst(1)
    gen.store(1)

    loop_start = gen.label('loop')
    gen.load(1)
    gen.iconst(10)
    gen.ilt()
    gen.brf('end')
    gen.load(0)
    gen.load(1)
    gen.imul()
    gen.store(0)
    gen.load(1)
    gen.iconst(1)
    gen.iadd()
    gen.store(1)
    gen.br('loop')

    gen.label('end')
    gen.load(0)
    gen.halt()

    return gen.bytecode

def gen_sum():
    gen = BytecodeGen()

    gen.iconst(0)
    gen.store(0)
    gen.iconst(1)
    gen.store(1)

    loop_start = gen.label('loop')
    gen.load(1)
    gen.iconst(11)
    gen.ilt()
    gen.brf('end')
    gen.load(0)
    gen.load(1)
    gen.iadd()
    gen.store(0)
    gen.load(1)
    gen.iconst(1)
    gen.iadd()
    gen.store(1)
    gen.br('loop')

    gen.label('end')
    gen.load(0)
    gen.halt()

    return gen.bytecode

if __name__ == "__main__":
    from vm.stack_vm import StackVM

    print("Computing 10!:")
    bytecode = gen_factorial()
    vm = StackVM()
    result = vm.execute(bytecode)
    print(f"Result: {result}")

    print("\nComputing sum 1+2+...+10:")
    bytecode = gen_sum()
    vm2 = StackVM()
    result2 = vm2.execute(bytecode)
    print(f"Result: {result2}")