# 主題五：Unix 系統程式設計

## Unix 系統呼叫概述

Unix 系統程式設計使用系統呼叫來與核心互動。主要的頭檔案包括：
- `<unistd.h>`：POSIX 系統呼叫
- `<fcntl.h>`：檔案控制選項
- `<sys/types.h>`：資料類型
- `<sys/stat.h>`：檔案狀態
- `<dirent.h>`：目錄操作

## 檔案操作

### open 和 close

```c
#include <fcntl.h>
#include <unistd.h>

int fd = open("file.txt", O_RDONLY);
if (fd == -1) {
    perror("open");
    return;
}

close(fd);
```

### read 和 write

```c
#include <unistd.h>

char buffer[1024];
ssize_t n = read(STDIN_FILENO, buffer, sizeof(buffer));
if (n > 0) {
    write(STDOUT_FILENO, buffer, n);
}
```

### open 的旗標

```c
O_RDONLY    // 唯讀
O_WRONLY    // 唯寫
O_RDWR      // 讀寫
O_CREAT     // 不存在則創建
O_EXCL      // 配合 O_CREAT，若存在則失敗
O_TRUNC     // 截斷為零長度
O_APPEND    // 附加模式
```

### 完整範例：複製檔案

```c
#include <fcntl.h>
#include <unistd.h>

int copy_file(const char *src, const char *dst) {
    int src_fd = open(src, O_RDONLY);
    if (src_fd == -1) {
        perror("open src");
        return -1;
    }

    int dst_fd = open(dst, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dst_fd == -1) {
        perror("open dst");
        close(src_fd);
        return -1;
    }

    char buffer[8192];
    ssize_t n;
    while ((n = read(src_fd, buffer, sizeof(buffer))) > 0) {
        if (write(dst_fd, buffer, n) != n) {
            perror("write");
            close(src_fd);
            close(dst_fd);
            return -1;
        }
    }

    close(src_fd);
    close(dst_fd);
    return 0;
}
```

## 目錄操作

### opendir, readdir, closedir

```c
#include <dirent.h>
#include <stdio.h>

void list_directory(const char *path) {
    DIR *dir = opendir(path);
    if (dir == NULL) {
        perror("opendir");
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        printf("%s\n", entry->d_name);
    }

    closedir(dir);
}
```

### stat 取得檔案資訊

```c
#include <sys/stat.h>

struct stat st;
if (stat("file.txt", &st) == 0) {
    printf("大小：%ld 位元組\n", (long)st.st_size);
    printf("權限：%o\n", st.st_mode & 0777);
    printf("最後修改：%ld\n", (long)st.st_mtime);
}
```

## 程序管理

### fork

```c
#include <unistd.h>
#include <sys/types.h>

pid_t pid = fork();

if (pid == -1) {
    perror("fork");
    return;
} else if (pid == 0) {
    // 子程序
    printf("子程序：PID = %d\n", getpid());
} else {
    // 父程序
    printf("父程序：建立了子程序 PID = %d\n", pid);
}
```

### exec 系列

```c
#include <unistd.h>

// 執行新程式
execl("/bin/ls", "ls", "-l", (char*)NULL);

// 使用 fork + exec
pid_t pid = fork();
if (pid == 0) {
    execl("/bin/ls", "ls", "-l", (char*)NULL);
    _exit(1);  // exec 成功則不回來
}
```

### wait

```c
#include <sys/wait.h>

int status;
pid_t pid = fork();
if (pid == 0) {
    // 子程序執行
    sleep(1);
    _exit(42);
} else {
    wait(&status);
    if (WIFEXITED(status)) {
        printf("子程序正常退出，返回 %d\n", WEXITSTATUS(status));
    }
}
```

### 管道

```c
#include <unistd.h>

int pipefd[2];
pipe(pipefd);

pid_t pid = fork();
if (pid == 0) {
    close(pipefd[0]);           // 關閉讀端
    dup2(pipefd[1], STDOUT_FILENO);  // 標準輸出重定向
    close(pipefd[1]);
    execl("/bin/ls", "ls", (char*)NULL);
} else {
    close(pipefd[1]);           // 關閉寫端
    // 從 pipefd[0] 讀取輸出
    char buffer[1024];
    ssize_t n = read(pipefd[0], buffer, sizeof(buffer));
    wait(NULL);
}
```

## 程序間通訊（IPC）

### 信號

```c
#include <signal.h>
#include <unistd.h>

void handler(int sig) {
    printf("收到信號 %d\n", sig);
}

signal(SIGINT, handler);  // 處理 Ctrl+C

while (1) {
    pause();  // 等待信號
}
```

### 共享記憶體

```c
#include <sys/shm.h>
#include <sys/ipc.h>

int shmid = shmget(IPC_PRIVATE, 1024, IPC_CREAT | 0666);
int *shared = (int*)shmat(shmid, NULL, 0);

*shared = 42;

shmdt(shared);
shmctl(shmid, IPC_RMID, NULL);
```

## 檔案描述符和 I/O 多工

### select

```c
#include <sys/select.h>

fd_set readfds;
FD_ZERO(&readfds);
FD_SET(STDIN_FILENO, &readfds);

struct timeval tv = {.tv_sec = 5, .tv_usec = 0};
int ready = select(STDIN_FILENO + 1, &readfds, NULL, NULL, &tv);

if (ready > 0) {
    if (FD_ISSET(STDIN_FILENO, &readfds)) {
        // stdin 可讀
    }
}
```

## 結語

Unix 系統程式設計提供了豐富的 API 來處理檔案、程序和程序間通訊。掌握這些基礎知識，是學習作業系統、開發系統工具和網路服務的前提。