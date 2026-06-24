# 著色器編譯優化

## 著色器預處理

```glsl
#define SHADOW_QUALITY 3

#if SHADOW_QUALITY == 1
    #define SHADOW_SIZE 512
#elif SHADOW_QUALITY == 2
    #define SHADOW_SIZE 1024
#else
    #define SHADOW_SIZE 2048
#endif
```

## 避免動態分支

```glsl
// 避免動態分支
float computeLighting(vec3 normal, vec3 lightDir) {
    return max(dot(normal, lightDir), 0.0);
}

// 改用查找表或數學技巧
float fakeAO(float dist) {
    return 1.0 - smoothstep(0.0, 1.0, dist);
}
```

## 紋理取樣優化

```glsl
// 減少 mip 級別切換開銷
vec3 sampleTextureTrilinear(usampler2D tex, vec2 uv) {
    vec2 texSize = vec2(textureSize(tex, 0));
    vec2 duv = 0.5 / texSize;

    vec3 col0 = texture(tex, uv).rgb;
    vec3 col1 = texture(tex, uv + duv).rgb;

    return mix(col0, col1, 0.5);
}
```

## 常數移動

```glsl
// 將常數計算移到著色器外部
const float INV_PI = 0.31830988618;
const float TWO_PI = 6.28318530718;

float fresnel(float cosTheta) {
    return INV_PI + (1.0 - INV_PI) * pow(1.0 - cosTheta, 5.0);
}
```

## 著色器內聯

```glsl
// 使用內聯函數減少呼叫開銷
inline vec3 computeNormal(vec3 pos) {
    return normalize(cross(dFdx(pos), dFdy(pos)));
}
```

## 參考資料

- [GPU 著色器優化](https://www.google.com/search?q=shader+optimization+GPU)