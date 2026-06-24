# 光線追蹤入門

## 光線追蹤基礎

光線追蹤是一種模擬光線傳播的渲染技術，可以產生真實的光照效果。

## 核心演算法

```cpp
Color traceRay(Ray ray, Scene* scene, int depth) {
    if (depth > MAX_DEPTH) return BLACK;

    Hit hit;
    if (!scene->intersect(ray, &hit)) {
        return scene->getBackground();
    }

    vec3 viewDir = -normalize(ray.direction);
    vec3 lightDir = normalize(scene->getLightDir());
    vec3 reflectDir = reflect(ray.direction, hit.normal);

    float diff = max(dot(hit.normal, lightDir), 0.0);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), hit.material.shininess);

    Color ambient = hit.material.ambient * scene->getAmbientLight();
    Color diffuse = hit.material.diffuse * diff * scene->getLightColor();
    Color specular = hit.material.specular * spec * scene->getLightColor();

    Color localColor = ambient + diffuse + specular;

    Ray reflectedRay = { hit.position + hit.normal * EPSILON, reflectDir };
    Color reflectedColor = traceRay(reflectedRay, scene, depth + 1);

    float reflectivity = hit.material.reflectivity;
    return localColor * (1.0 - reflectivity) + reflectedColor * reflectivity;
}
```

## 光線-球體相交

```cpp
bool intersectSphere(Ray ray, Sphere* sphere, Hit* hit) {
    vec3 oc = ray.origin - sphere->center;
    float a = dot(ray.direction, ray.direction);
    float b = 2.0 * dot(oc, ray.direction);
    float c = dot(oc, oc) - sphere->radius * sphere->radius;
    float disc = b * b - 4 * a * c;

    if (disc < 0) return false;

    float t = (-b - sqrt(disc)) / (2.0 * a);
    if (t < 0) t = (-b + sqrt(disc)) / (2.0 * a);
    if (t < 0) return false;

    hit->t = t;
    hit->position = ray.origin + ray.direction * t;
    hit->normal = normalize(hit->position - sphere->center);
    hit->material = sphere->material;

    return true;
}
```

## 光線-三角形相交

```cpp
bool intersectTriangle(Ray ray, Triangle* tri, Hit* hit) {
    vec3 edge1 = tri->v1 - tri->v0;
    vec3 edge2 = tri->v2 - tri->v0;
    vec3 h = cross(ray.direction, edge2);
    float a = dot(edge1, h);

    if (abs(a) < EPSILON) return false;

    float f = 1.0 / a;
    vec3 s = ray.origin - tri->v0;
    float u = f * dot(s, h);

    if (u < 0.0 || u > 1.0) return false;

    vec3 q = cross(s, edge1);
    float v = f * dot(ray.direction, q);

    if (v < 0.0 || u + v > 1.0) return false;

    float t = f * dot(edge2, q);

    if (t > EPSILON) {
        hit->t = t;
        hit->position = ray.origin + ray.direction * t;
        hit->normal = normalize(cross(edge1, edge2));
        hit->material = tri->material;
        return true;
    }

    return false;
}
```

## 陰影射線

```cpp
bool isInShadow(vec3 point, Scene* scene) {
    vec3 lightDir = normalize(scene->getLightDir());
    Ray shadowRay = { point + lightDir * EPSILON, lightDir };

    for (auto object : scene->getObjects()) {
        Hit hit;
        if (object->intersect(shadowRay, &hit)) {
            return true;
        }
    }
    return false;
}
```

## 參考資料

- [光線追蹤演算法](https://www.google.com/search?q=ray+tracing+algorithm+explained)
- [即時光線追蹤](https://www.google.com/search?q=real+time+ray+tracing+tutorial)