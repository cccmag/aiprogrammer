#!/usr/bin/env python3
"""Automata: DFA and NFA implementation"""

class DFA:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def accept(self, input_string):
        state = self.q0
        for symbol in input_string:
            if symbol not in self.sigma:
                return False
            state = self.delta.get((state, symbol))
            if state is None:
                return False
        return state in self.F


class NFA:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in self.delta.get((state, ''), set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(self, states, symbol):
        result = set()
        for state in states:
            result.update(self.delta.get((state, symbol), set()))
        return result

    def accept(self, input_string):
        current = self.epsilon_closure({self.q0})
        for symbol in input_string:
            current = self.epsilon_closure(self.move(current, symbol))
        return bool(current & self.F)


def demo():
    print("=== DFA Demo ===")
    Q = {'q0', 'q1'}
    sigma = {'0', '1'}
    delta = {
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q1',
        ('q1', '0'): 'q0',
        ('q1', '1'): 'q1',
    }
    dfa = DFA(Q, sigma, delta, 'q0', {'q1'})
    tests = ['1', '0', '01', '10', '101', '100']
    for t in tests:
        print(f"DFA accepts '{t}': {dfa.accept(t)}")

    print("\n=== NFA Demo ===")
    Q = {'q0', 'q1', 'q2'}
    sigma = {'a', 'b'}
    delta = {
        ('q0', 'a'): {'q1'},
        ('q0', ''): {'q2'},
        ('q1', 'b'): {'q2'},
    }
    nfa = NFA(Q, sigma, delta, 'q0', {'q2'})
    for t in ['ab', 'aab', 'b', '']:
        print(f"NFA accepts '{t}': {nfa.accept(t)}")


if __name__ == "__main__": demo()