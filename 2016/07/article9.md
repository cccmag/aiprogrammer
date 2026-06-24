# 物理引擎基礎

## 物理引擎概述

物理引擎模擬現實世界的物理規律，包括碰撞檢測、剛體動力學和軟體物理。

## 剛體動力學

```cpp
class RigidBody {
public:
    vec3 position;
    vec3 velocity;
    vec3 angularVelocity;
    vec3 acceleration;
    vec3 angularAcceleration;

    float mass;
    float inverseMass;
    mat3 inertia;
    mat3 inverseInertia;

    void applyForce(vec3 force) {
        acceleration += force * inverseMass;
    }

    void applyTorque(vec3 torque) {
        angularAcceleration += inverseInertia * torque;
    }

    void integrate(float dt) {
        position += velocity * dt + 0.5f * acceleration * dt * dt;
        velocity += acceleration * dt;

        vec3 angle = angularVelocity * dt + 0.5f * angularAcceleration * dt * dt;
        orientation = orientation * quaternionFromAxisAngle(angle);

        velocity *= (1.0f - linearDamping);
        angularVelocity *= (1.0f - angularDamping);
    }
};
```

## 碰撞檢測

### 球體-球體碰撞

```cpp
bool checkSphereSphere(Sphere* a, Sphere* b, Contact* contact) {
    vec3 delta = b->position - a->position;
    float distSq = dot(delta, delta);
    float radiusSum = a->radius + b->radius;

    if (distSq < radiusSum * radiusSum) {
        float dist = sqrt(distSq);
        contact->normal = delta / dist;
        contact->penetration = radiusSum - dist;
        contact->point = a->position + contact->normal * a->radius;
        return true;
    }
    return false;
}
```

### AABB 碰撞檢測

```cpp
struct AABB {
    vec3 min;
    vec3 max;
};

bool checkAABB(AABB* a, AABB* b) {
    if (a->max.x < b->min.x || a->min.x > b->max.x) return false;
    if (a->max.y < b->min.y || a->min.y > b->max.y) return false;
    if (a->max.z < b->min.z || a->min.z > b->max.z) return false;
    return true;
}
```

## 碰撞響應

```cpp
void resolveCollision(RigidBody* a, RigidBody* b, Contact* contact) {
    vec3 relVel = b->velocity - a->velocity;
    float velAlongNormal = dot(relVel, contact->normal);

    if (velAlongNormal > 0) return;

    float e = min(a->restitution, b->restitution);
    float j = -(1.0f + e) * velAlongNormal;
    j /= a->inverseMass + b->inverseMass;

    vec3 impulse = contact->normal * j;
    a->velocity -= impulse * a->inverseMass;
    b->velocity += impulse * b->inverseMass;

    vec3 tangental = relVel - contact->normal * velAlongNormal;
    float friction = 0.5f;
    vec3 frictionImpulse = tangental * friction * j;
    a->velocity -= frictionImpulse * a->inverseMass;
    b->velocity += frictionImpulse * b->inverseMass;
}
```

## 碰撞約束

```cpp
class DistanceConstraint {
public:
    RigidBody* a;
    RigidBody* b;
    float targetDistance;

    void solve() {
        vec3 delta = b->position - a->position;
        float currentDist = length(delta);
        vec3 normal = delta / currentDist;

        float error = currentDist - targetDistance;
        vec3 correction = normal * error * 0.5f;

        a->position += correction;
        b->position -= correction;
    }
};
```

## 參考資料

- [物理引擎程式設計](https://www.google.com/search?q=physics+engine+programming+tutorial)
- [碰撞檢測演算法](https://www.google.com/search?q=collision+detection+algorithms)