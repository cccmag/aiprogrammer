# 狀態機在遊戲開發的應用

## 前言

遊戲開發中，狀態機是管理複雜遊戲邏輯的核心工具。從角色行為到遊戲狀態管理，FSM（Finite State Machine）提供了一種結構化、易於理解和維護的方式來處理遊戲中的各種狀態轉換。

## 遊戲狀態機基礎

### 簡單的遊戲狀態機

```python
from enum import Enum, auto

class GameState(Enum):
    TITLE = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class GameStateMachine:
    def __init__(self):
        self.current_state = GameState.TITLE
        self.transitions = {
            GameState.TITLE: {GameState.PLAYING},
            GameState.PLAYING: {GameState.PAUSED, GameState.GAME_OVER, GameState.VICTORY},
            GameState.PAUSED: {GameState.PLAYING, GameState.TITLE},
            GameState.GAME_OVER: {GameState.TITLE, GameState.PLAYING},
            GameState.VICTORY: {GameState.TITLE, GameState.PLAYING},
        }

    def can_transition(self, new_state):
        return new_state in self.transitions.get(self.current_state, set())

    def transition(self, new_state):
        if self.can_transition(new_state):
            print(f"Transitioning from {self.current_state.name} to {new_state.name}")
            self.current_state = new_state
            return True
        return False

    def update(self):
        pass


def demo_game_states():
    game = GameStateMachine()

    game.transition(GameState.PLAYING)
    game.transition(GameState.PAUSED)
    game.transition(GameState.PLAYING)
    game.transition(GameState.VICTORY)
    game.transition(GameState.TITLE)

demo_game_states()
```

## 角色行為狀態機

### 平台遊戲角色

```python
class PlayerState(Enum):
    IDLE = auto()
    RUNNING = auto()
    JUMPING = auto()
    FALLING = auto()
    ATTACKING = auto()
    HIT = auto()
    DEAD = auto()


class Player:
    def __init__(self):
        self.state = PlayerState.IDLE
        self.velocity_y = 0
        self.is_grounded = True
        self.health = 100
        self.facing_right = True

    def update(self, input_data):
        prev_state = self.state

        if self.health <= 0:
            self.state = PlayerState.DEAD
        elif self.state == PlayerState.DEAD:
            return

        if self.state == PlayerState.HIT:
            return

        # 攻擊優先
        if input_data.get('attack') and self.is_grounded:
            self.state = PlayerState.ATTACKING

        # 跳躍
        elif input_data.get('jump') and self.is_grounded:
            self.state = PlayerState.JUMPING
            self.velocity_y = -15
            self.is_grounded = False

        # 左右移動
        elif input_data.get('left') or input_data.get('right'):
            if self.is_grounded:
                self.state = PlayerState.RUNNING
            self.facing_right = input_data.get('right', False)

        # 空中
        elif not self.is_grounded:
            if self.velocity_y < 0:
                self.state = PlayerState.JUMPING
            else:
                self.state = PlayerState.FALLING

        # 預設閒置
        elif self.is_grounded:
            self.state = PlayerState.IDLE

        # 物理更新
        if not self.is_grounded:
            self.velocity_y += 1  # 重力
            if self.velocity_y > 0:
                self.state = PlayerState.FALLING

        # 狀態進入/離開處理
        if prev_state != self.state:
            self.on_state_exit(prev_state)
            self.on_state_enter(self.state)

    def on_state_enter(self, state):
        if state == PlayerState.ATTACKING:
            print("Player starts attacking!")
        elif state == PlayerState.JUMPING:
            print("Player jumps!")

    def on_state_exit(self, state):
        if state == PlayerState.ATTACKING:
            print("Player stops attacking!")

    def take_damage(self, amount):
        self.health -= amount
        if self.health > 0:
            self.state = PlayerState.HIT
        else:
            self.state = PlayerState.DEAD
            self.health = 0
```

## 敵方 AI 狀態機

```python
class EnemyState(Enum):
    PATROL = auto()
    CHASE = auto()
    ATTACK = auto()
    RETREAT = auto()
    IDLE = auto()


class EnemyAI:
    def __init__(self):
        self.state = EnemyState.PATROL
        self.patrol_points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        self.current_point = 0
        self.player_detected = False
        self.health = 50

    def update(self, player_pos, distance_to_player):
        prev_state = self.state

        # 狀態轉換邏輯
        if self.health < 20:
            self.state = EnemyState.RETREAT
        elif distance_to_player < 50:
            self.state = EnemyState.ATTACK
        elif distance_to_player < 200:
            self.state = EnemyState.CHASE
        else:
            self.state = EnemyState.PATROL

        if prev_state != self.state:
            self.on_state_change(prev_state, self.state)

    def on_state_change(self, from_state, to_state):
        print(f"Enemy: {from_state.name} -> {to_state.name}")

    def get_action(self):
        if self.state == EnemyState.PATROL:
            return self.patrol_action()
        elif self.state == EnemyState.CHASE:
            return self.chase_action()
        elif self.state == EnemyState.ATTACK:
            return self.attack_action()
        elif self.state == EnemyState.RETREAT:
            return self.retreat_action()
        return (0, 0)

    def patrol_action(self):
        target = self.patrol_points[self.current_point]
        print(f"Patrolling to {target}")
        return target

    def chase_action(self):
        print("Chasing player!")

    def attack_action(self):
        print("Attacking!")

    def retreat_action(self):
        print("Retreating to heal!")
```

## 層級狀態機（HFSM）

```python
class HierarchicalState:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = {}

    def add_child(self, child):
        child.parent = self
        self.children[child.name] = child

    def enter(self):
        print(f"Entering {self.name}")

    def exit(self):
        print(f"Exiting {self.name}")

    def update(self):
        print(f"Updating {self.name}")


class HierarchicalStateMachine:
    def __init__(self, root):
        self.root = root
        self.current = root

    def transition(self, state_name):
        if state_name in self.current.children:
            self.current.exit()
            self.current = self.current.children[state_name]
            self.current.enter()

    def update(self):
        self.current.update()
```

## 實用技巧

### 1. 狀態進入/離開鉤子

```python
def state_hooks():
    """每個狀態的進入和離開邏輯"""
    class Character:
        def __init__(self):
            self.states = {}

        def add_state(self, name, on_enter=None, on_update=None, on_exit=None):
            self.states[name] = {
                'enter': on_enter or (lambda: None),
                'update': on_update or (lambda: None),
                'exit': on_exit or (lambda: None),
            }

        def enter_state(self, name):
            if self.current_state in self.states:
                self.states[self.current_state]['exit']()
            self.current_state = name
            self.states[name]['enter']()

        def update(self):
            if self.current_state in self.states:
                self.states[self.current_state]['update']()

    char = Character()
    char.add_state('idle', on_enter=lambda: print("IDLE"))
    char.add_state('walk', on_enter=lambda: print("WALK"))

state_hooks()
```

### 2. 條件化轉換

```python
def conditional_transitions():
    """基於條件的狀態轉換"""
    class ConditionalTransition:
        def __init__(self, target, condition):
            self.target = target
            self.condition = condition

        def can_transition(self):
            return self.condition()

    transitions = {
        'idle': [ConditionalTransition('walk', lambda: True)],
        'walk': [ConditionalTransition('run', lambda: False)],
    }

    print("Conditional transitions defined")

conditional_transitions()
```

## 小結

狀態機是遊戲開發中不可或缺的工具。從簡單的遊戲狀態管理到複雜的 AI 行為，FSM 提供了一種直覺、可維護的方式來組織遊戲邏輯。理解正規語言和自動機理論，可以幫助我們更好地設計和實現這些狀態機。

---

**延伸閱讀**

- [Game Programming Patterns: State](https://www.google.com/search?q=game+programming+patterns+state)
- [Finite State Machines in Game Development](https://www.google.com/search?q=FSM+game+development+tutorial)
- [Behavior Trees vs FSM](https://www.google.com/search?q=behavior+trees+vs+finite+state+machine)