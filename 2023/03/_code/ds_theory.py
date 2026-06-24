class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder(self):
        r = []
        self._inorder(self.root, r)
        return r

    def _inorder(self, n, r):
        if n:
            self._inorder(n.left, r)
            r.append(n.key)
            self._inorder(n.right, r)


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None

    def _h(self, n):
        return n.height if n else 0

    def _bf(self, n):
        return self._h(n.left) - self._h(n.right) if n else 0

    def _rr(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        y.height = 1 + max(self._h(y.left), self._h(y.right))
        x.height = 1 + max(self._h(x.left), self._h(x.right))
        return x

    def _rl(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        x.height = 1 + max(self._h(x.left), self._h(x.right))
        y.height = 1 + max(self._h(y.left), self._h(y.right))
        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, n, key):
        if n is None:
            return AVLNode(key)
        if key < n.key:
            n.left = self._insert(n.left, key)
        elif key > n.key:
            n.right = self._insert(n.right, key)
        else:
            return n
        n.height = 1 + max(self._h(n.left), self._h(n.right))
        b = self._bf(n)
        if b > 1 and key < n.left.key:
            return self._rr(n)
        if b < -1 and key > n.right.key:
            return self._rl(n)
        if b > 1 and key > n.left.key:
            n.left = self._rl(n.left)
            return self._rr(n)
        if b < -1 and key < n.right.key:
            n.right = self._rr(n.right)
            return self._rl(n)
        return n

    def inorder(self):
        r = []
        self._inorder(self.root, r)
        return r

    def _inorder(self, n, r):
        if n:
            self._inorder(n.left, r)
            r.append(n.key)
            self._inorder(n.right, r)


class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, []).append(u)

    def bfs(self, start):
        visited = {start}
        queue = [start]
        result = []
        while queue:
            v = queue.pop(0)
            result.append(v)
            for nb in self.adj.get(v, []):
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return result

    def dfs(self, start):
        visited = set()
        result = []
        self._dfs(start, visited, result)
        return result

    def _dfs(self, v, visited, result):
        visited.add(v)
        result.append(v)
        for nb in self.adj.get(v, []):
            if nb not in visited:
                self._dfs(nb, visited, result)


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, val):
        i = self._hash(key)
        for p in self.table[i]:
            if p[0] == key:
                p[1] = val
                return
        self.table[i].append([key, val])

    def get(self, key):
        i = self._hash(key)
        for p in self.table[i]:
            if p[0] == key:
                return p[1]
        return None

    def remove(self, key):
        i = self._hash(key)
        self.table[i] = [p for p in self.table[i] if p[0] != key]


def demo():
    print("=== BST ===")
    bst = BST()
    for k in [5, 3, 7, 2, 4, 8]:
        bst.insert(k)
    print("Inorder:", bst.inorder())
    print("Search 4:", bst.search(4).key if bst.search(4) else None)
    print("Search 9:", bst.search(9))

    print("\n=== AVL ===")
    avl = AVL()
    for k in [10, 20, 30, 40, 50, 25]:
        avl.insert(k)
    print("Inorder:", avl.inorder())

    print("\n=== Graph BFS / DFS ===")
    g = Graph()
    for u, v in [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]:
        g.add_edge(u, v)
    print("BFS from 1:", g.bfs(1))
    print("DFS from 1:", g.dfs(1))

    print("\n=== Hash Table ===")
    ht = HashTable()
    ht.insert("name", "Alice")
    ht.insert("age", 30)
    ht.insert("city", "Tokyo")
    print("name:", ht.get("name"))
    print("age:", ht.get("age"))
    ht.remove("age")
    print("age after remove:", ht.get("age"))


if __name__ == "__main__":
    demo()
