#include <stdio.h>
#include <string.h>
#define MAXSIZE 256

int f(const char *a, const char *b){
    int count = 0;
    int set_a[MAXSIZE] = {0};
    int set_b[MAXSIZE] = {0};
    for (int i = 0; a[i]; i++) set_a[(unsigned char)a[i]] = 1;
    for (int i = 0; b[i]; i++) set_b[(unsigned char)b[i]] = 1;
    for (int i = 0; i < MAXSIZE; i++) 
        if (set_a[i] != set_b[i]) 
            count++;
    return count;
}
int main(){
    const char *a = "0d00abc";
    const char *b = "abcABC";
    int result = f(a, b);
    printf("不同字符数: %d\n", result);
    return 0;
}
