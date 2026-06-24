# WebGL 2.0 新功能

## WebGL 2.0 概述

WebGL 2.0 是 2017 年初發布的重大更新，基於 OpenGL ES 3.0，帶來了多項重要新功能。

## 主要新功能

### 3D 紋理

```javascript
const texture = gl.createTexture();
gl.bindTexture(gl.TEXTURE_3D, texture);

gl.texImage3D(gl.TEXTURE_3D, 0, gl.RGBA, width, height, depth, 0, gl.RGBA, gl.UNSIGNED_BYTE, data);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
```

### 實例化渲染增強

```javascript
const instanceData = new Float32Array(64 * 16); // 64 個實例，每個 16 floats

gl.bindBuffer(gl.ARRAY_BUFFER, instanceVBO);
gl.bufferData(gl.ARRAY_BUFFER, instanceData, gl.DYNAMIC_DRAW);

const aInstanceMatrix = gl.getAttribLocation(program, 'uInstanceMatrix');
for (let i = 0; i < 4; i++) {
    const loc = aInstanceMatrix + i;
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 4, gl.FLOAT, false, 64, i * 16);
    gl.vertexAttribDivisor(loc, 1);
}

gl.drawArraysInstanced(gl.TRIANGLES, 0, 36, 64);
```

### 多渲染目標（MRT）

```javascript
const attachments = [
    { format: gl.RGBA, texture: colorTexture },
    { format: gl.RGBA16F, texture: normalTexture },
    { format: gl.RGBA16F, texture: positionTexture },
];

const fbo = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);

attachments.forEach((att, i) => {
    gl.framebufferTexture2D(
        gl.FRAMEBUFFER,
        gl.COLOR_ATTACHMENT0 + i,
        gl.TEXTURE_2D,
        att.texture,
        0
    );
});

gl.drawBuffers([gl.COLOR_ATTACHMENT0, gl.COLOR_ATTACHMENT1, gl.COLOR_ATTACHMENT2]);
```

### 深度範本紋理

```javascript
const depthTexture = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, depthTexture);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.DEPTH_COMPONENT24, width, height, 0, gl.DEPTH_COMPONENT, gl.UNSIGNED_INT, null);

const stencilTexture = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, stencilTexture);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.STENCIL_INDEX8, width, height, 0, gl.STENCIL_INDEX, gl.UNSIGNED_BYTE, null);
```

### 變換回饋

```glsl
#version 300 es
in vec3 aPosition;
in vec3 aVelocity;

out vec3 vPosition;
out vec3 vVelocity;

uniform float uDeltaTime;

void main() {
    vPosition = aPosition + aVelocity * uDeltaTime;
    vVelocity = aVelocity + vec3(0.0, -9.8, 0.0) * uDeltaTime;
}
```

```javascript
gl.transformFeedbackVaryings(program, ['vPosition', 'vVelocity'], gl.INTERLEAVED_ATTRIBS);
gl.linkProgram(program);

const tf = gl.createTransformFeedback();
gl.bindTransformFeedback(gl.TRANSFORM_FEEDBACK, tf);
gl.bindBufferBase(gl.TRANSFORM_FEEDBACK_BUFFER, 0, positionBuffer);
gl.bindBufferBase(gl.TRANSFORM_FEEDBACK_BUFFER, 1, velocityBuffer);
```

## 其它改進

- **非功率-of-2 紋理的完整 mipmap 支援**
- **景深紋理格式支援**
- **更廣泛的著色器精度支援**
- **改進的緩衝區讀寫效能**

## 瀏覽器支援

| 瀏覽器 | 支援版本 |
|-------|---------|
| Chrome | 56+ |
| Firefox | 51+ |
| Safari | 15+ |
| Edge | 79+ |

## 參考資料

- [WebGL 2.0 規格](https://www.google.com/search?q=WebGL+2.0+specification)
- [WebGL 2.0 新功能](https://www.google.com/search?q=WebGL+2.0+new+features+tutorial)