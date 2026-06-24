# Lua 與嵌入式腳本

## Lua 的設計哲學

Lua 是一種輕量級、可嵌入的腳本語言，由巴西 Roberto Ierusalimschy 等人於 1993 年開發。Lua 設計簡潔、易於嵌入 C 程式。

## Lua 的特點

- **輕量級**：核心庫很小
- **快速**：高效能的直譯器
- **可嵌入**：易於與 C/C++ 整合
- **簡潔**：簡單的語法

## 基本語法

```lua
-- 變數和類型
local name = "World"
local age = 30
local is_active = true

-- 函式
function greet(name)
    return "Hello, " .. name .. "!"
end

-- 表（Lua 的主要資料結構）
local point = { x = 10, y = 20 }
local array = { 1, 2, 3, 4, 5 }

-- 迭代器
for i, v in ipairs(array) do
    print(i, v)
end
```

## 嵌入式範例

```c
// C 中嵌入 Lua
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

int main() {
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);

    // 執行 Lua 代碼
    luaL_dostring(L, "print('Hello from Lua!')");

    // 呼叫 Lua 函式
    lua_getglobal(L, "math");
    lua_pushnumber(L, 10);
    lua_getfield(L, -1, "sqrt");
    lua_pushnumber(L, 10);
    lua_call(L, 1, 1);
    printf("sqrt(10) = %f\n", lua_tonumber(L, -1));

    lua_close(L);
    return 0;
}
```

## Lua 5.3 的新特性

### 整數類型

```lua
local i = 42  -- 現在是 integer 而非 float
```

### 位元運算

```lua
local x = 0xABCD
local shifted = x >> 4
local masked = x & 0xFF
```

### UTF-8 支援

```lua
local str = "你好，世界"
print(#str)  -- 15 bytes
```

## 遊戲開發中的 Lua

Lua 廣泛用於遊戲開發：

### Unity 中的 Lua（tolua）

```lua
-- Unity 腳本
local GameObject = UnityEngine.GameObject
local transform = GameObject.Find("Player").transform

function Update()
    transform:Translate(0, 0, Time.deltaTime * 10)
end
```

### Redis 中的 Lua

```lua
-- Redis Lua 腳本
local key = KEYS[1]
local value = redis.call('GET', key)
return value
```

## 使用場景

- **遊戲腳本**：魔獸世界、Roblox
- **配置腳本**：nginx、Redis
- **嵌入式應用**： IoT 設備
- **快速原型**：快速開發和測試

延伸閱讀：
- [Google 搜尋：Lua programming language](https://www.google.com/search?q=Lua+programming+language)
- [Google 搜尋：embedding Lua in C](https://www.google.com/search?q=embedding+Lua+in+C)