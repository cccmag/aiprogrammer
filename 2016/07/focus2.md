# OpenGL 與渲染管線

## OpenGL 簡介

OpenGL（Open Graphics Library）是一個跨平台的圖形 API，廣泛應用於遊戲、科學視覺化和 CAD 等領域。從 1992 年的 1.0 版本到今天的 4.5 版本，OpenGL 經歷了多次重大變革。

## 渲染管線架構

### 固定功能管線（OpenGL 1.x）

早期的 OpenGL 使用固定功能管線，開發者只能透過狀態設定來控制渲染行為。

```
客戶端 → 頂點变换 → 光照 → 剪裁 → 透視分割 → 視口變換 → 光柵化 → 片段
```

### 可程式化管線（OpenGL 2.0+）

OpenGL 2.0 引入了著色器（Shader），讓開發者可以自訂頂點和片段處理邏輯。

```
客戶端 → 頂點著色器 → 幾何著色器 → 剪裁 → 光柵化 → 片段著色器 → 測試與混合 → 幀緩沖
```

## 核心概念

### 頂點與圖元

- **頂點（Vertex）**：3D 空間中的點，包含位置、法向量、紋理座標等屬性
- **圖元（Primitive）**：點、線、三角形等基本幾何

```c
// 定義一個簡單的三角形
GLfloat vertices[] = {
    0.0f, 0.5f, 0.0f,  // 頂點 1
   -0.5f,-0.5f, 0.0f,  // 頂點 2
    0.5f,-0.5f, 0.0f   // 頂點 3
};

// 建立頂點緩沖區
GLuint vbo;
glGenBuffers(1, &vbo);
glBindBuffer(GL_ARRAY_BUFFER, vbo);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
```

### 著色器程式

```glsl
// 頂點著色器
#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}

// 片段著色器
#version 330 core
out vec4 FragColor;

void main() {
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
```

### 紋理與采樣

紋理是覆蓋在 3D 模型表面的 2D 圖像。

```c
GLuint texture;
glGenTextures(1, &texture);
glBindTexture(GL_TEXTURE_2D, texture);

// 設定紋理參數
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

// 載入紋理數據
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
glGenerateMipmap(GL_TEXTURE_2D);
```

### 緩衝區物件

| 類型 | 用途 |
|-----|------|
| VBO | 儲存頂點屬性 |
| EBO/IBO | 儲存索引資料 |
| FBO | 幀緩沖區用於離屏渲染 |
| RBO | 渲染緩沖區 |
| VAO | 封裝頂點狀態 |

### 狀態管理

OpenGL 是一個大型狀態機。常用的狀態設定：

```c
// 啟用深度測試
glEnable(GL_DEPTH_TEST);

// 設定混合模式
glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

// 設定背面剔除
glEnable(GL_CULL_FACE);
glCullFace(GL_BACK);
```

## 座標變換

### 模型變換（Model Transformation）

將模型從本地座標轉換到世界座標：

```c
glm::mat4 model = glm::mat4(1.0f);
model = glm::rotate(model, glm::radians(angle), glm::vec3(1.0, 0.0, 0.0));
model = glm::translate(model, glm::vec3(0.0, 0.0, 1.0));
```

### 視圖變換（View Transformation）

設定攝影機的位置和方向：

```c
glm::mat4 view = glm::lookAt(
    glm::vec3(0.0, 0.0, 3.0),    // 攝影機位置
    glm::vec3(0.0, 0.0, 0.0),    // 觀察目標
    glm::vec3(0.0, 1.0, 0.0)     // 上向量
);
```

### 投影變換（Projection Transformation）

透視投影用於 3D 渲染，正交投影用於 2D UI：

```c
// 透視投影
glm::mat4 projection = glm::perspective(
    glm::radians(45.0f),         // FOV
    800.0f / 600.0f,            // 寬高比
    0.1f,                        // 近平面
    100.0f                       // 遠平面
);

// 正交投影
glm::mat4 projection = glm::ortho(
    0.0f, 800.0f,
    0.0f, 600.0f,
    0.1f, 100.0f
);
```

## 擴展機制

OpenGL 透過擴展（Extension）提供額外功能：

```c
// 檢查擴展支援
if (glewIsExtensionSupported("GL_EXT_texture_filter_anisotropic")) {
    // 使用各向異性過濾
}

// 列舉所有支援的擴展
GLint numExtensions;
glGetIntegerv(GL_NUM_EXTENSIONS, &numExtensions);
for (int i = 0; i < numExtensions; i++) {
    const GLubyte *ext = glGetStringi(GL_EXTENSIONS, i);
    // 處理每個擴展
}
```

## 現代 OpenGL 開發建議

1. **使用 VAO**：封裝頂點狀態，減少狀態設定錯誤
2. **使用 UBOs**：高效地傳遞著色器常數
3. **批量渲染**：減少 draw call 次數
4. **使用現代工具庫**：GLM、GLFW、GLEW 等

## 參考資料

- [OpenGL 官方網站](https://www.google.com/search?q=OpenGL+official+website)
- [Learn OpenGL 教程](https://www.google.com/search?q=Learn+OpenGL+tutorial)
- [OpenGL 渲染管線](https://www.google.com/search?q=OpenGL+rendering+pipeline+explained)