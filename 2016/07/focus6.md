# 遊戲引擎架構

## 遊戲引擎概述

遊戲引擎是用於開發遊戲的軟體框架，提供渲染、物理、音效、輸入等核心功能。

### 主要元件

```
┌─────────────────────────────────────────┐
│               遊戲引擎                   │
├─────────────────────────────────────────┤
│  渲染系統   物理系統   音效系統   腳本系統 │
├─────────────────────────────────────────┤
│  場景管理   資源管理   輸入系統   網路系統 │
├─────────────────────────────────────────┤
│           核心基礎設施                   │
│     （記憶體、檔案、數學庫、編譯器）        │
└─────────────────────────────────────────┘
```

## 引擎元件系統

### 元件架構

現代遊戲引擎採用元件（Component）系統：

```cpp
class GameObject {
    std::vector<Component*> components;

public:
    void update(float deltaTime) {
        for (auto& comp : components) {
            comp->update(deltaTime);
        }
    }

    template<typename T>
    T* getComponent() {
        for (auto& comp : components) {
            if (auto result = dynamic_cast<T*>(comp))
                return result;
        }
        return nullptr;
    }

    void addComponent(Component* comp) {
        components.push_back(comp);
        comp->setOwner(this);
    }
};

class Transform : public Component {
public:
    vec3 position;
    quat rotation;
    vec3 scale;
};

class MeshRenderer : public Component {
public:
    Mesh* mesh;
    Material* material;
};

class RigidBody : public Component {
public:
    float mass;
    vec3 velocity;
};
```

### 場景圖

場景圖管理場景中所有物件的層次關係：

```cpp
class SceneNode {
public:
    Transform transform;
    SceneNode* parent;
    std::vector<SceneNode*> children;
    GameObject* object;

    void update(float deltaTime) {
        transform.update(deltaTime);
        for (auto child : children) {
            child->update(deltaTime);
        }
    }
};
```

## 渲染架構

### 前向渲染（Forward Rendering）

最簡單的渲染方式，每個物體單獨繪製：

```cpp
void forwardRender(Scene* scene, Camera* camera) {
    for (auto object : scene->getObjects()) {
        Shader* shader = object->getMaterial()->getShader();

        shader->use();
        shader->setMat4("uView", camera->getViewMatrix());
        shader->setMat4("uProjection", camera->getProjectionMatrix());
        shader->setMat4("uModel", object->getTransform()->getMatrix());

        object->getMesh()->draw();
    }
}
```

### 延遲渲染（Deferred Rendering）

先收集幾何資料，再計算光照：

```cpp
class DeferredRenderer {
    FrameBuffer geometryBuffer;

public:
    void geometryPass(Scene* scene) {
        geometryBuffer.bind();
        clear();

        for (auto object : scene->getObjects()) {
            renderGeometry(object);
        }

        geometryBuffer.unbind();
    }

    void lightingPass(Camera* camera) {
        for (auto light : scene->getLights()) {
            renderLight(light, camera);
        }
    }
};
```

### PBR 渲染管線

基於物理的渲染（PBR）提供更真實的光照：

```glsl
// PBR 片段著色器
vec3 calculatePBR(vec3 albedo, float metallic, float roughness,
                  vec3 normal, vec3 viewDir, vec3 lightDir) {
    vec3 F0 = mix(vec3(0.04), albedo, metallic);

    float NDF = distributionGGX(normal, viewDir, lightDir, roughness);
    float G = geometrySmith(normal, viewDir, lightDir, roughness);
    vec3 F = fresnelSchlick(max(dot(normal, viewDir), 0.0), F0);

    vec3 kS = F;
    vec3 kD = vec3(1.0) - kS;

    vec3 numerator = NDF * G * F;
    float denominator = 4.0 * max(dot(normal, viewDir), 0.0) *
                        max(dot(normal, lightDir), 0.0) + 0.0001;
    vec3 specular = numerator / denominator;

    float NdotL = max(dot(normal, lightDir), 0.0);
    return (kD * albedo / PI + specular) * lightColor * NdotL;
}
```

## 物理系統

### 碰撞檢測

```cpp
class CollisionSystem {
public:
    bool checkSphereSphere(Sphere* a, Sphere* b) {
        float distSq = lengthSq(a->position - b->position);
        float radiusSum = a->radius + b->radius;
        return distSq <= radiusSum * radiusSum;
    }

    bool checkBoxBox(Box* a, Box* b) {
        return (abs(a->center.x - b->center.x) < (a->halfExtents.x + b->halfExtents.x) &&
                abs(a->center.y - b->center.y) < (a->halfExtents.y + b->halfExtents.y) &&
                abs(a->center.z - b->center.z) < (a->halfExtents.z + b->halfExtents.z));
    }

    bool checkSphereBox(Sphere* sphere, Box* box) {
        vec3 closest = clamp(sphere->position, box->min(), box->max());
        float dist = length(sphere->position - closest);
        return dist < sphere->radius;
    }
};
```

### 物理模擬

```cpp
class RigidBody {
public:
    vec3 velocity;
    vec3 angularVelocity;
    float mass;
    float restitution;

    void applyForce(vec3 force) {
        velocity += force / mass;
    }

    void integrate(float dt) {
        position += velocity * dt;
        rotation += angularVelocity * dt;

        velocity *= 0.99f;
        angularVelocity *= 0.99f;
    }

    void collideWith(RigidBody* other) {
        vec3 normal = normalize(other->position - position);
        vec3 relVelocity = other->velocity - velocity;
        float velAlongNormal = dot(relVelocity, normal);

        if (velAlongNormal > 0) return;

        float e = min(restitution, other->restitution);
        float j = -(1 + e) * velAlongNormal;
        j /= 1/mass + 1/other->mass;

        velocity -= j / mass * normal;
        other->velocity += j / other->mass * normal;
    }
};
```

## 資源管理

### 資源載入

```cpp
class ResourceManager {
    std::unordered_map<std::string, Resource*> resources;

public:
    template<typename T>
    T* load(const std::string& path) {
        if (resources.find(path) != resources.end()) {
            return dynamic_cast<T*>(resources[path]);
        }

        Resource* res = loadResource<T>(path);
        resources[path] = res;
        return dynamic_cast<T*>(res);
    }

    Mesh* loadResource<Mesh>(const std::string& path) {
        // 載入模型檔案
    }

    Texture* loadResource<Texture>(const std::string& path) {
        // 載入紋理
    }
};
```

### 記憶體管理

```cpp
class MemoryPool {
    void* buffer;
    size_t offset;

public:
    void* allocate(size_t size, size_t alignment) {
        size_t current = (size_t)buffer + offset;
        size_t alignMask = alignment - 1;
        size_t aligned = (current + alignMask) & ~alignMask;

        offset = aligned - (size_t)buffer + size;
        return (void*)aligned;
    }

    void reset() {
        offset = 0;
    }
};
```

## 遊戲迴圈

```cpp
class GameEngine {
    bool running;

public:
    void run() {
        while (running) {
            float deltaTime = getDeltaTime();

            processInput();
            update(deltaTime);
            render();

            present();
        }
    }

    void update(float dt) {
        scene->update(dt);
        physicsSystem->update(dt);
        scriptSystem->update(dt);
    }
};
```

## 參考資料

- [遊戲引擎架構](https://www.google.com/search?q=game+engine+architecture+tutorial)
- [Unity 原始碼分析](https://www.google.com/search?q=Unity+engine+architecture+analysis)
- [實體元件系統](https://www.google.com/search?q=entity+component+system+game+development)