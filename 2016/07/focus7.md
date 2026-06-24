# 效能優化與陰影

## 效能優化策略

### 減少 Draw Call

Draw call 是 CPU 呼叫 GPU 繪製的命令。過多的 draw call 會成為效能瓶頸。

**批次渲染（Batching）**

```cpp
class BatchRenderer {
    std::vector<RenderCommand> commands;

public:
    void addToBatch(GameObject* obj) {
        // 按材質分組
        Material* mat = obj->getMaterial();
        commands.push_back({ obj->getMesh(), mat });
    }

    void renderBatched() {
        Material* currentMat = nullptr;

        for (auto& cmd : commands) {
            if (cmd.material != currentMat) {
                if (currentMat) currentMat->unbind();
                currentMat = cmd.material;
                currentMat->bind();
            }
            cmd.mesh->draw();
        }
    }
};
```

**GPU Instancing**

```cpp
// 繪製多個實例
glDrawElementsInstanced(
    GL_TRIANGLES,
    indexCount,
    GL_UNSIGNED_INT,
    0,
    instanceCount
);
```

```glsl
// 著色器中的實例屬性
layout(location = 5) in mat4 instanceMatrix;

void main() {
    gl_Position = projection * view * model * instanceMatrix * vec4(aPosition, 1.0);
}
```

### 層級化細節（LOD）

根據物件距離使用不同精確度的模型：

```cpp
class LODSystem {
public:
    struct LODLevel {
        Mesh* mesh;
        float distance;
    };

    std::vector<LODLevel> lods;

    Mesh* getMeshForDistance(float dist) {
        for (int i = 0; i < lods.size(); i++) {
            if (dist < lods[i].distance)
                return lods[i].mesh;
        }
        return lods.back().mesh;
    }
};
```

### 視錐裁剪（Frustum Culling）

只繪製可見範圍內的物件：

```cpp
bool isInFrustum(GameObject* obj, Frustum* frustum) {
    BoundingSphere sphere = obj->getBoundingSphere();

    for (int i = 0; i < 6; i++) {
        Plane* plane = frustum->planes[i];
        float dist = dot(plane->normal, sphere.center) + plane->d;

        if (dist < -sphere.radius)
            return false;
    }
    return true;
}
```

## 陰影映射技術

### 基本陰影映射

```cpp
class ShadowMap {
    FrameBuffer shadowFBO;
    Matrix4 lightSpaceMatrix;

public:
    void renderShadowPass(Scene* scene) {
        shadowFBO.bind();
        glClear(GL_DEPTH_BUFFER_BIT);

        glCullFace(GL_FRONT);

        Shader* shadowShader = getShadowShader();
        shadowShader->use();
        shadowShader->setMat4("uLightSpaceMatrix", lightSpaceMatrix);

        for (auto object : scene->getShadowCastingObjects()) {
            shadowShader->setMat4("uModel", object->getTransform()->getMatrix());
            object->getMesh()->draw();
        }

        glCullFace(GL_BACK);
        shadowFBO.unbind();
    }
};
```

### 級聯陰影映射（CSM）

為不同距離範圍使用不同解析度的陰影貼圖：

```cpp
class CascadedShadowMaps {
    std::vector<FrameBuffer> shadowMaps;
    std::vector<Matrix4> lightSpaceMatrices;
    std::vector<float> splitDepths;

public:
    void render(Scene* scene, Camera* camera) {
        std::vector<float> frustumSplits = calculateSplitDepths(5, 50, 100);

        for (int i = 0; i < shadowMaps.size(); i++) {
            shadowMaps[i].bind();

            Matrix4 lightProj = Matrix4::ortho(-50, 50, -50, 50, frustumSplits[i], frustumSplits[i+1]);
            Matrix4 lightView = calculateLightViewMatrix();
            lightSpaceMatrices[i] = lightProj * lightView;

            renderShadowCasters(scene, lightSpaceMatrices[i]);

            shadowMaps[i].unbind();
        }
    }
};
```

### 百分比鄰近過濾（PCF）

減少陰影邊緣的鋸齒：

```glsl
float PCF(vec3 projCoords) {
    float currentDepth = projCoords.z;
    float shadow = 0.0;

    float bias = 0.005;
    vec2 texelSize = 1.0 / textureSize(uShadowMap, 0);

    for (int x = -2; x <= 2; x++) {
        for (int y = -2; y <= 2; y++) {
            float pcfDepth = texture(uShadowMap, projCoords.xy + vec2(x, y) * texelSize).r;
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;
        }
    }

    return shadow / 25.0;
}
```

## 延遲渲染

### 幾何通道（G-Buffer）

先渲染所有幾何資料到紋理：

```cpp
void geometryPass() {
    gBuffer.bind();
    gBuffer.clear();

    for (auto object : objects) {
        Shader* geomShader = object->getGeometryShader();
        geomShader->use();
        geomShader->setMat4("uModel", object->getModelMatrix());

        // 渲染到 G-Buffer
        renderPosition(object->getPosition());
        renderNormal(object->getNormal());
        renderAlbedo(object->getAlbedo());
        renderPBR(object->getMetallicRoughness());
    }

    gBuffer.unbind();
}
```

### 光照通道

```cpp
void lightingPass(Camera* camera) {
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    Shader* lightingShader = getDeferredLightingShader();
    lightingShader->use();

    gBuffer.bindTextures();

    for (auto light : lights) {
        if (light->type == LIGHT_DIRECTIONAL) {
            renderDirectionalLight(light, camera);
        } else if (light->type == LIGHT_POINT) {
            renderPointLight(light, camera);
        }
    }
}
```

```glsl
// 延遲光照片段著色器
void main() {
    vec3 wPos = texture(uGPosition, vTexCoord).rgb;
    vec3 wNormal = texture(uGNormal, vTexCoord).rgb;
    vec3 albedo = texture(uGAlbedo, vTexCoord).rgb;
    vec2 pbr = texture(uGPBR, vTexCoord).rg;

    vec3 viewDir = normalize(uCameraPos - wPos);

    vec3 color = calculatePBR(wPos, wNormal, albedo, pbr.x, pbr.y, viewDir);

    FragColor = vec4(color, 1.0);
}
```

## 延遲 vs 前向渲染

| 特性 | 前向渲染 | 延遲渲染 |
|------|---------|---------|
| 幾何處理 | 每個光源處理一次 | 只處理一次 |
| 光源數量 | 少量光源效能好 | 大量光源效率高 |
| 透明物體 | 自然處理 | 需要額外處理 |
| 硬體需求 | 較低 | 需要 MRT 支援 |
| 記憶體 | 較少 | 需要 G-Buffer |

## 其它優化技術

### 節點剔除（Node Culling）

```cpp
void cullNodes(SceneNode* node, Frustum* frustum) {
    if (!isInFrustum(node, frustum)) {
        node->setVisible(false);
        return;
    }

    node->setVisible(true);

    for (auto child : node->getChildren()) {
        cullNodes(child, frustum);
    }
}
```

### 紋理圖集（Texture Atlas）

將多個小紋理合併成一個大紋理，減少紋理切換：

```cpp
class TextureAtlas {
    Texture2D atlas;
    std::map<std::string, Rect2D> regions;

public:
    void addTexture(const std::string& name, Texture2D* tex) {
        Rect2D region = findEmptyRegion(tex->getWidth(), tex->getHeight());
        copyTexture(tex, atlas, region);
        regions[name] = region;
    }
};
```

### 計算著色器

使用 GPU 進行通用計算：

```glsl
#version 430

layout(local_size_x = 16, local_size_y = 16) in;

layout(binding = 0) readonly buffer Positions {
    vec4 positions[];
};

layout(binding = 1) writeonly buffer Outputs {
    vec4 results[];
};

void main() {
    uint idx = gl_GlobalInvocationID.x;

    vec4 pos = positions[idx];
    results[idx] = vec4(pos.xyz * 2.0, 1.0);
}
```

## 參考資料

- [渲染效能優化](https://www.google.com/search?q=rendering+performance+optimization)
- [陰影映射技術](https://www.google.com/search?q=shadow+mapping+techniques)
- [延遲渲染詳解](https://www.google.com/search?q=deferred+rendering+explained)