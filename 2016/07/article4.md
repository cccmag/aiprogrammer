# 幾何著色器應用

## 幾何著色器介紹

幾何著色器在頂點著色器之後、柵格化之前執行，可以處理整個圖元。

## 實例化公告板

```glsl
layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;

in vec3 vWorldPos[];
in vec3 vNormal[];
in vec2 vTexCoord[];

out vec3 gWorldPos;
out vec3 gNormal;
out vec2 gTexCoord;
out float gDepth;

uniform mat4 uViewProj;

void main() {
    vec3 center = (vWorldPos[0] + vWorldPos[1] + vWorldPos[2]) / 3.0;

    for (int i = 0; i < 3; i++) {
        gWorldPos = vWorldPos[i];
        gNormal = vNormal[i];
        gTexCoord = vTexCoord[i];
        gDepth = length(vWorldPos[i]);

        gl_Position = uViewProj * vec4(vWorldPos[i], 1.0);
        EmitVertex();
    }
    EndPrimitive();
}
```

## 葉子生成

```glsl
layout(points) in;
layout(triangle_strip, max_vertices = 12) out;

in vec3 vPosition[];
in vec3 vNormal[];

uniform float uLeafSize;

void main() {
    vec3 pos = vPosition[0];
    vec3 up = vec3(0.0, 1.0, 0.0);
    vec3 right = normalize(cross(up, vNormal[0]));
    vec3 forward = cross(right, up);

    vec3 corners[4] = vec3[](
        pos - right * uLeafSize - forward * uLeafSize * 0.5,
        pos + right * uLeafSize - forward * uLeafSize * 0.5,
        pos - right * uLeafSize + forward * uLeafSize * 0.5,
        pos + right * uLeafSize + forward * uLeafSize * 0.5
    );

    vec2 texCoords[4] = vec2[](
        vec2(0.0, 1.0), vec2(1.0, 1.0),
        vec2(0.0, 0.0), vec2(1.0, 0.0)
    );

    for (int i = 0; i < 4; i++) {
        gl_Position = uViewProj * vec4(corners[i], 1.0);
        EmitVertex();
    }
    EndPrimitive();
}
```

## 細節層級生成

```glsl
layout(triangles) in;
layout(triangle_strip, max_vertices = 12) out;

in float vLOD[];

uniform float uTargetLOD;

void main() {
    if (vLOD[0] < uTargetLOD) {
        for (int i = 0; i < 3; i++) {
            gl_Position = gl_in[i].gl_Position;
            EmitVertex();
        }
        EndPrimitive();
    }
}
```

## 參考資料

- [幾何著色器教學](https://www.google.com/search?q=geometry+shader+tutorial+GLSL)