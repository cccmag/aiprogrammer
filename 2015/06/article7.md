# C 與 Python 的互補

## 兩種語言的特點

C 和 Python 代表了兩種不同的程式設計哲學：

- **C**：效能優先，手動控制，接近硬體
- **Python**：開發速度優先，自動管理，高抽象層次

## 互補關係

### C 的角色

1. **效能關鍵模組**：NumPy、SciPy 等底層使用 C
2. **系統介面**：作業系統和硬體的綁定層
3. **嵌入式**：微控制器上的 Python 直譯器

### Python 的角色

1. **快速開發**：原型和應用程式
2. **資料處理**：Pandas、NumPy
3. **網頁服務**：Flask、Django

## Python 呼叫 C

### ctypes

```c
// mylib.c
int add(int a, int b) {
    return a + b;
}
```

```python
import ctypes

lib = ctypes.CDLL('./libmylib.so')
result = lib.add(1, 2)
print(result)
```

### Python 擴展

```c
// mymodule.c
#include <Python.h>

static PyObject* add(PyObject *self, PyObject *args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
        return NULL;
    }
    return Py_BuildValue("i", a + b);
}

static PyMethodDef mymodule_methods[] = {
    {"add", add, METH_VARARGS, "Add two integers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef mymodule_def = {
    PyModuleDef_HEAD_INIT,
    "mymodule",
    NULL,
    -1,
    mymodule_methods
};

PyMODINIT_FUNC PyInit_mymodule(void) {
    return PyModule_Create(&mymodule_def);
}
```

### Cython

```cython
# mymodule.pyx
cdef int add(int a, int b):
    return a + b

def py_add(a, b):
    return add(a, b)
```

## 典型架構

```
+------------------+
|    Python 應用    |
+------------------+
|    Python 直譯器  |
+------------------+
|   C 擴展模組      |
+------------------+
|    C 函式庫       |
+------------------+
|   作業系統 API    |
+------------------+
```

## 常見組合

### 資料科學

- **NumPy**：C/Fortran 實現的核心計算
- **Pandas**：基於 NumPy 的資料分析
- **TensorFlow**：C++ 實現的深度學習

### 系統工具

- **Ansible**：Python 自動化工具
- **系統監控**：Python 指令碼呼叫 C 函式庫

### 遊戲開發

- **遊戲引擎**：C/C++ 實現
- **遊戲腳本**：Python 邏輯

## 效能優化策略

1. **瓶頸分析**：使用 profiler 找出熱點
2. **C 優化**：將瓶頸用 C 重寫
3. **結合使用**：Python 膠水程式碼 + C 效能模組

## 結論

C 和 Python 並非互相排斥，而是互補的。理解兩種語言的優勢，可以幫助你選擇最適合每個任務的工具，達到開發速度和執行效率的最佳平衡。