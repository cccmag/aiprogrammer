# OpenGL ES 2.0：遊戲效能提升

## OpenGL ES 2.0 簡介

### 版本差異

```
OpenGL ES 版本比較：
───────────────────────────
OpenGL ES 1.1：
  - 固定管線
  - 廣泛支援（所有 Android 2.0+）
  - 適合 2D 遊戲

OpenGL ES 2.0：
  - 可程式管線
  - 需要 GPU 支援
  - 適合 3D 遊戲
```

### 2010 年支援情況

```
支援 OpenGL ES 2.0 的裝置（2010 年）：
───────────────────────────
Nexus One：      支援
Droid：          支援
Galaxy S：       支援
iPhone 3GS：     支援
```

## 可程式管線

### 與 1.1 的差異

```
管線比較：
───────────────────────────
固定管線（1.1）：
  輸入 → 變換 → 光照 → 材質 → 輸出

可程式管線（2.0）：
  輸入 → Vertex Shader → 柵格化 → Fragment Shader → 輸出
```

### Vertex Shader

```c
// 頂點著色器範例
attribute vec4 aPosition;
attribute vec4 aColor;
uniform mat4 uMVPMatrix;
varying vec4 vColor;

void main() {
    gl_Position = uMVPMatrix * aPosition;
    vColor = aColor;
}
```

### Fragment Shader

```c
// 片段著色器範例
precision mediump float;
varying vec4 vColor;

void main() {
    gl_FragColor = vColor;
}
```

## Android OpenGL 設定

### 基本設定

```java
// 宣告使用 OpenGL ES 2.0
<manifest>
    <uses-feature android:glEsVersion="0x00020000"
                  android:required="true"/>
</manifest>
```

### EGL 初始化

```java
public class MyGLRenderer implements GLSurfaceView.Renderer {
    private int EGLContextVersion = 2;

    public void onSurfaceCreated(GL10 gl, EGLConfig config) {
        // 檢查是否為 OpenGL ES 2.0
        String version = gl.glGetString(GL10.GL_VERSION);
        Log.d("OpenGL", "Version: " + version);

        // 設定 viewport
        GLES20.glViewport(0, 0, width, height);
    }
}
```

## 著色器程式

### 編譯著色器

```java
public static int loadShader(int type, String shaderCode) {
    int shader = GLES20.glCreateShader(type);
    GLES20.glShaderSource(shader, shaderCode);
    GLES20.glCompileShader(shader);
    return shader;
}

public static int createProgram(int vertexShader, int fragmentShader) {
    int program = GLES20.glCreateProgram();
    GLES20.glAttachShader(program, vertexShader);
    GLES20.glAttachShader(program, fragmentShader);
    GLES20.glLinkProgram(program);
    return program;
}
```

### 使用程式

```java
public void onDrawFrame(GL10 gl) {
    GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT);

    // 使用程式
    GLES20.glUseProgram(mProgram);

    // 綁定屬性
    GLES20.glBindAttribLocation(mProgram, 0, "aPosition");
    GLES20.glBindAttribLocation(mProgram, 1, "aColor");

    // 繪製
    GLES20.glDrawArrays(GLES20.GL_TRIANGLES, 0, 3);
}
```

## 效能優勢

### 與 1.1 的效能比較

```
效能比較：
───────────────────────────
3D 渲染：       2-5x 提升
紋理處理：      更靈活
光照計算：      可程式化
記憶體使用：    可能增加
```

### 適合場景

```
適合 OpenGL ES 2.0 的應用：
───────────────────────────
3D 遊戲：       需要陰影、反射
視覺效果：      後處理、粒子系統
地形渲染：      LOD、拼接
物理模擬：      即時計算
```

## 開發工具

### 框架支援

```
遊戲引擎支援（2010 年）：
───────────────────────────
Unity：         完全支援
SIO2：          支援 2.0
libgdx：        支援 2.0
AndEngine：     支援 2.0
Cocos2d-x：     即將支援
```

### 範例資源

```
學習資源：
───────────────────────────
Android SDK 範例：    OpenGLES20
GPU 監控：            使用 adb
文件：                khronos.org
```

---

## 結論

OpenGL ES 2.0 為 Android 遊戲開發打開了新的大門。可程式管線讓開發者能夠實現更複雜的視覺效果，雖然學習曲線較陡，但對於認真的遊戲開發者來說是值得投資的技能。

---

*本期文章到此結束。*