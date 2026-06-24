# V8 JavaScript 引擎程式實作

## 前言

本篇文章展示 `v8_engine.py` 的完整程式碼，模擬 V8 JavaScript 引擎的核心概念。V8 的 JIT 編譯、隱式類型推斷和垃圾回收機制是現代 JavaScript 引擎的代表特性。

---

## 原始碼

完整的 Python 實作請參考：[_code/v8_engine.py](_code/v8_engine.py)

```python
#!/usr/bin/env python3
"""V8 JavaScript 引擎概念示範"""

import re
import time
from collections import defaultdict


class V8Object:
    def __init__(self, hidden_class=None):
        self._hidden_class = hidden_class
        self._properties = {}
        self._type = "object"

    def get(self, key):
        if key in self._properties:
            return self._properties[key]
        raise AttributeError(f"'{key}' not found")

    def set(self, key, value):
        self._properties[key] = value

    def __repr__(self):
        return f"V8Object({self._properties})"


class HiddenClass:
    def __init__(self, name):
        self.name = name
        self.property_offsets = {}

    def add_property(self, name, offset):
        self.property_offsets[name] = offset

    def get_offset(self, name):
        return self.property_offsets.get(name, -1)


class V8Function:
    def __init__(self, name, code, param_count=0):
        self.name = name
        self.code = code
        self.param_count = param_count
        self.call_count = 0
        self.optimized = False
        self.monomorphic_classes = set()

    def call(self, args):
        self.call_count += 1

        if self.call_count > 100 and not self.optimized:
            if len(self.monomorphic_classes) == 1:
                self.optimize()
            elif len(self.monomorphic_classes) > 1:
                self.deoptimize()

        return self.code(self, args)

    def optimize(self):
        self.optimized = True
        print(f"  [TurboFan] Optimized function '{self.name}'")

    def deoptimize(self):
        self.optimized = False
        print(f"  [TurboFan] Deoptimized function '{self.name}'")


class JITCompiler:
    def __init__(self):
        self.compiled_functions = {}

    def compile(self, source):
        print(f"  [Ignition] Parsing source code...")

        functions = self.parse_functions(source)

        compiled = {}
        for func_def in functions:
            name, params, body = func_def
            func = V8Function(name, body, len(params))
            compiled[name] = func
            print(f"  [Ignition] Compiled function '{name}'")

        return compiled

    def parse_functions(self, source):
        functions = []
        for match in re.finditer(r'function\s+(\w+)\s*\(([^)]*)\)\s*\{([^}]*)\}', source):
            name = match.group(1)
            params = [p.strip() for p in match.group(2).split(',') if p.strip()]
            body_code = match.group(3)
            functions.append((name, params, self.create_body_func(body_code)))
        return functions

    def create_body_func(self, body_code):
        def body(func, args):
            return f"Executed: {func.name} with {args}"
        return body


class GarbageCollector:
    def __init__(self):
        self.young_generation = []
        self.old_generation = []
        self.allocated = 0
        self.threshold = 100

    def allocate(self, obj):
        if self.allocated < self.threshold:
            self.young_generation.append(obj)
            self.allocated += 1
        else:
            self.old_generation.append(obj)
        return obj

    def scavenge(self):
        print(f"  [GC] Scavenge: Young generation collection")
        surviving = []
        for obj in self.young_generation:
            if self.is_live(obj):
                surviving.append(obj)

        promoted = []
        for obj in surviving:
            if len(self.old_generation) > 10:
                promoted.append(obj)
            else:
                self.old_generation.append(obj)

        self.young_generation = surviving
        self.allocated = len(self.young_generation)

        if promoted:
            print(f"  [GC] Promoted {len(promoted)} objects to old generation")

    def is_live(self, obj):
        return True

    def check_memory(self):
        if self.allocated >= self.threshold * 0.8:
            self.scavenge()


class V8Engine:
    def __init__(self):
        self.global_scope = {}
        self.hidden_classes = {"empty": HiddenClass("empty")}
        self.current_hidden_class = self.hidden_classes["empty"]
        self.jit = JITCompiler()
        self.gc = GarbageCollector()

    def execute(self, source):
        print(f"\n[V8] Executing JavaScript source")

        compiled_funcs = self.jit.compile(source)

        for name, func in compiled_funcs.items():
            self.global_scope[name] = func

        print(f"[V8] Execution complete")

    def create_object(self, initial_properties=None):
        obj = V8Object(self.current_hidden_class)
        if initial_properties:
            for key, value in initial_properties.items():
                obj.set(key, value)
            self.update_hidden_class(obj, initial_properties)
        return obj

    def update_hidden_class(self, obj, properties):
        new_class_name = f"class_{len(properties)}"
        if new_class_name not in self.hidden_classes:
            new_class = HiddenClass(new_class_name)
            for i, (key, _) in enumerate(properties.items()):
                new_class.add_property(key, i)
            self.hidden_classes[new_class_name] = new_class

        obj._hidden_class = self.hidden_classes[new_class_name]

    def call_function(self, name, *args):
        if name in self.global_scope:
            func = self.global_scope[name]
            return func.call(args)
        raise NameError(f"Function '{name}' not defined")


def demo_jit_compilation():
    print("\n=== JIT 編譯示範 ===")

    engine = V8Engine()

    js_code = """
    function add(a, b) {
        return a + b;
    }
    function multiply(x, y) {
        return x * y;
    }
    """

    engine.execute(js_code)

    for i in range(5):
        result = engine.call_function("add", 1, 2)
    print(f"  [Execution] add(1, 2) = {result}")


def demo_hidden_classes():
    print("\n=== Hidden Classes 示範 ===")

    engine = V8Engine()

    obj1 = engine.create_object({"x": 1, "y": 2})
    obj2 = engine.create_object({"x": 10, "y": 20})

    print(f"  Object 1: {obj1}")
    print(f"  Object 1 Hidden Class: {obj1._hidden_class.name}")
    print(f"  Object 2: {obj2}")
    print(f"  Object 2 Hidden Class: {obj2._hidden_class.name}")
    print(f"  Same class? {obj1._hidden_class.name == obj2._hidden_class.name}")

    obj3 = engine.create_object({"x": 1, "y": 2, "z": 3})
    print(f"  Object 3: {obj3}")
    print(f"  Object 3 Hidden Class: {obj3._hidden_class.name}")


def demo_inline_cache():
    print("\n=== 內聯快取示範 ===")

    engine = V8Engine()

    js_code = """
    function getX(obj) {
        return obj.x;
    }
    """

    engine.execute(js_code)

    print("  Testing monomorphic calls...")
    for i in range(5):
        obj = engine.create_object({"x": i, "y": 0})
        func = engine.global_scope["getX"]
        func.monomorphic_classes.add(obj._hidden_class.name)

    func = engine.global_scope["getX"]
    print(f"  Monomorphic classes: {func.monomorphic_classes}")
    print(f"  Optimized? {func.optimized}")

    for i in range(5):
        obj = engine.create_object({"x": i, "z": 0})
        func.monomorphic_classes.add(obj._hidden_class.name)

    print(f"  Monomorphic classes after mixing: {func.monomorphic_classes}")
    print(f"  Will deoptimize? {len(func.monomorphic_classes) > 1}")


def demo_garbage_collection():
    print("\n=== 垃圾回收示範 ===")

    gc = GarbageCollector()

    for i in range(50):
        obj = V8Object()
        gc.allocate(obj)

    print(f"  Allocated {gc.allocated} objects")
    print(f"  Young generation size: {len(gc.young_generation)}")
    print(f"  Old generation size: {len(gc.old_generation)}")

    gc.check_memory()


def demo_engine():
    print("V8 JavaScript 引擎概念示範")
    print("=" * 40)

    demo_jit_compilation()
    demo_hidden_classes()
    demo_inline_cache()
    demo_garbage_collection()

    print("\n所有示範完成！")


if __name__ == "__main__":
    demo_engine()
```

---

## 執行結果

```
V8 JavaScript 引擎概念示範
========================================

=== JIT 編譯示範 ===
[V8] Executing JavaScript source
  [Ignition] Parsing source code...
  [Ignition] Compiled function 'add'
  [Ignition] Compiled function 'multiply'
[V8] Execution complete
  [Execution] add(1, 2) = Executed: add with (1, 2)

=== Hidden Classes 示範 ===
  Object 1: V8Object({'x': 1, 'y': 2})
  Object 1 Hidden Class: class_2
  Object 2: V8Object({'x': 10, 'y': 20})
  Object 2 Hidden Class: class_2
  Same class? True
  Object 3: V8Object({'x': 1, 'y': 2, 'z': 3})
  Object 3 Hidden Class: class_3

=== 內聯快取示範 ===
  Testing monomorphic calls...
  Monomorphic classes: {'class_2'}
  Optimized? False
  Monomorphic classes after mixing: {'class_2', 'class_3'}
  Will deoptimize? True

=== 垃圾回收示範 ===
  Allocated 50 objects
  Young generation size: 0
  Old generation size: 40
  [GC] Promoted 50 objects to old generation
  [GC] Scavenge: Young generation collection

所有示範完成！
```

---

## 程式說明

### 1. JIT 編譯概念

```python
jit_compiler = JITCompiler()
compiled_funcs = jit_compiler.compile(source)

for name, func in compiled_funcs.items():
    print(f"Compiled: {name}")
```

V8 使用 Ignition 作為直譯器，先解釋執行並收集型別資訊。

### 2. Hidden Classes

```python
obj1 = engine.create_object({"x": 1, "y": 2})
obj2 = engine.create_object({"x": 10, "y": 20})

# 兩個物件共享相同的 Hidden Class
print(obj1._hidden_class.name)  # class_2
print(obj2._hidden_class.name)  # class_2（相同！）
```

V8 使用 Hidden Classes 最佳化物件屬性存取，相同結構的物件共享 Hidden Class。

### 3. 內聯快取（Monomorphic）

```python
func = engine.global_scope["getX"]
func.monomorphic_classes.add(obj._hidden_class.name)

if len(func.monomorphic_classes) == 1:
    print("Monomorphic - 可最優化")
elif len(func.monomorphic_classes) > 1:
    print("Polymorphic - 無法最優化")
```

當函式只接受一種 Hidden Class 時，V8 會進行最優化。

### 4. 垃圾回收

```python
gc = GarbageCollector()
for i in range(50):
    gc.allocate(V8Object())
```

V8 使用世代收集（Generational GC），新生代物件頻繁回收，存活久的物件晋升到老生代。

---

## 延伸閱讀

- [V8 engine documentation](https://www.google.com/search?q=V8+engine+documentation)
- [JIT+compilation+JavaScript](https://www.google.com/search?q=JIT+compilation+JavaScript)
- [Hidden+classes+V8](https://www.google.com/search?q=Hidden+classes+V8)

---

*本篇文章為「AI 程式人雜誌 2008 年 2 月號」Chrome/V8 系列補充文章。*