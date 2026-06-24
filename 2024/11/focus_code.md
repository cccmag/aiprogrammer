# devops_demo.js：DevOps 自動化流程模擬

## 概述

`devops_demo.js` 是一個模擬 DevOps 自動化流程的 Node.js 腳本。它展示了三個核心場景：

1. **Docker 構建流程模擬**——模擬映像構建、標籤和推送
2. **CI 管線階段模擬**——模擬程式碼檢查、測試、構建和部署
3. **部署策略演示**——模擬藍綠部署和滾動更新

## 核心功能

### 1. Docker 構建流程

```javascript
async function simulateDockerBuild(imageName) {
  console.log(`🔨 構建映像: ${imageName}`);
  await delay(800);
  console.log(`✅ 構建完成: ${imageName}`);
  
  console.log(`🏷️  標記映像: ${imageName}:latest`);
  await delay(300);
  
  console.log(`📤 推送映像到倉庫...`);
  await delay(500);
  console.log(`✅ 推送完成`);
  
  return { image: imageName, tag: 'latest', size: '245MB' };
}
```

模擬了 Docker 構建的三個階段：`docker build`、`docker tag` 和 `docker push`。

### 2. CI 管線階段

```javascript
async function runPipeline() {
  const stages = [
    { name: 'Lint', action: () => lint() },
    { name: 'Unit Tests', action: () => unitTest() },
    { name: 'Build', action: () => build() },
    { name: 'Integration Tests', action: () => integrationTest() },
    { name: 'Deploy', action: () => deploy() }
  ];
  
  for (const stage of stages) {
    const result = await stage.action();
    if (!result.success) throw new Error(`${stage.name} 失敗`);
  }
}
```

每個階段都是獨立步驟，失敗時中斷管線。

### 3. 部署策略

**藍綠部署**：維護兩個相同的生產環境，切換流量：

```javascript
async function blueGreenDeploy(version) {
  console.log(`🟦 部署藍色環境 v${version}...`);
  await delay(800);
  console.log(`🔄 切換流量到藍色環境...`);
  await delay(500);
  console.log(`🟩 關閉綠色環境 v${version - 1}...`);
}
```

**滾動更新**：逐步替換容器實例：

```javascript
async function rollingUpdate(version, instances) {
  for (let i = 1; i <= instances; i++) {
    console.log(`📦 更新實例 ${i}/${instances} 到 v${version}`);
    await delay(400);
  }
}
```

## 執行結果

```
=== DevOps 自動化流程模擬 ===

📦 Docker 構建流程
🔨 構建映像: myapp
✅ 構建完成: myapp
🏷️  標記映像: myapp:latest
📤 推送映像到倉庫...
✅ 推送完成

🔧 CI 管線
🔍 Lint... ✅ 通過
🧪 Unit Tests... ✅ 通過 (42/42)
📦 Build... ✅ 完成
🔗 Integration Tests... ✅ 通過
🚀 Deploy... ✅ 完成 (v2.3.1)

📊 部署策略 - 藍綠部署
🟦 部署藍色環境 v2...
🔄 切換流量到藍色環境...
🟩 關閉綠色環境 v1...

📊 部署策略 - 滾動更新
📦 更新實例 1/4 到 v2
📦 更新實例 2/4 到 v2
📦 更新實例 3/4 到 v2
📦 更新實例 4/4 到 v2
✅ 滾動更新完成
```

## 執行方式

```bash
node _code/devops_demo.js
```

或使用測試腳本：

```bash
_code/test.sh
```

## 程式碼要點

1. **非同步流程控制**：使用 `async/await` 和 `setTimeout` 模擬耗時操作
2. **階段化執行**：管線任務依序執行，支援失敗中斷
3. **策略模式**：不同的部署策略使用不同的實作方式
4. **狀態追蹤**：記錄每個階段的執行時間和結果

## 延伸練習

- 加入更多的部署策略（金絲雀部署、A/B 測試）
- 實作管線並行執行（整合測試和靜態分析同時運行）
- 加入失敗重試機制和超時處理

---

## 延伸閱讀

- [Node.js Async/Await](https://www.google.com/search?q=Node.js+async+await+tutorial)
- [Docker CLI 參考](https://www.google.com/search?q=Docker+CLI+reference)
- [部署策略模式](https://www.google.com/search?q=deployment+strategies+blue+green+rolling)
