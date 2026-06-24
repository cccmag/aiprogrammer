#!/usr/bin/env python3
"""Computer Architecture Simulator - ALU, Pipeline, Cache, CPI"""

class ALU:
    def execute(self, op: str, a: int, b: int) -> int:
        ops = {
            'ADD': lambda: a + b,
            'SUB': lambda: a - b,
            'AND': lambda: a & b,
            'OR':  lambda: a | b,
            'XOR': lambda: a ^ b,
            'MUL': lambda: a * b,
        }
        return ops[op]()


class Pipeline:
    STAGES = ['IF', 'ID', 'EX', 'MEM', 'WB']

    def __init__(self, num_inst=8):
        self.num_inst = num_inst
        self.cycle = 0
        self.stage_inst = {s: None for s in self.STAGES}

    def step(self):
        self.cycle += 1
        for i in reversed(range(len(self.STAGES))):
            if i == len(self.STAGES) - 1:
                self.stage_inst[self.STAGES[i]] = self.stage_inst[self.STAGES[i-1]]
            elif i > 0:
                self.stage_inst[self.STAGES[i]] = self.stage_inst[self.STAGES[i-1]]
            else:
                n = self.cycle - 1
                self.stage_inst[self.STAGES[i]] = f"inst{n}" if n < self.num_inst else None

    def run(self):
        print("=== Pipeline Simulation ===")
        done = [False] * self.num_inst
        while not all(done):
            self.step()
            line = f"Cycle {self.cycle:3d}: "
            for s in self.STAGES:
                inst = self.stage_inst[s]
                if inst:
                    idx = int(inst.replace('inst', ''))
                    if s == 'WB':
                        done[idx] = True
                    line += f"{s}({inst})  "
            if any(self.stage_inst.values()):
                print(line)
        print()

    @property
    def total_cycles(self):
        return self.num_inst + len(self.STAGES) - 1


class Cache:
    def __init__(self, size=1024, block_size=64):
        self.block_size = block_size
        self.num_blocks = size // block_size
        self.blocks = [None] * self.num_blocks
        self.hits = 0
        self.misses = 0

    def read(self, address):
        idx = (address // self.block_size) % self.num_blocks
        tag = address // self.block_size
        if self.blocks[idx] == tag:
            self.hits += 1
            return True
        self.blocks[idx] = tag
        self.misses += 1
        return False

    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total * 100 if total else 0


class CPICalculator:
    def __init__(self):
        self.inst_types = {
            'ALU':     {'count': 0, 'cpi': 1},
            'LOAD':    {'count': 0, 'cpi': 2},
            'STORE':   {'count': 0, 'cpi': 2},
            'BRANCH':  {'count': 0, 'cpi': 3},
            'FP':      {'count': 0, 'cpi': 4},
        }

    def add_inst(self, itype, count=1):
        if itype in self.inst_types:
            self.inst_types[itype]['count'] += count

    @property
    def total_insts(self):
        return sum(t['count'] for t in self.inst_types.values())

    @property
    def avg_cpi(self):
        total = self.total_insts
        if total == 0:
            return 0
        weighted = sum(t['count'] * t['cpi'] for t in self.inst_types.values())
        return weighted / total

    def execution_time(self, clock_rate=2e9):
        return self.total_insts * self.avg_cpi / clock_rate


def demo():
    alu = ALU()
    print("=== ALU Operations ===")
    for op in ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'MUL']:
        a, b = 10, 20
        res = alu.execute(op, a, b)
        print(f"{op}({a}, {b}) = {res}")
    print()

    pipe = Pipeline(8)
    pipe.run()
    ideal_cycles = pipe.num_inst * len(Pipeline.STAGES)
    actual_cycles = pipe.total_cycles
    print(f"No-pipeline cycles: {ideal_cycles}")
    print(f"Pipeline cycles: {actual_cycles}")
    print(f"Speedup: {ideal_cycles}/{actual_cycles} = {ideal_cycles/actual_cycles:.2f}")
    print()

    cache = Cache(size=256, block_size=32)
    for addr in [0, 32, 64, 96, 0, 32, 100, 128, 64, 0]:
        cache.read(addr)
    print("=== Cache Simulation ===")
    print(f"Hits: {cache.hits}, Misses: {cache.misses}, Hit rate: {cache.hit_rate():.1f}%")
    print()

    calc = CPICalculator()
    calc.add_inst('ALU', 300)
    calc.add_inst('LOAD', 200)
    calc.add_inst('STORE', 100)
    calc.add_inst('BRANCH', 150)
    calc.add_inst('FP', 50)
    print("=== CPI Calculation ===")
    for t, d in calc.inst_types.items():
        pct = d['count'] / calc.total_insts * 100
        print(f"{t:8s}: {d['count']:4d} insts, CPI={d['cpi']}, {pct:5.1f}%")
    print(f"Total instructions: {calc.total_insts}")
    print(f"Average CPI: {calc.avg_cpi:.2f}")
    print(f"Execution time (2GHz): {calc.execution_time()*1e6:.2f} us")
    print()

    print("=== Amdahl's Law Demo ===")
    for p in [0.5, 0.75, 0.9, 0.95, 0.99]:
        s = 10.0
        speedup = 1.0 / ((1 - p) + p / s)
        print(f"P={p:.2f}, S={s:.0f}: speedup={speedup:.2f}")


if __name__ == "__main__":
    demo()
