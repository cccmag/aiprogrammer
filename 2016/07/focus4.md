# 3D 數學基礎

## 向量運算

向量是 3D 圖形學的基礎，用於表示位置、方向和速度。

### 基本運算

```javascript
// 向量加法
vec3 add(vec3 a, vec3 b) {
    return { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z };
}

// 向量減法
vec3 subtract(vec3 a, vec3 b) {
    return { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z };
}

// 純量乘法
vec3 scale(vec3 v, float s) {
    return { x: v.x * s, y: v.y * s, z: v.z * s };
}

// 向量長度
float length(vec3 v) {
    return Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

// 單位向量
vec3 normalize(vec3 v) {
    const len = length(v);
    return { x: v.x / len, y: v.y / len, z: v.z / len };
}
```

### 點積（Dot Product）

點積用於計算夾角和投影：

```javascript
// 點積定義：a · b = |a| |b| cos(θ)
float dot(vec3 a, vec3 b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

// 計算夾角
float angleBetween(vec3 a, vec3 b) {
    return Math.acos(dot(a, b) / (length(a) * length(b)));
}

// 計算投影
vec3 project(vec3 v, vec3 onto) {
    const d = dot(v, onto) / dot(onto, onto);
    return scale(onto, d);
}
```

### 叉積（Cross Product）

叉積產生垂直於兩個輸入向量的向量：

```javascript
// 叉積定義：a × b = |a| |b| sin(θ) n
vec3 cross(vec3 a, vec3 b) {
    return {
        x: a.y * b.z - a.z * b.y,
        y: a.z * b.x - a.x * b.z,
        z: a.x * b.y - a.y * b.x
    };
}

// 計算垂直於三角形平面的法向量
vec3 triangleNormal(vec3 v0, vec3 v1, vec3 v2) {
    const edge1 = subtract(v1, v0);
    const edge2 = subtract(v2, v0);
    return normalize(cross(edge1, edge2));
}
```

## 矩陣運算

### 矩陣乘法

```javascript
// 4x4 矩陣乘法
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
```

### 單位矩陣

```
| 1  0  0  0 |
| 0  1  0  0 |
| 0  0  1  0 |
| 0  0  0  1 |
```

### 變換矩陣

**位移矩陣**：
```
| 1  0  0  tx |
| 0  1  0  ty |
| 0  0  1  tz |
| 0  0  0  1  |
```

**縮放矩陣**：
```
| sx 0  0  0 |
| 0  sy 0  0 |
| 0  0  sz 0 |
| 0  0  0  1 |
```

**繞 X 軸旋轉（角度 θ）**：
```
| 1  0      0       0 |
| 0  cosθ  -sinθ   0 |
| 0  sinθ   cosθ   0 |
| 0  0      0       1 |
```

**繞 Y 軸旋轉（角度 θ）**：
```
| cosθ  0  sinθ  0 |
| 0      1  0      0 |
| -sinθ  0  cosθ  0 |
| 0      0  0      1 |
```

**繞 Z 軸旋轉（角度 θ）**：
```
| cosθ  -sinθ  0  0 |
| sinθ   cosθ  0  0 |
| 0       0     1  0 |
| 0       0     0  1 |
```

## 座標系統與變換

### 左手座標系 vs 右手座標系

- **右手座標系**（DirectX、OpenGL 傳統）：X 右、Y 上、Z 前
- **左手座標系**（Unity、Blender）：X 右、Y 上、Z 後

### MVP 變換流程

```
模型座標 → 模型矩陣 → 世界座標 → 視圖矩陣 → 視圖座標 → 投影矩陣 → 剪裁座標 → 透視除法 → NDC → 視口變換 → 螢幕座標
```

```javascript
// 完整的 MVP 變換
const mvp = mat4Multiply(projectionMatrix, viewMatrix);
mvp = mat4Multiply(mvp, modelMatrix);

// 在著色器中
gl_Position = uMvp * vec4(aPosition, 1.0);
```

## 四元數

四元數用於表示 3D 旋轉，避免歐拉角的萬向節鎖問題。

### 四元數定義

q = w + xi + yj + zk = [w, (x, y, z)]

### 基本運算

```javascript
class Quaternion {
    constructor(w = 1, x = 0, y = 0, z = 0) {
        this.w = w;
        this.x = x;
        this.y = y;
        this.z = z;
    }

    // 四元數乘法
    multiply(q) {
        return new Quaternion(
            this.w * q.w - this.x * q.x - this.y * q.y - this.z * q.z,
            this.w * q.x + this.x * q.w + this.y * q.z - this.z * q.y,
            this.w * q.y - this.x * q.z + this.y * q.w + this.z * q.x,
            this.w * q.z + this.x * q.y - this.y * q.x + this.z * q.w
        );
    }

    // 單位四元數
    normalize() {
        const len = Math.sqrt(this.w * this.w + this.x * this.x +
                              this.y * this.y + this.z * this.z);
        return new Quaternion(
            this.w / len, this.x / len,
            this.y / len, this.z / len
        );
    }

    // 從軸角創建四元數
    static fromAxisAngle(axis, angle) {
        const halfAngle = angle / 2;
        const sin = Math.sin(halfAngle);
        return new Quaternion(
            Math.cos(halfAngle),
            axis.x * sin,
            axis.y * sin,
            axis.z * sin
        ).normalize();
    }

    // 轉換為旋轉矩陣
    toMatrix() {
        const x = this.x, y = this.y, z = this.z, w = this.w;
        return new Float32Array([
            1 - 2*y*y - 2*z*z, 2*x*y + 2*w*z,     2*x*z - 2*w*y,     0,
            2*x*y - 2*w*z,     1 - 2*x*x - 2*z*z, 2*y*z + 2*w*x,     0,
            2*x*z + 2*w*y,     2*y*z - 2*w*x,     1 - 2*x*x - 2*y*y, 0,
            0,                 0,                 0,                 1
        ]);
    }
}
```

### 球形線性插值（SLERP）

```javascript
function slerp(q1, q2, t) {
    let dot = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z;

    let q2s = q2;
    if (dot < 0) {
        dot = -dot;
        q2s = { w: -q2.w, x: -q2.x, y: -q2.y, z: -q2.z };
    }

    if (dot > 0.9995) {
        return normalize({
            w: q1.w + t * (q2s.w - q1.w),
            x: q1.x + t * (q2s.x - q1.x),
            y: q1.y + t * (q2s.y - q1.y),
            z: q1.z + t * (q2s.z - q1.z)
        });
    }

    const theta0 = Math.acos(dot);
    const theta = theta0 * t;
    const sinTheta = Math.sin(theta);
    const sinTheta0 = Math.sin(theta0);

    const s0 = Math.cos(theta) - dot * sinTheta / sinTheta0;
    const s1 = sinTheta / sinTheta0;

    return {
        w: s0 * q1.w + s1 * q2s.w,
        x: s0 * q1.x + s1 * q2s.x,
        y: s0 * q1.y + s1 * q2s.y,
        z: s0 * q1.z + s1 * q2s.z
    };
}
```

## 實用公式速查

| 公式 | 用途 |
|-----|------|
| dot(a, b) = |a||b|cosθ | 計算夾角 |
| |a × b| = |a||b|sinθ | 計算垂直面積 |
| RY(θ) · T(t) = 平移旋轉 | 組合變換順序 |
| quaternion.slerp(a, b, t) | 平滑旋轉插值 |

## 參考資料

- [3D 數學基礎教程](https://www.google.com/search?q=3D+math+tutorial+for+graphics)
- [四元數詳細解說](https://www.google.com/search?q=quaternion+rotation+tutorial)
- [矩陣變換詳解](https://www.google.com/search?q=matrix+transformation+3D+graphics)