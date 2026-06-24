# Node.js 8 LTS：HTTP/2 與 N-API

## 前言

Node.js 8 於 2017 年 5 月發布，同年 10 月進入 LTS（長期支援）狀態。這個版本帶來了重要的新特性，包括原生 Promise 效能提升和 N-API。

## HTTP/2 支援

```javascript
const http2 = require('http2');
const fs = require('fs');

const server = http2.createSecureServer({
  key: fs.readFileSync('server-key.pem'),
  cert: fs.readFileSync('server-cert.pem')
});

server.on('stream', (stream, headers) => {
  stream.respond({
    'content-type': 'text/html',
    ':status': 200
  });
  stream.end('<h1>Hello World</h1>');
});

server.listen(8443);
```

## N-API

N-API 提供稳定的 C/C++ API，用於開發原生模組：

```c
// N-API 範例
#include <node_api.h>

napi_value Method(napi_env env, napi_callback_info info) {
  napi_status status;
  napi_value world;
  status = napi_create_string_utf8(env, "world", NAPI_AUTO_LENGTH, &world);
  return world;
}

napi_value Init(napi_env env, napi_value exports) {
  napi_status status;
  napi_value fn;
  status = napi_create_function(env, NULL, 0, Method, NULL, &fn);
  status = napi_set_named_property(env, exports, "hello", fn);
  return exports;
}

NAPI_MODULE(NODE_GYP_MODULE_NAME, Init)
```

## 對 AI 的應用

Node.js 8 的 N-API 使得開發高效能的 AI 推理引擎成為可能：

```javascript
// 使用 N-API 封装 TensorFlow C++ API
const tf = require('./tf-node addon');
const result = tf.runInference(model, input);
```

---

**延伸閱讀**

- [Node.js 8 LTS](https://www.google.com/search?q=Node.js+8+LTS)
- [N-API Documentation](https://www.google.com/search?q=node+n-api)