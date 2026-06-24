# 資料導向設計

## 什麼是資料導向設計？

資料導向設計（Data-Oriented Design）是一種最佳化記憶體訪問模式的程式設計方法。

## 與物件導向的對比

### 物件導向：資料和行為分開

```c++
// 物件導向
class Entity {
    Vector3 position;
    Vector3 velocity;
    float health;
    float damage;
    void update();
    void render();
};

std::vector<Entity> entities;  // 同一類型的物件連續儲存

// 但不同型別的資料交錯儲存
// position, velocity, health, damage, position, velocity, ...
```

### 資料導向：相同類型的資料連續儲存

```c++
// 資料導向
struct Positions { std::vector<Vector3> data; };
struct Velocities { std::vector<Vector3> data; };
struct Healths { std::vector<float> data; };

Positions positions;
Velocities velocities;
Healths healths;

// 所有位置連續儲存
// 所有速度連續儲存
// 所有生命值連續儲存
```

## 範例：粒子系統

### 物件導向版本

```c++
struct ParticleOO {
    float x, y, z;      // 12 位元組
    float vx, vy, vz;   // 12 位元組
    float life;         // 4 位元組
    bool active;        // 1 位元組 + 3 padding
};
// 總共 32 位元組

std::vector<ParticleOO> particles;
```

### 資料導向版本

```c++
struct ParticlesDOD {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;
    std::vector<float> life;
    std::vector<char> active;
};
// 每個陣列自己的資料連續儲存
```

## 快取命中

### 假設場景：更新所有粒子

```c++
// 物件導向：跳躍式訪問
for (auto& p : particles) {
    if (p.active) {
        p.x += p.vx;
        p.y += p.vy;
        p.z += p.vz;
        p.life -= dt;
    }
}
// 每次訪問：x, y, z, vx, vy, vz, life... 不是連續的！
// 快取命中率低

// 資料導向：順序訪問
for (int i = 0; i < n; i++) {
    if (active[i]) {
        x[i] += vx[i];
        y[i] += vy[i];
        z[i] += vz[i];
        life[i] -= dt;
    }
}
// 只有同類型資料接續儲存
// 快取命中率高
```

## 結構整併（Structure of Arrays）

```c++
// SoA：同類型資料放在一起
struct ParticlesSoA {
    float* x, * y, * z;
    float* vx, * vy, * vz;
    float* life;
    char* active;
};

// 更好：連續配置
struct ParticleBlock {
    float x[MAX_PARTICLES];
    float y[MAX_PARTICLES];
    float z[MAX_PARTICLES];
    float vx[MAX_PARTICLES];
    float vy[MAX_PARTICLES];
    float vz[MAX_PARTICLES];
    float life[MAX_PARTICLES];
    char active[MAX_PARTICLES];
};
```

## 熱/冷資料分離

```c++
// 不好：熱門和冷門資料混合
struct Entity {
    float position[3];    // 經常訪問（熱）
    float velocity[3];     // 經常訪問（熱）
    float health;          // 經常訪問（熱）
    char name[256];        // 很少訪問（冷）
    std::vector<History> history;  // 很少訪問（冷）
};

// 好：分開儲存
struct EntityHot {
    float position[3];
    float velocity[3];
    float health;
};

struct EntityCold {
    char name[256];
    std::vector<History> history;
};
```

## 應用場景

1. **遊戲引擎**：Entity Component System (ECS)
2. **科學計算**：大型陣列運算
3. **資料庫**：列式儲存
4. **網路協定**：封包處理

## 參考資料

- [資料導向設計](https://www.google.com/search?q=data-oriented+design+tutorial)
- [SOA vs AOS](https://www.google.com/search?q=structure+of+arrays+vs+array+of+structures)