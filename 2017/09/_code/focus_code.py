#!/usr/bin/env python3
"""強化學習示範"""

def demo():
    print("=" * 50)
    print("強化學習示範")
    print("=" * 50)

    print("\n1. 強化學習核心概念:")
    print("   Agent（代理人）")
    print("   Environment（環境）")
    print("   State（狀態）")
    print("   Action（動作）")
    print("   Reward（獎賞）")

    print("\n2. Q-learning 更新規則:")
    print("   Q(s,a) ← Q(s,a) + α[r + γmax Q(s',a') - Q(s,a)]")

    print("\n3. Exploration vs Exploitation:")
    print("   ε-greedy: ε 機率隨機，否則貪心")

    print("\n4. DQN 核心技術:")
    print("   - 經驗回放 (Experience Replay)")
    print("   - 目標網路 (Target Network)")

    print("\n5. Policy Gradient:")
    print("   直接優化策略 π(a|s)")
    print("   梯度: ∇J = E[∇log π(a|s) × Q(s,a)]")

    print("\n6. Actor-Critic:")
    print("   Actor: 策略網路（選擇動作）")
    print("   Critic: 價值網路（評估好壞）")

    print("\n" + "=" * 50)
    print("強化學習示範完成")
    print("=" * 50)

if __name__ == "__main__":
    demo()