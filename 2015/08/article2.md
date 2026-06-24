# 從入門到精通：Vim 使用指南

## 前言

Vim 是 Linux 系統中最強大的文字編輯器之一，幾乎每台 Linux 伺服器都有安裝。

---

## 基本模式

| 模式 | 說明 | 進入方式 |
|------|------|----------|
| Normal | 命令模式 | Esc |
| Insert | 插入模式 | i, a, o |
| Visual | 可視模式 | v, V, Ctrl+v |
| Command | 命令列模式 | : |

---

## 基本操作

### 移動

```vim
h j k l     左 下 上 右
w           下一個單字詞首
e           下一個單字詞尾
b           上一個單字詞首
0           行首
$           行尾
gg          檔案開頭
G           檔案結尾
:Ctrl+d     下半頁
:Ctrl+u     上半頁
```

### 編輯

```vim
i           在游標前插入
a           在游標後插入
o           在下方新增一行
O           在上方新增一行
x           刪除游標下的字元
dd          刪除一行
dw          刪除一個單字詞
yy          複製一行
p           貼上
u           復原
Ctrl+r      重做
```

---

## 搜尋與取代

```vim
/pattern        向下搜尋
?pattern        向上搜尋
n               下一個匹配
N               上一個匹配
:%s/old/new/g   全部取代
:%s/old/new/gc  確認後取代
```

---

## Vimrc 設定

```vim
" ~/.vimrc 範例

" 基本設定
set nocompatible
set backspace=2
set encoding=utf-8

" 顯示設定
set number          " 行號
set relativenumber  " 相對行號
set showcmd         " 顯示命令
set cursorline      " 游標行反白

" 縮排
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent

" 搜尋
set incsearch
set hlsearch
set ignorecase
set smartcase

" 支援滑鼠
set mouse=a

" 語法高亮
syntax on
```

---

## 進階技巧

### 多視窗

```vim
:sp file.txt     " 水平分割
:vsp file.txt    " 垂直分割
Ctrl+w w         " 切換視窗
Ctrl+w q         " 關閉視窗
:only            " 只保留當前視窗
```

### 分頁

```vim
:tabnew file.txt " 新增分頁
gt               " 下一分頁
gT               " 上一分頁
:tabclose        " 關閉分頁
```

### 巨集

```vim
qa               " 開始錄製巨集到暫存器 a
# 操作...
q                " 停止錄製
@a               " 執行巨集
@@               " 再次執行
```

### 文字物件

```vim
ci"              " 改變 "" 內的內容
ca"              " 改變 "" 內的內容（含引號）
yi(              " 複製 () 內的內容
va{              " 選取 {} 內的內容（含大括號）
```

---

## 外掛程式推薦

### Vundle（外掛管理器）

```vim
" ~/.vimrc 加入
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'ctrlpvim/ctrlp.vim'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'

call vundle#end()
```

### NERDTree（檔案瀏覽）

```vim
" 開啟 NERDTree
:NERDTreeToggle

" 快捷鍵
o       開啟檔案
go      預覽
t       新分頁開啟
i       垂直分割
```

### CtrlP（快速開檔）

```vim
:CtrlP             " 開啟
:CtrlPBuffer       " 只搜尋緩衝區
:CtrlPMRU          " 最近使用的檔案
```

[搜尋 Vim plugins 2015](https://www.google.com/search?q=best+Vim+plugins+2015)

---

## 小結

Vim 學習曲線陡峭，但一旦熟練，能大幅提升文字編輯效率。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Vim 官方網站](https://www.google.com/search?q=Vim+official+website)
- [Vim Adventures](https://www.google.com/search?q=Vim+adventures+game)