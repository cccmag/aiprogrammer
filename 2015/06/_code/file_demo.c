#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

void demo(void) {
    printf("=== Unix 檔案操作展示 ===\n\n");

    const char *filename = "demo_output.txt";
    const char *content = "Hello from C!\nThis is a test file.\n";

    printf("使用標準 I/O：\n");
    FILE *f = fopen(filename, "w");
    if (f == NULL) {
        perror("fopen");
        return;
    }
    fprintf(f, "%s", content);
    fclose(f);
    printf("  已寫入檔案：%s\n", filename);

    f = fopen(filename, "r");
    if (f == NULL) {
        perror("fopen");
        return;
    }
    printf("  檔案內容：\n    ");
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), f) != NULL) {
        printf("%s", buffer);
    }
    fclose(f);

    printf("\n使用 Unix 系統呼叫：\n");
    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        perror("open");
        return;
    }

    struct stat st;
    if (fstat(fd, &st) == 0) {
        printf("  檔案大小：%ld 位元組\n", (long)st.st_size);
        printf("  檔案權限：%o\n", st.st_mode & 0777);
    }
    close(fd);

    unlink(filename);
    printf("\n  已刪除測試檔案\n");

    printf("\n=== Unix 檔案操作展示完成 ===\n");
}

int main(void) {
    demo();
    return 0;
}