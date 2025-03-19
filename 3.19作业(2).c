//已知长度为n的线性表A采用顺序存储结构，请写一时间复杂度为O(n),
//空间复杂度为O(1)的算法，该算法删除线性表中所有值为item的数据元素
#include <stdio.h>
int RemoveItem(int A[], int n, int item) {
    int j = 0;
    for (int i = 0; i < n; i++) {
        if (A[i] != item) {
            A[j] = A[i];
            j++;
        }
    }
    return j;
}
int main() {
    int A[] = {6, 13, 12, 14, 12, 17, 6, 6, 21, 5};
    int n = sizeof(A) / sizeof(A[0]);
    int item = 6;
    printf("原数组:");
    for (int i = 0; i < n; i++) {
        printf("%d ", A[i]);
    }
    printf("\n");
    int newLength = RemoveItem(A, n, item);
    printf("删除 %d 后的数组:", item);
    for (int i = 0; i < newLength; i++) {
        printf("%d ", A[i]);
    }
    printf("\n");
    return 0;
}
