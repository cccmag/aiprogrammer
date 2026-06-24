#!/usr/bin/env python3
"""Regular Expression Engine using Thompson's Construction"""

class NFAFragment:
    def __init__(self, start, accept, transitions):
        self.start = start
        self.accept = accept
        self.transitions = transitions


def shunting_yard(regex):
    precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
    output = []
    stack = []

    for c in regex:
        if c.isalnum() or c == '#':
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[c]:
                output.append(stack.pop())
            stack.append(c)

    while stack:
        output.append(stack.pop())
    return output


def thompson(postfix):
    nfa_count = [0]

    def new_state():
        s = f"q{nfa_count[0]}"
        nfa_count[0] += 1
        return s

    stack = []
    transitions = {}

    for c in postfix:
        if c.isalnum():
            start, accept = new_state(), new_state()
            transitions[(start, c)] = {accept}
            stack.append(NFAFragment(start, accept, transitions))
        elif c == '*':
            frag = stack.pop()
            start, accept = new_state(), new_state()
            transitions[(start, '')] = {frag.start, accept}
            transitions[(frag.accept, '')] = {frag.start, accept}
            stack.append(NFAFragment(start, accept, transitions))
        elif c == '|':
            frag2 = stack.pop()
            frag1 = stack.pop()
            start, accept = new_state(), new_state()
            transitions[(start, '')] = {frag1.start, frag2.start}
            transitions[(frag1.accept, '')] = {accept}
            transitions[(frag2.accept, '')] = {accept}
            stack.append(NFAFragment(start, accept, transitions))
        elif c == '.':
            frag2 = stack.pop()
            frag1 = stack.pop()
            transitions[(frag1.accept, '')] = {frag2.start}
            stack.append(NFAFragment(frag1.start, frag2.accept, transitions))
        elif c == '?':
            frag = stack.pop()
            start, accept = new_state(), new_state()
            transitions[(start, '')] = {frag.start, accept}
            transitions[(frag.accept, '')] = {accept}
            stack.append(NFAFragment(start, accept, transitions))

    return stack.pop() if stack else None


class RegexNFA:
    def __init__(self, pattern):
        self.pattern = pattern
        self.postfix = shunting_yard(pattern)
        self.fragment = thompson(self.postfix)
        if self.fragment:
            self.start = self.fragment.start
            self.accept = self.fragment.accept
            self.transitions = self.fragment.transitions
            self.Q = set()
            for (s, _), targets in self.transitions.items():
                self.Q.add(s)
                self.Q.update(targets)
            self.sigma = set(c for c in pattern if c.isalnum())

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in self.transitions.get((state, ''), set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(self, states, symbol):
        result = set()
        for state in states:
            result.update(self.transitions.get((state, symbol), set()))
        return result

    def accept(self, input_string):
        if not self.fragment:
            return False
        current = self.epsilon_closure({self.start})
        for symbol in input_string:
            current = self.epsilon_closure(self.move(current, symbol))
        return self.accept in current


def demo():
    print("=== Regex Engine Demo ===")
    patterns = ['a*b', 'a+b', 'a?b', '(a|b)*', 'a*b+c']
    test_strings = ['', 'b', 'ab', 'aab', 'abc', 'aaab', 'abbc']

    for pattern in patterns:
        print(f"\nPattern: {pattern}")
        nfa = RegexNFA(pattern)
        for s in test_strings:
            result = nfa.accept(s)
            print(f"  '{s}': {'ACCEPT' if result else 'reject'}")


if __name__ == "__main__": demo()