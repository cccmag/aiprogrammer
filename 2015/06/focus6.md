# 主題六：網路程式設計

## socket 概述

socket 是 Unix 網路程式設計的基礎。它提供了一個統一的介面來進行網路通訊。

## 基本概念

### socket 型別

- **SOCK_STREAM**：面向連接的可靠流式 socket（TCP）
- **SOCK_DGRAM**：無連接的資料報 socket（UDP）
- **SOCK_RAW**：原始 socket，用於自定義協定

### 位址結構

```c
#include <netinet/in.h>

// IPv4
struct sockaddr_in {
    sa_family_t    sin_family;   // AF_INET
    in_port_t      sin_port;     // 連接埠號
    struct in_addr  sin_addr;    // IP 位址
    char           sin_zero[8];
};

struct in_addr {
    uint32_t       s_addr;       // 32 位元 IP
};
```

### IP 位址轉換

```c
#include <arpa/inet.h>

// 字串轉二進位
struct in_addr addr;
inet_pton(AF_INET, "192.168.1.1", &addr);

// 二進位轉字串
char buf[INET_ADDRSTRLEN];
inet_ntop(AF_INET, &addr, buf, sizeof(buf));
```

## TCP 客戶端

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(void) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);

    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) < 0) {
        perror("connect");
        return 1;
    }

    const char *msg = "Hello, Server!";
    send(sock, msg, strlen(msg), 0);

    char buffer[1024];
    ssize_t n = recv(sock, buffer, sizeof(buffer) - 1, 0);
    buffer[n] = '\0';
    printf("收到：%s\n", buffer);

    close(sock);
    return 0;
}
```

## TCP 伺服器

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 8080

int main(void) {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        return 1;
    }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(server_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        return 1;
    }

    if (listen(server_fd, 5) < 0) {
        perror("listen");
        return 1;
    }

    printf("伺服器監聽連接埠 %d...\n", PORT);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);

        if (client_fd < 0) {
            perror("accept");
            continue;
        }

        char client_ip[INET_ADDRSTRLEN];
        printf("客戶端連線：%s\n",
            inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip)));

        char buffer[1024];
        ssize_t n = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        if (n > 0) {
            buffer[n] = '\0';
            printf("收到：%s\n", buffer);

            const char *response = "Hello, Client!";
            send(client_fd, response, strlen(response), 0);
        }

        close(client_fd);
    }

    close(server_fd);
    return 0;
}
```

## UDP 客戶端

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(void) {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);

    const char *msg = "Hello, UDP Server!";
    sendto(sock, msg, strlen(msg), 0, (struct sockaddr*)&server, sizeof(server));

    char buffer[1024];
    struct sockaddr_in from;
    socklen_t from_len = sizeof(from);
    ssize_t n = recvfrom(sock, buffer, sizeof(buffer) - 1, 0,
                         (struct sockaddr*)&from, &from_len);

    if (n > 0) {
        buffer[n] = '\0';
        printf("收到：%s\n", buffer);
    }

    close(sock);
    return 0;
}
```

## UDP 伺服器

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 8080

int main(void) {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        return 1;
    }

    printf("UDP 伺服器監聽連接埠 %d...\n", PORT);

    char buffer[1024];
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);

    ssize_t n = recvfrom(sock, buffer, sizeof(buffer) - 1, 0,
                         (struct sockaddr*)&client_addr, &client_len);

    if (n > 0) {
        buffer[n] = '\0';
        printf("收到：%s\n", buffer);

        const char *response = "Hello, UDP Client!";
        sendto(sock, response, strlen(response), 0,
               (struct sockaddr*)&client_addr, client_len);
    }

    close(sock);
    return 0;
}
```

## 位址轉換函式

### htons, htonl, ntohs, ntohl

```c
// 主機位元組序轉網路位元組序
uint16_t port = htons(8080);     // 16 位元（連接埠）
uint32_t addr = htonl(0x7F000001); // 32 位元（IP）

// 網路位元組序轉主機位元組序
uint16_t host_port = ntohs(port);
uint32_t host_addr = ntohl(addr);
```

## 結論

socket 程式設計是網路應用開發的基礎。掌握 TCP 和 UDP 的客戶端和伺服器端程式設計，可以開發各類網路應用。進一步可以學習 select/poll/epoll 等 I/O 多工機制，開發高效能的網路服務。