#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void demo(void) {
    printf("=== C 語言指標展示 ===\n\n");

    int x = 42;
    int *p = &x;

    printf("基本指標：\n");
    printf("  x 的值：%d\n", x);
    printf("  x 的位址：%p\n", (void*)&x);
    printf("  p 儲存的位址：%p\n", (void*)p);
    printf("  *p 的值：%d\n\n", *p);

    int arr[] = {10, 20, 30, 40, 50};
    int *ap = arr;

    printf("指標算術：\n");
    printf("  arr[0] = %d, *(ap+0) = %d\n", arr[0], *(ap + 0));
    printf("  arr[2] = %d, *(ap+2) = %d\n\n", arr[2], *(ap + 2));

    const char *str = "Hello, World!";
    printf("字串指標：\n");
    printf("  字串：%s\n", str);
    printf("  第一個字元：%c\n", str[0]);
    printf("  長度：%zu\n\n", strlen(str));

    int *dyn_arr = (int*)malloc(5 * sizeof(int));
    if (dyn_arr == NULL) {
        printf("記憶體配置失敗\n");
        return;
    }

    printf("動態配置：\n");
    for (int i = 0; i < 5; i++) {
        dyn_arr[i] = (i + 1) * 10;
    }
    printf("  配置的陣列：");
    for (int i = 0; i < 5; i++) {
        printf("%d ", dyn_arr[i]);
    }
    printf("\n");

    free(dyn_arr);
    printf("  記憶體已釋放\n\n");

    printf("=== C 語言指標展示完成 ===\n");
}

int main(void) {
    demo();
    return 0;
}