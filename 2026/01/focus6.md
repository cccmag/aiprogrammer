# 6. Jupyter Lab 與遠端開發

## Jupyter Lab

Jupyter Lab 是 Jupyter Notebook 的下一代介面，提供整合式的開發環境，支援多種檔案格式的編輯器、終端機與資料檢視器。在 AI 開發中特別適合資料探索、模型原型設計與可視化分析。Jupyter Lab 的擴充功能生態系也相當豐富，可以加入程式碼格式化、變數檢視器等實用工具。

```bash
# 安裝 Jupyter Lab
pip install jupyterlab

# 啟動（本機使用）
jupyter lab

# 啟動（允許遠端連線）
jupyter lab --port=8888 --ip=0.0.0.0 --no-browser

# 設定密碼（首次執行）
jupyter lab password
```

## 遠端開發方案

### SSH 隧道
將遠端伺服器的 Jupyter Lab 透過 SSH 隧道安全地連接到本地瀏覽器，避免直接暴露服務在網路上：

```bash
# 建立 SSH 隧道
ssh -L 8888:localhost:8888 user@remote-server

# 在遠端啟動 Jupyter Lab
jupyter lab --port=8888 --no-browser

# 在本地瀏覽器打開 http://localhost:8888
```

### VS Code Remote SSH
VS Code 的 Remote SSH 擴充功能讓你在本地編輯器中操作遠端檔案，執行終端指令與除錯。GPU 資源在遠端，開發體驗在本地，兩全其美。安裝 `ms-vscode-remote.remote-ssh` 擴充功能即可使用。

### 持久化會話
使用 tmux 保持遠端會話持久化，避免 SSH 斷線導致訓練中斷：

```bash
tmux new -s training_session
# 在 tmux 中啟動訓練
python train.py
# Ctrl+b d 離開會話（訓練持續進行）
tmux attach -t training_session  # 重新連接
```

## 效能考量

- 遠端開發時注意網路延遲對互動式編程的影響
- GPU 伺服器建議使用 SSH 隧道而非直接暴露埠號
- 使用 GPU 版 Jupyter Docker 映像可快速建立開發環境

## 參考資源

- https://www.google.com/search?q=Jupyter+Lab+remote+SSH+tunnel+setup+guide+port+forwarding
- https://www.google.com/search?q=VS+Code+Remote+SSH+AI+deep+learning+development+environment
- https://www.google.com/search?q=tmux+persistent+session+GPU+training+server+management
