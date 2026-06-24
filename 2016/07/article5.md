# 延遲渲染技術

## 延遲渲染概述

延遲渲染（Deferred Rendering）是一種分階段的渲染技術，先收集幾何資料，再進行光照計算。

## G-Buffer 結構

| 紋理 | 格式 | 內容 |
|-----|------|------|
| Position | RGBA32F | 世界座標 |
| Normal | RGBA16F | 法向量（視角空間） |
| Albedo | RGBA8 | 漫反射顏色 |
| PBR | RGBA8 | 金屬度、粗糙度 |

## 幾何通道

```cpp
class GBuffer {
public:
    enum TextureType {
        GB_POSITION,
        GB_NORMAL,
        GB_ALBEDO,
        GB_PBR,
        GB_DEPTH,
        GB_COUNT
    };

    FrameBuffer frameBuffer;
    Texture2D textures[GB_COUNT];

    void bind() {
        frameBuffer.bind();
        Texture::bindTextures(textures, GB_COUNT);
    }
};

void geometryPass(GBuffer& gbuffer, Scene* scene) {
    gbuffer.bind();
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    for (auto object : scene->getObjects()) {
        renderGeometry(object);
    }
}
```

## 光照通道

```cpp
void lightingPass(GBuffer& gbuffer, Scene* scene, Camera* cam) {
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    for (auto light : scene->getLights()) {
        if (light->type == LIGHT_POINT) {
            renderPointLight(gbuffer, light, cam);
        }
    }
}
```

## 光照計算

```glsl
vec3 calculateDirectionalLight(
    vec3 lightDir,
    vec3 lightColor,
    vec3 albedo,
    float metallic,
    float roughness,
    vec3 normal,
    vec3 viewDir
) {
    vec3 F0 = mix(vec3(0.04), albedo, metallic);

    float NdotL = max(dot(normal, lightDir), 0.0);
    vec3 radiance = lightColor * NdotL;

    vec3 F = fresnelSchlick(max(dot(normal, viewDir), 0.0), F0);
    vec3 kS = F;
    vec3 kD = 1.0 - kS;

    vec3 diffuse = kD * albedo / PI;

    return diffuse * radiance;
}
```

## 透明物體處理

```cpp
void renderTransparentObjects(Scene* scene) {
    sortTransparentObjects(scene);

    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    for (auto object : scene->getTransparentObjects()) {
        renderForward(object);
    }

    glDisable(GL_BLEND);
}
```

## 參考資料

- [延遲渲染詳解](https://www.google.com/search?q=deferred+rendering+tutorial)
- [G-Buffer 設計](https://www.google.com/search?q=G-Buffer+design+deferred+rendering)