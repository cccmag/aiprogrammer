#!/usr/bin/env python3

class DFA:
    def __init__(self, states, alphabet, transition, start, accepts):
        self.transition = transition
        self.start = start
        self.accepts = set(accepts)

    def accept(self, s):
        state = self.start
        for ch in s:
            state = self.transition.get((state, ch))
            if state is None:
                return False
        return state in self.accepts


class NFA:
    def __init__(self, states, alphabet, transition, start, accepts):
        self.transition = transition
        self.start = start
        self.accepts = set(accepts)

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            s = stack.pop()
            for ns in self.transition.get((s, ''), set()):
                if ns not in closure:
                    closure.add(ns)
                    stack.append(ns)
        return closure

    def accept(self, s):
        states = self.epsilon_closure({self.start})
        for ch in s:
            next_states = set()
            for st in states:
                next_states |= self.transition.get((st, ch), set())
            states = self.epsilon_closure(next_states)
        return bool(states & self.accepts)


class RegexEngine:
    def __init__(self, pattern):
        self.nfa = self._compile(self._parse(pattern))

    def _parse(self, pattern):
        i = [0]
        def parse_union():
            left = parse_concat()
            while i[0] < len(pattern) and pattern[i[0]] == '|':
                i[0] += 1
                right = parse_concat()
                left = ('union', left, right)
            return left
        def parse_concat():
            left = parse_star()
            while i[0] < len(pattern) and pattern[i[0]] not in '|)':
                right = parse_star()
                left = ('concat', left, right)
            return left
        def parse_star():
            base = parse_base()
            while i[0] < len(pattern) and pattern[i[0]] == '*':
                i[0] += 1
                base = ('star', base)
            return base
        def parse_base():
            if i[0] >= len(pattern):
                return ('eps',)
            ch = pattern[i[0]]
            if ch == '(':
                i[0] += 1
                node = parse_union()
                if i[0] < len(pattern) and pattern[i[0]] == ')':
                    i[0] += 1
                return node
            elif ch == '\\' and i[0] + 1 < len(pattern):
                i[0] += 2
                return ('char', ch)
            else:
                i[0] += 1
                return ('char', ch)
        return parse_union()

    def _compile(self, node):
        next_id = [0]
        def new_state():
            sid = next_id[0]
            next_id[0] += 1
            return sid
        transitions = {}
        start = new_state()
        accept = new_state()
        def build(node, s):
            if node[0] == 'char':
                t = new_state()
                transitions.setdefault((s, node[1]), set()).add(t)
                return t
            elif node[0] == 'eps':
                return s
            elif node[0] == 'union':
                a1 = build(node[1], s)
                a2 = build(node[2], s)
                t = new_state()
                transitions.setdefault((a1, ''), set()).add(t)
                transitions.setdefault((a2, ''), set()).add(t)
                return t
            elif node[0] == 'concat':
                mid = build(node[1], s)
                return build(node[2], mid)
            elif node[0] == 'star':
                t = new_state()
                transitions.setdefault((s, ''), set()).add(t)
                mid = build(node[1], t)
                transitions.setdefault((mid, ''), set()).add(t)
                transitions.setdefault((mid, ''), set()).add(s)
                return s
        final = build(node, start)
        transitions.setdefault((final, ''), set()).add(accept)
        all_states = set()
        for (st, _), tgts in transitions.items():
            all_states.add(st)
            all_states |= tgts
        return NFA(all_states, set(), transitions, start, {accept})

    def match(self, s):
        return self.nfa.accept(s)


class CFGParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        token = self.peek()
        if expected is not None and token != expected:
            raise SyntaxError(f"Expected {expected}, got {token}")
        self.pos += 1
        return token

    def parse(self):
        result = self.parse_E()
        if self.peek() is not None:
            raise SyntaxError(f"Unexpected token {self.peek()}")
        return result

    def parse_E(self):
        left = self.parse_T()
        return self.parse_E_prime(left)

    def parse_E_prime(self, left):
        if self.peek() == '+':
            self.consume('+')
            right = self.parse_T()
            return self.parse_E_prime(('+', left, right))
        return left

    def parse_T(self):
        left = self.parse_F()
        return self.parse_T_prime(left)

    def parse_T_prime(self, left):
        if self.peek() == '*':
            self.consume('*')
            right = self.parse_F()
            return self.parse_T_prime(('*', left, right))
        return left

    def parse_F(self):
        if self.peek() == '(':
            self.consume('(')
            expr = self.parse_E()
            self.consume(')')
            return expr
        token = self.consume()
        return ('num', token)


def calc_ast(node):
    if node[0] == '+':
        return calc_ast(node[1]) + calc_ast(node[2])
    elif node[0] == '*':
        return calc_ast(node[1]) * calc_ast(node[2])
    elif node[0] == 'num':
        return int(node[1])


class TuringMachine:
    def __init__(self, transition, start, accepts, blank='_'):
        self.transition = transition
        self.start = start
        self.accepts = set(accepts)
        self.blank = blank
        self.tape = []
        self.head = 0
        self.state = start

    def reset(self, input_str):
        self.tape = list(input_str) if input_str else [self.blank]
        self.head = 0
        self.state = self.start

    def step(self):
        symbol = self.tape[self.head] if self.head < len(self.tape) else self.blank
        key = (self.state, symbol)
        if key not in self.transition:
            return False
        next_state, write, move = self.transition[key]
        if self.head >= len(self.tape):
            self.tape.append(self.blank)
        self.tape[self.head] = write
        if move == 'R':
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append(self.blank)
        elif move == 'L':
            self.head = max(0, self.head - 1)
        self.state = next_state
        return True

    def run(self, input_str, max_steps=1000):
        self.reset(input_str)
        for _ in range(max_steps):
            if self.state in self.accepts:
                return True
            if not self.step():
                return False
        return self.state in self.accepts


def demo():
    print("=" * 50)
    print("AI 程式人雜誌 - 形式語言與自動機實作展示")
    print("=" * 50)

    print("\n--- DFA 範例：以 00 結尾的二進位字串 ---")
    dfa = DFA(
        states={0, 1, 2},
        alphabet={'0', '1'},
        transition={
            (0, '0'): 1, (0, '1'): 0,
            (1, '0'): 2, (1, '1'): 0,
            (2, '0'): 2, (2, '1'): 0,
        },
        start=0,
        accepts={2},
    )
    for s in ["0", "00", "100", "1100", "1", "01", "101"]:
        print(f"  '{s}' -> {'接受' if dfa.accept(s) else '拒絕'}")

    print("\n--- NFA 範例：包含 'ab' 的字串 ---")
    nfa = NFA(
        states={0, 1, 2},
        alphabet={'a', 'b'},
        transition={
            (0, 'a'): {0, 1},
            (0, 'b'): {0},
            (1, 'b'): {2},
        },
        start=0,
        accepts={2},
    )
    for s in ["ab", "aab", "bab", "ba", "aa", "bb"]:
        print(f"  '{s}' -> {'接受' if nfa.accept(s) else '拒絕'}")

    print("\n--- 正則表達式引擎範例 ---")
    regex = RegexEngine("a(b|c)")
    for s in ["ab", "ac", "abc", "a", "b"]:
        print(f"  'a(b|c)' match '{s}' -> {regex.match(s)}")

    print("\n--- CFG 解析器範例：算術表達式 ---")
    for expr in ["3+4*5", "(3+4)*5", "1+2+3", "2*3*4"]:
        tokens = list(expr)
        try:
            parser = CFGParser(tokens)
            ast = parser.parse()
            val = calc_ast(ast)
            print(f"  '{expr}' = {val}  (AST: {ast})")
        except SyntaxError as e:
            print(f"  '{expr}' -> 語法錯誤: {e}")

    print("\n--- Turing Machine 範例：前導零移除 ---")
    tm = TuringMachine(
        transition={
            ('q0', '0'): ('q0', '_', 'R'),
            ('q0', '1'): ('q1', '1', 'R'),
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q1', '1', 'R'),
            ('q1', '_'): ('q2', '_', 'L'),
        },
        start='q0',
        accepts={'q2'},
    )
    for s in ["00101", "010", "100", "000", "1"]:
        result = tm.run(s)
        tape_str = ''.join(tm.tape).replace('_', '')
        print(f"  '{s}' -> 接受={result}, 磁帶='{tape_str}'")

    print("\n" + "=" * 50)
    print("展示完畢！")


if __name__ == '__main__':
    demo()
