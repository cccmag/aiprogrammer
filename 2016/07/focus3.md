# WebGL 與瀏覽器 3D

## WebGL 簡介

WebGL（Web Graphics Library）是一個基於 OpenGL ES 的 JavaScript API，允許在瀏覽器中進行硬體加速的 3D 圖形渲染。WebGL 由 Khronos Group 維護，廣泛支援於所有現代瀏覽器。

## WebGL 程式設計模型

### 與 OpenGL 的關係

WebGL 基於 OpenGL ES 2.0，這意味著：
- 使用 GLSL ES 著色器
- 固定功能管線被移除
- 所有渲染都透過著色器完成

### 基本架構

```html
<canvas id="glCanvas" width="800" height="600"></canvas>

<script>
const canvas = document.getElementById('glCanvas');
const gl = canvas.getContext('webgl');

if (!gl) {
    console.error('WebGL not supported');
}

// 設定視口
gl.viewport(0, 0, canvas.width, canvas.height);

// 清除顏色緩沖區
gl.clearColor(0.0, 0.0, 0.0, 1.0);
gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
</script>
```

## 著色器程式

### 頂點著色器

```glsl
attribute vec3 aPosition;
attribute vec3 aColor;

uniform mat4 uModelViewProjection;

varying vec3 vColor;

void main() {
    gl_Position = uModelViewProjection * vec4(aPosition, 1.0);
    vColor = aColor;
}
```

### 片段著色器

```glsl
precision mediump float;

varying vec3 vColor;

void main() {
    gl_FragColor = vec4(vColor, 1.0);
}
```

### 編譯著色器

```javascript
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
```

## 頂點資料與緩衝區

```javascript
const positions = new Float32Array([
    0.0,  0.5, 0.0,
   -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0
]);

const positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

// 綁定到 attribute
const aPosition = gl.getAttribLocation(program, 'aPosition');
gl.enableVertexAttribArray(aPosition);
gl.vertexAttribPointer(aPosition, 3, gl.FLOAT, false, 0, 0);
```

## 矩陣與數學

WebGL 沒有內建矩陣功能，通常使用第三方庫：

### 使用 gl-matrix

```javascript
import { mat4, vec3 } from 'gl-matrix';

// 創建單位矩陣
const modelMatrix = mat4.create();

// 模型變換：旋轉和位移
mat4.rotateZ(modelMatrix, modelMatrix, Math.PI / 4);
mat4.translate(modelMatrix, modelMatrix, [1.0, 0.0, 0.0]);

// 視圖矩陣
const viewMatrix = mat4.create();
mat4.lookAt(viewMatrix, [0, 0, 5], [0, 0, 0], [0, 1, 0]);

// 投影矩陣
const projectionMatrix = mat4.create();
mat4.perspective(projectionMatrix, Math.PI / 2, 800 / 600, 0.1, 100);

// 組合 MVP 矩陣
const mvpMatrix = mat4.create();
mat4.multiply(mvpMatrix, projectionMatrix, viewMatrix);
mat4.multiply(mvpMatrix, mvpMatrix, modelMatrix);

// 傳遞到著色器
const uMvp = gl.getUniformLocation(program, 'uModelViewProjection');
gl.uniformMatrix4fv(uMvp, false, mvpMatrix);
```

## Three.js 框架

Three.js 是最受歡迎的 WebGL 框架，簡化了 3D 開發：

### 基本範例

```javascript
import * as THREE from 'three';

// 創建場景
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);

// 創建攝影機
const camera = new THREE.PerspectiveCamera(
    75, window.innerWidth / window.innerHeight, 0.1, 1000
);
camera.position.z = 5;

// 創建渲染器
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 創建幾何體
const geometry = new THREE.BoxGeometry(1, 1, 1);

// 創建材質
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });

// 創建網格物件
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// 動畫迴圈
function animate() {
    requestAnimationFrame(animate);

    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    renderer.render(scene, camera);
}
animate();
```

### 載入 3D 模型

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.gltf', (gltf) => {
    const model = gltf.scene;
    scene.add(model);

    // 動畫
    const mixer = new THREE.AnimationMixer(model);
    gltf.animations.forEach((clip) => {
        mixer.clipAction(clip).play();
    });
});
```

## Canvas 2D 與 WebGL 比較

| 特性 | Canvas 2D | WebGL |
|------|----------|-------|
| 維度 | 2D | 2D/3D |
| API 等級 | 高階 | 低階（類 OpenGL） |
| 效能 | 一般 | 極高（GPU 加速） |
| 程式複雜度 | 簡單 | 複雜 |
| 瀏覽器支援 | 全部 | 全部（需要 canvas） |
| 適用場景 | UI、2D 遊戲 | 3D 遊戲、視覺化 |

## 效能考量

1. **減少 draw call**：使用 instancing 或批次渲染
2. **紋理壓縮**：使用 DXT/ETC/PVRTC 格式
3. **物件池**：重用幾何體和材質
4. **LOD**：根據距離簡化模型
5. **延遲渲染**：複雜場景的優化策略

## 參考資料

- [WebGL 官方規格](https://www.google.com/search?q=WebGL+specification+Khronos)
- [MDN WebGL 教程](https://www.google.com/search?q=MDN+WebGL+tutorial)
- [Three.js 官方網站](https://www.google.com/search?q=Three.js+official+website)