# 著色器程式設計

## GLSL 語言基礎

GLSL（OpenGL Shading Language）是 OpenGL 和 WebGL 使用的著色器語言。它是一種 C 風格的語言，為 GPU 設計。

### 基本語法

```glsl
#version 330 core

precision mediump float;

in vec3 aPosition;
in vec3 aNormal;
in vec2 aTexCoord;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform vec3 uLightDirection;

out vec3 vNormal;
out vec3 vPosition;
out vec2 vTexCoord;

void main() {
    vec4 worldPosition = uModel * vec4(aPosition, 1.0);
    vPosition = worldPosition.xyz;
    vNormal = mat3(transpose(inverse(uModel))) * aNormal;
    vTexCoord = aTexCoord;

    gl_Position = uProjection * uView * worldPosition;
}
```

### 資料型別

| 型別 | 說明 |
|-----|------|
| void | 無返回值 |
| bool | 布林值 |
| int, float | 整數、浮點數 |
| vec2, vec3, vec4 | 向量 |
| mat2, mat3, mat4 | 矩陣 |
| sampler2D | 2D 紋理 |
| samplerCube | 立方體紋理 |

### 限定符

```glsl
attribute vec3 aPosition;    // 頂點屬性（OpenGL 2.0）
in vec3 vNormal;              // 頂點著色器輸入（OpenGL 3.0+）

uniform mat4 uModel;          // 全域常數

out vec3 vColor;             // 輸出到片段著色器

in vec3 vPosition;           // 從頂點著色器輸入
layout(location = 0) in vec3 aPosition;  // 明確綁定位置
```

## 頂點著色器

頂點著色器處理每個頂點，執行座標變換和屬性傳遞。

### 基本職責

1. 接收頂點屬性（位置、法向量、紋理座標等）
2. 執行座標變換（模型 → 世界 → 視圖 → 投影）
3. 計算並輸出插值所需的数据
4. 設定 `gl_Position` 內建變數

### 範例：帶光照的頂點著色器

```glsl
#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec3 aNormal;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform mat3 uNormalMatrix;

out vec3 vNormal;
out vec3 vWorldPosition;

void main() {
    vec4 worldPosition = uModel * vec4(aPosition, 1.0);
    vWorldPosition = worldPosition.xyz;
    vNormal = uNormalMatrix * aNormal;

    gl_Position = uProjection * uView * worldPosition;
}
```

## 片段著色器

片段著色器（又稱像素著色器）處理每個片段，計算最終顏色。

### 基本職責

1. 接收從頂點著色器插值的資料
2. 執行紋理取樣
3. 計算光照效果
4. 輸出最終顏色到 `gl_FragColor`

### 範例：Phong 光照片段著色器

```glsl
#version 330 core

in vec3 vNormal;
in vec3 vWorldPosition;

uniform vec3 uLightPosition;
uniform vec3 uCameraPosition;
uniform vec3 uLightColor;
uniform vec3 uAmbientColor;
uniform sampler2D uDiffuseTexture;

out vec4 FragColor;

void main() {
    vec3 normal = normalize(vNormal);
    vec3 lightDir = normalize(uLightPosition - vWorldPosition);
    vec3 viewDir = normalize(uCameraPosition - vWorldPosition);
    vec3 reflectDir = reflect(-lightDir, normal);

    float diff = max(dot(normal, lightDir), 0.0);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

    vec3 ambient = uAmbientColor * 0.1;
    vec3 diffuse = diff * uLightColor;
    vec3 specular = spec * uLightColor * 0.5;

    FragColor = vec4(ambient + diffuse + specular, 1.0);
}
```

## 光照模型

### ambient（環境光）

```glsl
vec3 ambient = uAmbientMaterial * uAmbientLight;
```

### diffuse（漫射光）

```glsl
float diff = max(dot(normal, lightDir), 0.0);
vec3 diffuse = diff * uDiffuseMaterial * uLightColor;
```

### specular（鏡面反射）

```glsl
vec3 reflectDir = reflect(-lightDir, normal);
float spec = pow(max(dot(viewDir, reflectDir), shininess), 0.0);
vec3 specular = spec * uSpecularMaterial * uLightColor;
```

### 完整 Phong 模型

```glsl
vec3 phongLighting(vec3 normal, vec3 viewDir, vec3 lightDir) {
    vec3 ambient = uAmbientMaterial * uAmbientLight;

    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * uDiffuseMaterial * uLightColor;

    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), uShininess);
    vec3 specular = spec * uSpecularMaterial * uLightColor;

    return ambient + diffuse + specular;
}
```

## 紋理取樣

```glsl
uniform sampler2D uTexture;
uniform samplerCube uCubemap;

in vec2 vTexCoord;

void main() {
    vec4 texColor = texture(uTexture, vTexCoord);
    vec4 cubemapColor = texture(uCubemap, vReflectDir);

    FragColor = texColor;
}
```

## 高階技巧

### 陰影映射

```glsl
float shadowCalculation(vec4 fragPosLightSpace) {
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5;

    if (projCoords.z > 1.0)
        return 0.0;

    float closestDepth = texture(uShadowMap, projCoords.xy).r;
    float currentDepth = projCoords.z;
    float shadow = currentDepth - 0.001 > closestDepth ? 1.0 : 0.0;

    return shadow;
}
```

### 環境映射

```glsl
void main() {
    vec3 I = normalize(vViewPosition - vWorldPosition);
    vec3 R = reflect(I, normalize(vNormal));

    vec4 color = texture(uEnvMap, R);
    FragColor = vec4(color.rgb, 1.0);
}
```

### 幾何著色器

```glsl
layout(triangles) in;
layout(line_strip, max_vertices = 6) out;

void main() {
    for (int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position;
        EmitVertex();
    }
    EndPrimitive();

    for (int i = 0; i < 3; i++) {
        gl_Position = gl_in[i].gl_Position + vec4(0.0, 0.1, 0.0, 0.0);
        EmitVertex();
    }
    EndPrimitive();
}
```

## WebGL 2.0 新特性

- **串聯反饋（Transform Feedback）**：收集著色器輸出的資料
- **多渲染目標（MRT）**：一次渲染到多個紋理
- **3D 紋理和陣列紋理**
- **非功率-of-2 紋理的完整 mipmap 支援**

## 參考資料

- [GLSL 官方規格](https://www.google.com/search?q=GLSL+specification)
- [ShaderToy 線上著色器測試](https://www.google.com/search?q=ShaderToy+online+GLSL)
- [GLSL 教程](https://www.google.com/search?q=GLSL+tutorial+beginner)