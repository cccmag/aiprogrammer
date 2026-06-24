# 模擬器與真實環境

## Sim-to-Real 的鴻溝

RL 在模擬器中表現驚人，但部署到真實世界時往往失效。這是因為模擬器永遠無法完美建模真實物理——摩擦力、感測器雜訊、延遲、材質變形等。這個差距稱為 **Sim-to-Real Gap**。

## Domain Randomization

Domain Randomization（域隨機化）是最有效的 Sim-to-Real 技術之一。訓練時隨機化模擬器的參數，讓策略學會適應不確定性：

```python
import numpy as np
import gymnasium as gym

class DomainRandomizationWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self.friction_range = (0.5, 1.5)
        self.mass_range = (0.5, 2.0)

    def reset(self, **kwargs):
        # 隨機化物理參數
        friction = np.random.uniform(*self.friction_range)
        mass = np.random.uniform(*self.mass_range)
        # 透過 MuJoCo 的 MJCF 修改參數
        if hasattr(self.env.unwrapped, "model"):
            self.env.unwrapped.model.geom_friction[0, 0] = friction
            for body_id in range(self.env.unwrapped.model.nbody):
                self.env.unwrapped.model.body_mass[body_id] *= mass
        return self.env.reset(**kwargs)
```

## 更進階的技術

除了 Domain Randomization，還有幾種縮小 Sim-to-Real 差距的方法：

**System Identification**：在真實系統上採集數據，反向校準模擬器參數，讓模擬更貼近真實：

```python
def system_identification(real_trajectories, simulator_fn):
    def loss(params):
        sim_trajectories = simulator_fn(params)
        return np.mean((real_trajectories - sim_trajectories) ** 2)

    from scipy.optimize import minimize
    result = minimize(loss, initial_params, method="Nelder-Mead")
    return result.x
```

**Domain Adaptation**：利用對抗式訓練或風格轉換，讓模型學到跨域不變的特徵表示。這種方法在視覺領域特別有效。

**Progressive Net**：先在模擬器訓練，再用少量真實數據微調，保留模擬器學到的知識：

```python
class ProgressiveNet(nn.Module):
    def __init__(self, sim_pretrained):
        super().__init__()
        self.sim_layers = sim_pretrained.features
        self.real_layers = nn.Sequential(
            nn.Linear(512, 256), nn.ReLU(),
            nn.Linear(256, n_actions))

    def forward(self, x, is_real=False):
        features = self.sim_layers(x)
        return self.real_layers(features)
```

## 自動駕駛中的 Sim-to-Real

自動駕駛是 Sim-to-Real 最典型的應用場景。CARLA、MetaDrive、SMARTS 等模擬器為自動駕駛 RL 提供了安全的訓練環境：

```python
import metadrive

env = metadrive.MetaDriveEnv(
    config={"use_render": False, "start_seed": 0,
            "num_scenarios": 100})

obs, _ = env.reset()
for _ in range(1000):
    action = [0.0, 0.5]  # steering, throttle
    obs, reward, term, trunc, info = env.step(action)
    if term or trunc:
        obs, _ = env.reset()
env.close()
```

CARLA 更提供了完整的感測器套件（相機、LiDAR、GPS、IMU），讓 RL 策略可以在逼真的 urban driving 場景中訓練。

## 結語

Sim-to-Real 是 RL 實用化的最大瓶頸之一。Domain Randomization 是最務實的解法，但沒有銀彈。對於安全關鍵應用，模擬器訓練 + 真實世界微調 + 安全約束的組合是當前的最佳實踐。


**延伸閱讀**
- [Domain Randomization for Transferring Deep Neural Networks](https://www.google.com/search?q=Domain+Randomization+OpenAI+2017)
- [CARLA: An Open Urban Driving Simulator](https://www.google.com/search?q=CARLA+simulator+autonomous+driving)
- [MetaDrive: Composing Diverse Driving Scenarios](https://www.google.com/search?q=MetaDrive+driving+simulator+RL)
