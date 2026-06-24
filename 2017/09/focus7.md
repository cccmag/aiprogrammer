# 強化學習應用案例

## 遊戲領域

### Atari 遊戲

DQN (2013) 在 Atari 遊戲上達到人類水準。

```python
# 使用 Baselines 的 DQN
from baselines import deepq

def callback(lcl, glb):
    pass

env = gym.make('Breakout-v0')

model = deepq.models.mlp([64, 64])

act = deepq.learn(
    env,
    q_func=model,
    num_actions=env.action_space.n,
    lr=1e-3,
    max_timesteps=10000000,
    buffer_size=50000,
    exploration_fraction=0.1,
    exploration_final_eps=0.01,
    print_freq=10,
    callback=callback
)

act.save("breakout_model.pkl")
env.close()
```

###圍棋

AlphaGo 結合深度學習與蒙地卡羅樹搜索。

```python
# 概念性圍棋 Agent
class GoAgent:
    def __init__(self):
        self.policy_network = load_policy_network()
        self.value_network = load_value_network()
        self.mcts = MonteCarloTreeSearch()

    def select_move(self, board_state):
        # 使用 MCTS + 神經網路選擇動作
        root = self.mcts.run(self.policy_network, board_state)
        return root.best_child().action

# AlphaGo Zero 的改進：從零學習，不使用人類棋譜
# 只有圍棋規則，透過自我對弈學習
```

### 星際爭霸 II

```python
# 使用 PySC2 (StarCraft II Learning Environment)
from pysc2.env import sc2_env
from pysc2.agents import base_agent

class MyAgent(base_agent.BaseAgent):
    def step(self, obs):
        # 根據觀察選擇動作
        return actions.FunctionCall(actions.FUNCTIONS.no_op())
```

## 機器人控制

### 機械手臂

```python
# 使用 PyBullet 或 Mujoco 模拟
import pybullet as p
import pybullet_envs

env = gym.make('FetchReach-v1')

obs = env.reset()
for _ in range(1000):
    action = env.action_space.sample()  # 或學習到的策略
    obs, reward, done, info = env.step(action)

    if done:
        obs = env.reset()

env.close()
```

### 雙足行走

```python
# BipedalWalker 環境
env = gym.make('BipedalWalker-v2')

# 使用的策略梯度方法
from stable_baselines import PPO2

model = PPO2('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=100000)

obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()

    if done:
        obs = env.reset()

env.close()
```

## 自駕車

### 端到端駕駛

```python
# 使用 CARLA 模擬器
# pip install carla

import carla

client = carla.Client('localhost', 2000)
world = client.get_world()

# 取得車輛
vehicle = world.get_actors().filter('vehicle.*')[0]

# 簡化的自動駕駛
def auto_drive(vehicle):
    # 獲取感測器數據
    camera_data = get_camera_data()

    # 使用學習到的策略控制
    action = policy_network.predict(camera_data)

    # 執行動作
    apply_control(vehicle, action)
```

### 車道保持

```python
# 使用 DeepRNN 或類似架構
class EndToEndDriving:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, Flatten, Dense, LSTM

        model = Sequential([
            Conv2D(32, (5, 5), activation='relu', input_shape=(66, 200, 3)),
            Conv2D(64, (3, 3), activation='relu'),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(256, activation='relu'),
            Dense(3)  # 轉角，油門，剎車
        ])
        return model
```

## 推薦系統

```python
# 強化學習推薦系統概念
class RecommenderAgent:
    def __init__(self, n_items, embedding_dim=64):
        self.embedding = np.random.randn(n_items, embedding_dim)
        self.policy = self.build_policy_network()

    def recommend(self, user_state, k=10):
        # 根據用戶狀態推薦 k 個項目
        scores = self.policy.predict(user_state)
        top_k = np.argsort(scores)[-k:]
        return top_k

    def update(self, user, item, feedback):
        # 根據用戶回饋更新策略
        # 正面回饋强化，負面回饋抑制
        pass
```

## 金融交易

```python
# 交易 Agent 概念
class TradingAgent:
    def __init__(self, state_dim, action_dim):
        self.q_network = self.build_network(state_dim, action_dim)

    def get_state(self, price_history, portfolio):
        # 組合價格歷史與投資組合狀態
        return np.concatenate([price_history, portfolio])

    def choose_action(self, state):
        # epsilon-greedy
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_dim)

        q_values = self.q_network.predict(state.reshape(1, -1))
        return np.argmax(q_values)

# 動作：0=持有, 1=買入, 2=賣出
```

## 資源管理

### 資料中心冷卻

DeepMind 使用 RL 優化資料中心冷卻能耗：

```python
# 概念性的冷卻控制 Agent
class CoolingAgent:
    def __init__(self, n_sensors, n_actuators):
        self.policy = build_policy_network(n_sensors, n_actuators)

    def sense(self, sensors):
        # 讀取溫度感測器
        return sensors

    def act(self, state):
        # 調整冷氣設定
        return self.policy.predict(state)
```

## 工業控制

```python
# 工業過程控制
class ProcessControlAgent:
    def __init__(self):
        self.model = load_process_model()  # 過程模型

    def control(self, measurements):
        # 測量：溫度、壓力、流量等
        # 動作：閥門開度、加熱功率等
        state = np.array(measurements)
        action = self.policy.predict(state)
        return action

# 使用 PP0 訓練
from stable_baselines import PPO2

env = gym.make('ProcessControl-v0')
model = PPO2('MlpPolicy', env)
model.learn(total_timesteps=50000)
```

## 對話系統

```python
# 對話策略學習
class DialogueAgent:
    def __init__(self, n_states, n_actions):
        self.q_network = np.zeros((n_states, n_actions))

    def respond(self, user_intent, dialogue_state):
        # 根據意圖和對話狀態選擇回覆
        state = self.encode(user_intent, dialogue_state)
        return self.choose_action(state)

    def learn(self, state, action, reward, next_state):
        # 從回饋中學習
        self.q_network[state, action] += 0.1 * (
            reward + 0.9 * np.max(self.q_network[next_state]) -
            self.q_network[state, action]
        )
```

## 總結

強化學習應用廣泛：
- **遊戲**：Atari、圍棋、StarCraft
- **機器人**：手臂控制、雙足行走
- **自駕車**：端到端駕駛
- **金融**：交易策略
- **工業**：資源調度、過程控制

這些應用展示 RL 從遊戲到現實世界的潛力。