# Simple stack-based virtual machine

class StackVM:
    def __init__(self):
        self.stack = []
        self.locals = {}
        self.ip = 0

    def execute(self, bytecode):
        ops = {
            'ICONST': lambda v: self.stack.append(v),
            'IADD': lambda: self._binop(lambda a, b: a + b),
            'ISUB': lambda: self._binop(lambda a, b: a - b),
            'IMUL': lambda: self._binop(lambda a, b: a * b),
            'ILT': lambda: self._compare(lambda a, b: a < b),
            'BR': lambda dest: self.__dict__.update({'ip': dest - 1}),
            'BRT': lambda dest: self._branch_true(dest),
            'BRF': lambda dest: self._branch_false(dest),
            'LOAD': lambda idx: self.stack.append(self.locals.get(idx, 0)),
            'STORE': lambda idx: self.locals.update({idx: self.stack.pop()}),
            'DUP': lambda: self.stack.append(self.stack[-1]),
            'POP': lambda: self.stack.pop(),
            'HALT': lambda: None,
        }

        self.ip = 0
        while self.ip < len(bytecode):
            op, *args = bytecode[self.ip]
            if op == 'HALT':
                break
            ops[op](*args) if args else ops[op]()
            self.ip += 1

        return self.stack[-1] if self.stack else None

    def _binop(self, op):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(op(a, b))

    def _compare(self, op):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(1 if op(a, b) else 0)

    def _branch_true(self, dest):
        if self.stack.pop():
            self.ip = dest - 1

    def _branch_false(self, dest):
        if not self.stack.pop():
            self.ip = dest - 1

if __name__ == "__main__":
    # Example: compute 10!
    bytecode = [
        ('ICONST', 1),     # 1
        ('STORE', 0),      # result = 1
        ('ICONST', 1),     # i = 1
        ('STORE', 1),       # store i
        ('LOAD', 1),        # load i
        ('ICONST', 10),    # load 10
        ('ILT',),          # i < 10
        ('BRF', 14),       # if not, goto 14
        ('LOAD', 0),       # load result
        ('LOAD', 1),       # load i
        ('IMUL',),         # result * i
        ('STORE', 0),      # store result
        ('LOAD', 1),       # load i
        ('ICONST', 1),     # load 1
        ('IADD',),         # i + 1
        ('STORE', 1),      # store i
        ('BR', 6),         # goto 6
        ('LOAD', 0),       # load result
        ('HALT',),         # halt
    ]

    vm = StackVM()
    result = vm.execute(bytecode)
    print(f"10! = {result}")  # Should be 3628800