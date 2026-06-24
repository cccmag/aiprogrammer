# Linux 效能監控：top 與 htop

## 前言

了解系統資源使用情況對 AI 開發者最佳化訓練流程很重要。

## top 命令

```bash
# 基本使用
top

# 指定更新頻率
top -d 1

# 顯示特定程序
top -p 1234
```

### top 常用快捷鍵

| 按鍵 | 功能 |
|-----|------|
| M | 按記憶體使用排序 |
| P | 按 CPU 使用排序 |
| T | 按運行時間排序 |
| q | 退出 |

## htop 命令

```bash
# 安裝
sudo apt install htop

# 啟動
htop
```

## GPU 監控

```bash
# NVIDIA GPU
nvidia-smi

# 持續監控
watch -n 1 nvidia-smi

# 詳細輸出
nvidia-smi -l 1
```

## 延伸閱讀

- [Linux 效能監控指南](https://www.google.com/search?q=linux+system+monitoring+top+htop)