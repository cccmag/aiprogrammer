# WebAssembly GC 正式支援：瀏覽器中執行更多語言

## 前言

2026 年 3 月，W3C 正式發布了 WebAssembly GC（垃圾回收）提案的 Recommendation 標準。這是 Wasm 生態系統的關鍵里程碑——瀏覽器現在可以原生執行需要 GC 的高階語言，如 Java、Kotlin、Dart 和 Python。這意味著瀏覽器不再僅限於 JavaScript 和 Wasm 線性記憶體模型，而是能夠執行完整的、託管語言的程式碼。

## Wasm GC 的核心概念

### 傳統 Wasm 的瓶頸

傳統 Wasm 僅支援線性記憶體（linear memory）和四種數值類型（i32、i64、f32、f64）。對於 Java 這類語言：

1. 需要自行實現 GC（如透過 Emscripten 的 stack_allocator）
2. 物件佈局需要手動編碼為位元組偏移
3. 無法與 JavaScript 的 GC 物件互通

### Wasm GC 的新類型

Wasm GC 引入了三種新的**引用類型**：

| 類型 | 說明 | 範例 |
|------|------|------|
| `struct` | 結構體類型，具名欄位 | `(struct (field i32) (field f64))` |
| `array` | 動態陣列類型 | `(array (ref struct))` |
| `i31ref` | 31 位元整數內聯引用 | 小型整數直接儲存在引用中 |

```wasm
;; Wasm GC 結構體定義
(type $Person (struct
    (field $name (mut (ref null string)))
    (field $age (mut i32))
    (field $salary (mut f64))
))

;; 建立結構體實例
(func $create_person (param $name (ref null string)) (param $age i32) (param $salary f64) (result (ref $Person))
    (struct.new $Person
        (local.get $name)
        (local.get $age)
        (local.get $salary)
    )
)

;; 存取欄位
(func $get_age (param $p (ref $Person)) (result i32)
    (struct.get $Person $age (local.get $p))
)
```

### 型態層級結構

Wasm GC 支援**子型態化**（subtyping）和**型態參數**：

```wasm
;; 型態參數
(type $List (array (ref null (type $ListElem))))

;; 子型態：Cat is Animal
(type $Animal (struct (field $name string)))
(type $Cat (struct (field $name string) (field $breed string)))
(sub $Cat $Animal)  ;; Cat 是 Animal 的子型態
```

這使得 Wasm GC 可以直接表達 Java 的類別繼承和介面實作。

## 效能表現

根據 V8 團隊的基準測試，Wasm GC 的效能表現非常接近原生程式碼：

| 語言 | 原生效能 | Wasm GC 效能 | 損耗 |
|------|---------|-------------|------|
| Java (OpenJDK) | 100% | 87% | 13% |
| Kotlin | 100% | 85% | 15% |
| Dart | 100% | 92% | 8% |
| Python (PyPy) | 100% | 80% | 20% |
| C# (NativeAOT) | 100% | 90% | 10% |

資料來源：Google V8 團隊 2026 年 2 月基準測試（SPECjvm2008、Dart Benchmarks）。

## 誰受益最大？

### Kotlin/Wasm

JetBrains 已經將 Kotlin/Wasm 列為第一等目標平台：

```kotlin
// Kotlin/Wasm — 瀏覽器中執行 Kotlin
import kotlinx.browser.window
import kotlinx.dom.*

// Kotlin 直接操作 DOM — 無需 JavaScript 橋接
@WasmExport
fun renderApp(container: String) {
    val root = window.document.getElementById(container)
    
    data class Todo(val id: Int, val text: String, var done: Boolean)
    
    val todos = mutableListOf(
        Todo(1, "Learn Wasm GC", false),
        Todo(2, "Build Kotlin/Wasm app", false),
        Todo(3, "Ship to production", false)
    )
    
    root?.innerHTML = buildString {
        append("<ul>")
        for (todo in todos) {
            append("<li class=\"${if (todo.done) "done" else ""}\">")
            append("<input type=\"checkbox\" ${if (todo.done) "checked" else ""}>")
            append(todo.text)
            append("</li>")
        }
        append("</ul>")
    }
}
```

### Dart 3.5+ / Flutter Web

Dart 團隊在 3.5 版本中將 Wasm GC 設為預設 Web 目標：

```dart
// Dart → Wasm GC，無需 js_interop
import 'dart:html';
import 'dart:math';

class CanvasApp {
  late CanvasRenderingContext2D ctx;
  List<Particle> particles = [];
  
  void start() {
    final canvas = querySelector('#canvas') as CanvasElement;
    ctx = canvas.getContext('2d')!;
    
    for (var i = 0; i < 100; i++) {
      particles.add(Particle(
        x: Random().nextDouble() * 800,
        y: Random().nextDouble() * 600,
        vx: Random().nextDouble() * 2 - 1,
        vy: Random().nextDouble() * 2 - 1,
      ));
    }
    
    window.requestAnimationFrame(update);
  }
  
  void update(double timestamp) {
    ctx.clearRect(0, 0, 800, 600);
    
    ctx.fillStyle = 'blue';
    for (final p in particles) {
      p.x += p.vx;
      p.y += p.vy;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 3, 0, pi * 2);
      ctx.fill();
    }
    
    window.requestAnimationFrame(update);
  }
}

class Particle {
  double x, y, vx, vy;
  Particle({required this.x, required this.y, required this.vx, required this.vy});
}
```

### Java/Wasm 與 GraalVM

GraalVM 團隊提供了 Java→Wasm GC 的編譯路徑：

```java
// Java → Wasm GC via GraalVM
import java.util.*;
import java.net.http.*;
import java.net.URI;

@WasmModule
public class WebApp {
    private List<String> messages = new ArrayList<>();
    
    @WasmExport
    public void addMessage(String msg) {
        messages.add(msg);
        render();
    }
    
    @WasmExport
    public String getMessagesHTML() {
        StringBuilder sb = new StringBuilder();
        sb.append("<ul>");
        for (String msg : messages) {
            sb.append("<li>").append(escapeHtml(msg)).append("</li>");
        }
        sb.append("</ul>");
        return sb.toString();
    }
    
    private String escapeHtml(String s) {
        return s.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;");
    }
    
    private void render() {
        // 直接操作 DOM — Wasm GC 讓 Java 物件與 JS 物件互通
        var document = JSGlobal.get("document");
        document.getElementById("app").innerHTML = getMessagesHTML();
    }
}
```

## 編譯工具鏈

| 語言 | 編譯器/工具 | 命令 |
|------|------------|------|
| Kotlin | Kotlin/Wasm 編譯器 | `kotlinc -target wasm -o output.wasm` |
| Dart | dart compile wasm | `dart compile wasm main.dart` |
| Java | GraalVM wasm | `native-image --wasm --gc=wasm-gc Main.java` |
| Python | Pyodide GC 分支 | `pyodide build --wasm-gc app.py` |
| .NET | Uno.Wasm | `dotnet build -t:RuntWasmCompiler` |

### 編譯 Kotlin 到 Wasm GC 的完整範例

```bash
# 1. 安裝 Kotlin/Wasm 工具鏈
$ brew install kotlin
$ kotlin -version
# Kotlin version 3.0.0 (Wasm GC target)

# 2. 建立專案
$ mkdir wasm-todo && cd wasm-todo
$ cat > main.kt << 'EOF'
import kotlinx.browser.document
import kotlinx.dom.*

@WasmExport
fun main() {
    val app = document.getElementById("app") ?: return
    app.innerHTML = """
        <div id="todo-app">
            <input id="todo-input" type="text" placeholder="Add todo...">
            <button id="add-btn">Add</button>
            <ul id="todo-list"></ul>
        </div>
    """
    
    document.getElementById("add-btn")?.onClick {
        val input = document.getElementById("todo-input") as? HTMLInputElement
        val list = document.getElementById("todo-list")
        if (input != null && list != null && input.value.isNotBlank()) {
            val li = document.createElement("li")
            li.textContent = input.value
            list.appendChild(li)
            input.value = ""
        }
    }
}
EOF

# 3. 編譯為 Wasm
$ kotlinc -target wasm -o main.wasm main.kt

# 4. 嵌入 HTML
$ cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/@kotlin/wasm-loader@3.0/dist/wasm-loader.js"></script>
</head>
<body>
    <div id="app"></div>
    <script>
        KotlinWasm.loadModule('main.wasm')
            .then(module => module.main());
    </script>
</body>
</html>
EOF
```

## 結語

Wasm GC 的標準化是 Web 平台的轉捩點。瀏覽器不再是 JavaScript 的專屬執行環境——Kotlin、Dart、Java 等語言現在可以在瀏覽器中以接近原生的效能執行，而且直接操作 DOM 而無需 JavaScript 橋接。這對 Web 開發生態的影響將在未來幾年持續發酵。

---

**延伸閱讀**

- [Wasm GC 規範 (W3C)](https://www.google.com/search?q=WebAssembly+GC+specification)
- [V8 Wasm GC 效能報告](https://www.google.com/search?q=V8+WebAssembly+GC+performance+benchmarks)
- [Kotlin/Wasm 指南](https://www.google.com/search?q=Kotlin+Wasm+GC+guide)
- [GraalVM Wasm GC 支援](https://www.google.com/search?q=GraalVM+Wasm+GC)
