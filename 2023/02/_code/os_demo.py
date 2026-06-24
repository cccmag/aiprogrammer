#!/usr/bin/env python3
"""作業系統原理綜合展示"""

from collections import deque
import itertools

def demo():
    print("=" * 56)
    print("  作業系統原理展示")
    print("=" * 56)

    process_states_demo()
    cpu_scheduling_demo()
    page_replacement_demo()
    deadlock_detection_demo()

    print("\n所有展示完成。")

def process_states_demo():
    print("\n--- 1. 行程狀態轉換 ---")
    states = ["New", "Ready", "Running", "Waiting", "Terminated"]
    print("行程狀態模型：")
    for s in states:
        print(f"  □ {s}")
    print("\n狀態轉換序列：")
    transitions = [
        ("New", "Ready", "建立完成"),
        ("Ready", "Running", "排程器分派"),
        ("Running", "Waiting", "I/O 請求"),
        ("Waiting", "Ready", "I/O 完成"),
        ("Running", "Ready", "時間片到期"),
        ("Running", "Terminated", "執行完畢"),
    ]
    for src, dst, reason in transitions:
        print(f"  {src} ──[{reason}]──> {dst}")

def cpu_scheduling_demo():
    print("\n--- 2. CPU 排程演算法比較 ---")
    processes = [("P1", 0, 5), ("P2", 1, 3), ("P3", 2, 8), ("P4", 3, 2)]
    print("行程：到達時間 / 服務時間")
    for p, at, bt in processes:
        print(f"  {p}: 到達={at}, 服務時間={bt}")

    print("\nFCFS (先到先服務)：")
    fcfs_schedule(sorted(processes, key=lambda x: x[1]))
    print("\nSJF (最短工作優先)：")
    sjf_schedule(processes)
    print("\nRR (時間片輪轉, q=2)：")
    rr_schedule(processes, 2)

def fcfs_schedule(procs):
    time = 0
    total_wait = 0
    for p, at, bt in procs:
        if time < at:
            time = at
        wait = time - at
        total_wait += wait
        print(f"  {p} 等待={wait}, 開始={time}, 完成={time+bt}")
        time += bt
    print(f"  平均等待時間: {total_wait/len(procs):.1f}")

def sjf_schedule(procs):
    ready = []
    queue = sorted(procs, key=lambda x: x[1])
    time = 0
    total_wait = 0
    i = 0
    n = len(queue)
    while i < n or ready:
        while i < n and queue[i][1] <= time:
            ready.append(queue[i])
            i += 1
        if not ready:
            time = queue[i][1]
            continue
        ready.sort(key=lambda x: x[2])
        p, at, bt = ready.pop(0)
        wait = time - at
        total_wait += wait
        print(f"  {p} 等待={wait}, 開始={time}, 完成={time+bt}")
        time += bt
    print(f"  平均等待時間: {total_wait/len(procs):.1f}")

def rr_schedule(procs, quantum):
    n = len(procs)
    remaining = {p: bt for p, _, bt in procs}
    arrival = {p: at for p, at, _ in procs}
    last_run = {p: at for p, at, _ in procs}
    time = 0
    total_wait = 0
    completed = 0
    queue = deque()
    order = sorted(procs, key=lambda x: x[1])
    idx = 0
    while completed < n:
        while idx < n and order[idx][1] <= time:
            queue.append(order[idx][0])
            idx += 1
        if not queue:
            time = order[idx][1]
            continue
        p = queue.popleft()
        wait = time - last_run[p]
        total_wait += wait
        run = min(quantum, remaining[p])
        print(f"  {p} 等待 {wait}, 運行 {run}, 時間={time}-{time+run}", end="")
        remaining[p] -= run
        time += run
        last_run[p] = time
        if remaining[p] == 0:
            completed += 1
            print(" (完成)")
        else:
            print()
            while idx < n and order[idx][1] <= time:
                queue.append(order[idx][0])
                idx += 1
            queue.append(p)
    print(f"  平均等待時間: {total_wait/n:.1f}")

def page_replacement_demo():
    print("\n--- 3. 頁面置換演算法 (3 個框架) ---")
    ref = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7]
    print(f"參照序列: {ref}")
    for algo, fn in [("FIFO", fifo), ("LRU", lru), ("OPT", opt)]:
        faults = fn(ref, 3)
        print(f"  {algo}: {faults} 次頁面錯誤")

def fifo(ref, frames):
    mem = []
    faults = 0
    for page in ref:
        if page not in mem:
            if len(mem) >= frames:
                mem.pop(0)
            mem.append(page)
            faults += 1
    return faults

def lru(ref, frames):
    mem = []
    faults = 0
    for page in ref:
        if page in mem:
            mem.remove(page)
        else:
            if len(mem) >= frames:
                mem.pop(0)
            faults += 1
        mem.append(page)
    return faults

def opt(ref, frames):
    mem = []
    faults = 0
    for i, page in enumerate(ref):
        if page not in mem:
            if len(mem) >= frames:
                farthest = -1
                victim = -1
                for m in mem:
                    try:
                        pos = ref.index(m, i+1)
                    except ValueError:
                        pos = len(ref)
                    if pos > farthest:
                        farthest = pos
                        victim = m
                mem.remove(victim)
            mem.append(page)
            faults += 1
    return faults

def deadlock_detection_demo():
    print("\n--- 4. 死結偵測 (銀行家演算法) ---")
    processes = ["P0", "P1", "P2", "P3", "P4"]
    alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    max_need = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    avail = [3, 3, 2]
    print(f"行程數量: {len(processes)}")
    print(f"資源類型: A(3), B(5), C(2)")
    print(f"可用資源: {avail}")
    print(f"\n各行程分配/最大需求:")
    for i, p in enumerate(processes):
        print(f"  {p}: 分配={alloc[i]}, 最大={max_need[i]}")

    safe, seq = bankers(processes, alloc, max_need, avail)
    if safe:
        print(f"\n系統處於安全狀態。安全序列: {' → '.join(seq)}")
    else:
        print(f"\n系統處於不安全狀態！")

    print("\n死結條件偵測：")
    print("  1. 互斥等待：共享資源互斥存取")
    print("  2. 持有等待：行程持有資源同時請求其他資源")
    print("  3. 不可搶占：資源只能由持有行程釋放")
    print("  4. 循環等待：行程間形成環狀依賴")

def bankers(processes, alloc, max_need, avail):
    n = len(processes)
    m = len(avail)
    need = [[max_need[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    work = avail[:]
    finish = [False] * n
    seq = []
    while len(seq) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += alloc[i][j]
                finish[i] = True
                seq.append(processes[i])
                found = True
        if not found:
            return False, seq
    return True, seq

if __name__ == "__main__":
    demo()
