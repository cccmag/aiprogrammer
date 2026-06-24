# 程式化內容生成：演算法與 Rust 實作

## 1. 引言

程式化內容生成（Procedural Content Generation, PCG）在現代遊戲開發中扮演重要角色——從 Minecraft 的地形到《星露谷物語》的地圖。Rust 的效能和安全性使其成為實作 PCG 演算法的理想語言。

## 2. Perlin / Simplex 噪聲

### 2.1 核心概念

Perlin 噪聲由 Ken Perlin 於 1983 年發明，用於產生自然的偽隨機紋理。Simplex 噪聲是其改進版本，效率更高且方向性偽影更少。

### 2.2 Rust 實作

```rust
use rand::Rng;

#[derive(Clone)]
struct PerlinNoise {
    perm: [usize; 512],
    gradients: [(f32, f32); 256],
}

impl PerlinNoise {
    fn new(seed: u64) -> Self {
        let mut rng = rand::rngs::StdRng::seed_from_u64(seed);
        let gradients: [(f32, f32); 256] = std::array::from_fn(|_| {
            let angle = rng.gen::<f32>() * std::f32::consts::TAU;
            (angle.cos(), angle.sin())
        });
        let mut perm: [usize; 256] = std::array::from_fn(|i| i);
        for i in (1..256).rev() {
            let j = rng.gen_range(0..=i);
            perm.swap(i, j);
        }
        let mut full_perm = [0usize; 512];
        for i in 0..512 {
            full_perm[i] = perm[i & 255];
        }
        Self { perm: full_perm, gradients }
    }

    fn fade(t: f32) -> f32 { t * t * t * (t * (t * 6.0 - 15.0) + 10.0) }
    fn lerp(a: f32, b: f32, t: f32) -> f32 { a + t * (b - a) }

    fn dot(g: (f32, f32), x: f32, y: f32) -> f32 { g.0 * x + g.1 * y }

    fn noise(&self, x: f32, y: f32) -> f32 {
        let xi = x.floor() as i32 & 255;
        let yi = y.floor() as i32 & 255;
        let xf = x - x.floor();
        let yf = y - y.floor();
        let u = Self::fade(xf);
        let v = Self::fade(yf);

        let aa = self.perm[self.perm[xi as usize] + yi as usize];
        let ab = self.perm[self.perm[xi as usize] + (yi + 1) as usize];
        let ba = self.perm[self.perm[(xi + 1) as usize] + yi as usize];
        let bb = self.perm[self.perm[(xi + 1) as usize] + (yi + 1) as usize];

        let x1 = Self::lerp(
            Self::dot(self.gradients[aa], xf, yf),
            Self::dot(self.gradients[ba], xf - 1.0, yf),
            u,
        );
        let x2 = Self::lerp(
            Self::dot(self.gradients[ab], xf, yf - 1.0),
            Self::dot(self.gradients[bb], xf - 1.0, yf - 1.0),
            u,
        );
        Self::lerp(x1, x2, v)
    }
}
```

### 2.3 多倍頻疊加（Octave Layering）

真實地形需要疊加不同頻率的噪聲：

```rust
struct FractalNoise {
    base: PerlinNoise,
    octaves: u32,
    persistence: f32,
    lacunarity: f32,
}

impl FractalNoise {
    fn sample(&self, x: f32, y: f32) -> f32 {
        let mut value = 0.0;
        let mut amp = 1.0;
        let mut freq = 1.0;
        let mut max_amp = 0.0;

        for _ in 0..self.octaves {
            value += amp * self.base.noise(x * freq, y * freq);
            max_amp += amp;
            amp *= self.persistence;
            freq *= self.lacunarity;
        }
        value / max_amp
    }
}
```

## 3. BSP 地牢生成

二元空間分割（BSP）演算法適合產生連通的地牢關卡：

```rust
struct BSPNode {
    x: i32, y: i32, w: i32, h: i32,
    left: Option<Box<BSPNode>>,
    right: Option<Box<BSPNode>>,
    room: Option<Rect>,
}

fn split_node(node: &mut BSPNode, min_size: i32, rng: &mut impl Rng) {
    if node.w < min_size * 2 || node.h < min_size * 2 { return; }

    let horizontal = if node.w > node.h && node.w as f32 / node.h as f32 > 1.25 {
        false
    } else if node.h > node.w && node.h as f32 / node.w as f32 > 1.25 {
        true
    } else { rng.gen_bool(0.5) };

    let max = (if horizontal { node.h } else { node.w }) - min_size;
    let split = rng.gen_range(min_size..=max);

    if horizontal {
        node.left = Some(Box::new(BSPNode { x: node.x, y: node.y, w: node.w, h: split, left: None, right: None, room: None }));
        node.right = Some(Box::new(BSPNode { x: node.x, y: node.y + split, w: node.w, h: node.h - split, left: None, right: None, room: None }));
    } else {
        // 垂直分割，邏輯類似
    }
}
```

## 4. Wave Function Collapse

WFC 演算法從輸入樣例推斷區域性規則，生成全域性地圖：

```rust
use ndarray::Array2;
use std::collections::HashSet;

struct WFCSolver {
    grid: Array2<HashSet<usize>>,   // 每個格子的可能候選
    patterns: Vec<Array2<u8>>,      // 輸入樣例的 3×3 模式
}

impl WFCSolver {
    fn observe(&mut self) -> Option<(usize, usize)> {
        // 找到熵最低的格子
        let mut min_entropy = f32::MAX;
        let mut target = None;
        for idx in 0..self.grid.len() {
            let n = self.grid.as_slice().unwrap()[idx].len();
            if n > 1 {
                let entropy = (n as f32).ln();
                if entropy < min_entropy {
                    min_entropy = entropy;
                    target = Some(idx);
                }
            }
        }
        // 隨機坍縮該格子
        if let Some(idx) = target {
            let i = idx / self.grid.shape()[1];
            let j = idx % self.grid.shape()[1];
            Some((i, j))
        } else { None }
    }

    fn propagate(&mut self, x: usize, y: usize) {
        // 根據已坍縮的格子移除相鄰格子的矛盾候選
        // 包含相容性檢查和遞迴約束傳播
    }
}
```

## 5. L-Systems（林氏系統）

L-System 利用字串重寫規則產生有機結構，適合生成植被或建築：

```rust
struct LSystem {
    axiom: String,
    rules: Vec<(char, String)>,
    angle: f32,
}

impl LSystem {
    fn generate(&self, iterations: u32) -> String {
        let mut current = self.axiom.clone();
        for _ in 0..iterations {
            current = current.chars().map(|c| {
                self.rules.iter()
                    .find(|(k, _)| *k == c)
                    .map(|(_, v)| v.as_str())
                    .unwrap_or_else(|| c.to_string().leak())
                    .to_string()
            }).collect();
        }
        current
    }

    fn interpret(&self, instructions: &str) -> Vec<(f32, f32)> {
        // F: 前進並畫線，+: 左轉，-: 右轉，[: 推入狀態，]: 彈出狀態
        let mut segments = Vec::new();
        let mut pos = (0.0f32, 0.0f32);
        let mut dir = 90.0f32.to_radians();
        let mut stack = Vec::new();

        for c in instructions.chars() {
            match c {
                'F' => {
                    let new_pos = (pos.0 + dir.cos(), pos.1 + dir.sin());
                    segments.push((pos, new_pos));
                    pos = new_pos;
                }
                '+' => dir += self.angle.to_radians(),
                '-' => dir -= self.angle.to_radians(),
                '[' => stack.push((pos, dir)),
                ']' => { let (p, d) = stack.pop().unwrap(); pos = p; dir = d; }
                _ => {}
            }
        }
        segments
    }
}
```

## 6. Bevy 整合

將 PCG 產出的地圖資料轉換為 Bevy 實體：

```rust
fn spawn_pcg_map(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    noise: Res<FractalNoise>,
) {
    for x in -10..10 {
        for y in -10..10 {
            let height = noise.sample(x as f32 * 0.1, y as f32 * 0.1);
            let tile = if height > 0.3 {
                TileType::Ground
            } else if height > 0.0 {
                TileType::Water
            } else {
                TileType::DeepWater
            };
            spawn_tile(&mut commands, &mut meshes, &mut materials, x, y, tile);
        }
    }
}
```

## 7. 結語

PCG 是一門結合數學和藝術的學問。Rust 的型別系統和效能讓開發者可以實作高品質的 PCG 演算法，而 Bevy 的 ECS 架構則讓動態生成內容的管理變得優雅。

## 延伸閱讀

- [Perlin noise algorithm](https://www.google.com/search?q=Perlin+noise+algorithm+explanation)
- [Wave Function Collapse](https://www.google.com/search?q=wave+function+collapse+procedural+generation)
- [BSP dungeon generation](https://www.google.com/search?q=BSP+dungeon+generation+algorithm)
- [L-Systems for procedural generation](https://www.google.com/search?q=L-Systems+procedural+generation)
