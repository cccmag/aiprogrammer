# 實作 3D 渲染範例

## 前言

理論說得再多，不如親手實作一個 3D 渲染範例。本篇文章將帶領讀者用 WebGL 實作一個簡單的 3D 場景，涵蓋著色器編寫、頂點屬性、矩陣變換和紋理映射。

本範例實作一個簡單的「3D 場景檢視器」，包含：

- 立方體模型渲染
- 基礎光照效果
- 攝影機控制
- 紋理映射

---

## 原始碼

完整的 JavaScript 實作請參考：[_code/webgl-demo.js](_code/webgl-demo.js)

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>WebGL 3D Demo</title>
    <style>
        body { margin: 0; overflow: hidden; }
        canvas { width: 100vw; height: 100vh; display: block; }
    </style>
</head>
<body>
<canvas id="glCanvas"></canvas>
<script type="module" src="webgl-demo.js"></script>
</body>
</html>
```

```javascript
// webgl-demo.js - WebGL 3D 渲染範例

const canvas = document.getElementById('glCanvas');
const gl = canvas.getContext('webgl');

if (!gl) {
    throw new Error('WebGL not supported');
}

const vertexShaderSource = `
    attribute vec3 aPosition;
    attribute vec3 aNormal;
    attribute vec2 aTexCoord;

    uniform mat4 uModel;
    uniform mat4 uView;
    uniform mat4 uProjection;
    uniform mat3 uNormalMatrix;

    varying vec3 vNormal;
    varying vec3 vPosition;
    varying vec2 vTexCoord;

    void main() {
        vec4 worldPosition = uModel * vec4(aPosition, 1.0);
        vPosition = worldPosition.xyz;
        vNormal = uNormalMatrix * aNormal;
        vTexCoord = aTexCoord;

        gl_Position = uProjection * uView * worldPosition;
    }
`;

const fragmentShaderSource = `
    precision mediump float;

    varying vec3 vNormal;
    varying vec3 vPosition;
    varying vec2 vTexCoord;

    uniform vec3 uLightDirection;
    uniform vec3 uLightColor;
    uniform sampler2D uTexture;

    void main() {
        vec3 normal = normalize(vNormal);
        vec3 lightDir = normalize(uLightDirection);

        float diff = max(dot(normal, lightDir), 0.0);
        vec3 diffuse = diff * uLightColor;

        vec3 ambient = vec3(0.1);
        vec3 texColor = texture2D(uTexture, vTexCoord).rgb;

        gl_FragColor = vec4((ambient + diffuse) * texColor, 1.0);
    }
`;

function createShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error('Shader compile error:', gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

function createProgram(gl, vertexShader, fragmentShader) {
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error('Program link error:', gl.getProgramInfoLog(program));
        gl.deleteProgram(program);
        return null;
    }
    return program;
}

const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);
const program = createProgram(gl, vertexShader, fragmentShader);

const positions = new Float32Array([
    -1, -1, -1,   1, -1, -1,   1,  1, -1,  -1,  1, -1,
    -1, -1,  1,   1, -1,  1,   1,  1,  1,  -1,  1,  1,
]);

const normals = new Float32Array([
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     1, -1,  1,  1, -1,  1,  1,  1,  1,  1,  1,  1,
]);

const texCoords = new Float32Array([
    0, 0,  1, 0,  1, 1,  0, 1,
    0, 0,  1, 0,  1, 1,  0, 1,
]);

const indices = new Uint16Array([
    0, 1, 2,  0, 2, 3,
    4, 5, 6,  4, 6, 7,
    0, 4, 7,  0, 7, 3,
    1, 5, 6,  1, 6, 2,
    0, 1, 5,  0, 5, 4,
    2, 3, 7,  2, 7, 6,
]);

const positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

const normalBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
gl.bufferData(gl.ARRAY_BUFFER, normals, gl.STATIC_DRAW);

const texCoordBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
gl.bufferData(gl.ARRAY_BUFFER, texCoords, gl.STATIC_DRAW);

const indexBuffer = gl.createBuffer();
gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);

const aPosition = gl.getAttribLocation(program, 'aPosition');
const aNormal = gl.getAttribLocation(program, 'aNormal');
const aTexCoord = gl.getAttribLocation(program, 'aTexCoord');

function createTexture(gl, width, height, r, g, b) {
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);

    const data = new Uint8Array(width * height * 4);
    for (let i = 0; i < width * height; i++) {
        data[i * 4] = r;
        data[i * 4 + 1] = g;
        data[i * 4 + 2] = b;
        data[i * 4 + 3] = 255;
    }

    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, data);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);

    return texture;
}

const texture = createTexture(gl, 64, 64, 200, 100, 50);

const uModel = gl.getUniformLocation(program, 'uModel');
const uView = gl.getUniformLocation(program, 'uView');
const uProjection = gl.getUniformLocation(program, 'uProjection');
const uNormalMatrix = gl.getUniformLocation(program, 'uNormalMatrix');
const uLightDirection = gl.getUniformLocation(program, 'uLightDirection');
const uLightColor = gl.getUniformLocation(program, 'uLightColor');
const uTexture = gl.getUniformLocation(program, 'uTexture');

let rotation = 0;

function mat4Perspective(fov, aspect, near, far) {
    const f = 1.0 / Math.tan(fov / 2);
    return new Float32Array([
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (far + near) / (near - far), -1,
        0, 0, (2 * far * near) / (near - far), 0,
    ]);
}

function mat4LookAt(eye, center, up) {
    const z = normalize([eye[0] - center[0], eye[1] - center[1], eye[2] - center[2]]);
    const x = normalize(cross(up, z));
    const y = cross(z, x);

    return new Float32Array([
        x[0], y[0], z[0], 0,
        x[1], y[1], z[1], 0,
        x[2], y[2], z[2], 0,
        -dot(x, eye), -dot(y, eye), -dot(z, eye), 1,
    ]);
}

function mat4RotateY(m, angle) {
    const c = Math.cos(angle);
    const s = Math.sin(angle);
    const rot = new Float32Array([
        c, 0, -s, 0,
        0, 1, 0, 0,
        s, 0, c, 0,
        0, 0, 0, 1,
    ]);
    return mat4Multiply(m, rot);
}

function mat4Multiply(a, b) {
    const result = new Float32Array(16);
    for (let row = 0; row < 4; row++) {
        for (let col = 0; col < 4; col++) {
            let sum = 0;
            for (let k = 0; k < 4; k++) {
                sum += a[row * 4 + k] * b[k * 4 + col];
            }
            result[row * 4 + col] = sum;
        }
    }
    return result;
}

function mat3FromMat4(m) {
    return new Float32Array([
        m[0], m[1], m[2],
        m[4], m[5], m[6],
        m[8], m[9], m[10],
    ]);
}

function normalize(v) {
    const len = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    return [v[0] / len, v[1] / len, v[2] / len];
}

function cross(a, b) {
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ];
}

function dot(a, b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);
}

window.addEventListener('resize', resize);
resize();

function render() {
    gl.clearColor(0.1, 0.1, 0.1, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST);

    gl.useProgram(program);

    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.enableVertexAttribArray(aPosition);
    gl.vertexAttribPointer(aPosition, 3, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, normalBuffer);
    gl.enableVertexAttribArray(aNormal);
    gl.vertexAttribPointer(aNormal, 3, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, texCoordBuffer);
    gl.enableVertexAttribArray(aTexCoord);
    gl.vertexAttribPointer(aTexCoord, 2, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);

    const aspect = canvas.width / canvas.height;
    const projection = mat4Perspective(Math.PI / 4, aspect, 0.1, 100);
    const view = mat4LookAt([3, 3, 3], [0, 0, 0], [0, 1, 0]);

    let model = new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
    model = mat4RotateY(model, rotation);

    gl.uniformMatrix4fv(uModel, false, model);
    gl.uniformMatrix4fv(uView, false, view);
    gl.uniformMatrix4fv(uProjection, false, projection);
    gl.uniformMatrix3fv(uNormalMatrix, false, mat3FromMat4(model));

    gl.uniform3f(uLightDirection, 1.0, 1.0, 1.0);
    gl.uniform3f(uLightColor, 1.0, 1.0, 1.0);

    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.uniform1i(uTexture, 0);

    gl.drawElements(gl.TRIANGLES, 36, gl.UNSIGNED_SHORT, 0);

    rotation += 0.01;
    requestAnimationFrame(render);
}

render();
```

---

## 執行結果

```
$ python3 -m http.server 8000
```

在瀏覽器中開啟 `http://localhost:8000/_code/webgl-demo.html`，可以看到：

- 一個帶紋理的旋轉立方體
- 簡單的方向光照效果
- 深色背景

---

## 程式結構說明

### 著色器程式

- **頂點著色器**：接收頂點位置、法向量、紋理座標，執行 MVP 變換
- **片段著色器**：計算 Lambert 光照，採樣紋理顏色

### 緩衝區設置

1. **positionBuffer**：立方體 8 個頂點的位置
2. **normalBuffer**：每個頂點的法向量
3. **texCoordBuffer**：每個頂點的紋理座標
4. **indexBuffer**：36 個索引（12 個三角形）

### 矩陣函數

- `mat4Perspective`：透視投影矩陣
- `mat4LookAt`：視圖矩陣（攝影機）
- `mat4RotateY`：繞 Y 軸旋轉
- `mat4Multiply`：矩陣乘法
- `mat3FromMat4`：提取 3x3 旋轉部分用於法向量變換

### 紋理創建

使用 `createTexture` 函數創建一個簡單的純色紋理作為範例。實際應用中可以使用真實圖片。

---

## 延伸練習

有興趣的讀者可以嘗試以下改進：

1. **加入攝影機控制**：使用滑鼠拖曳旋轉視角
2. **加入多個物件**：使用 instancing 渲染多個立方體
3. **加入陰影**：實現基本的陰影映射
4. **加入紋理載入**：使用 Image 物件載入真實紋理
5. **加入OBJ 模型載入**：解析並渲染複雜模型

---

## 結語

這個範例雖然簡單，但它涵蓋了 WebGL 3D 渲染的核心概念：

- 著色器編程（GLSL）
- 頂點屬性與緩衝區
- 矩陣變換（模型、視圖、投影）
- 紋理映射
- 簡單的光照模型

掌握了這些基礎，你就可以進一步學習更複雜的渲染技術，如延遲渲染、PBR 光照、陰影映射等。

詳細的技術背景請參考：
- [電腦圖學導論](focus1.md) — 3D 繪圖基礎理論
- [OpenGL 與渲染管線](focus2.md) — 渲染管線詳解
- [WebGL 與瀏覽器 3D](focus3.md) — WebGL 程式設計
- [3D 數學基礎](focus4.md) — 向量與矩陣
- [著色器程式設計](focus5.md) — GLSL 教學