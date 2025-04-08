//设从键盘输入一整数的序列：a1, a2, a3，…，an，试编写算法实现：
//用栈结构存储输入的整数，当ai≠-1时，将ai进栈；当ai=-1时，输出栈顶整数并出栈。
//算法应对异常情况（入栈满等）给出相应的信息。
#include<stdio.h>
#define MaxSize 6
typedef struct stack{
    int *top;
    int *base;
    int stacksize;
}SqStack;

int InitStack(SqStack *k){
    k -> base = (int *)malloc(sizeof(int) * MaxSize);
    if(!k -> base) return 0;
    k -> top = k -> base;
    k -> stacksize = MaxSize;
    return 1;
}

int PushStack(SqStack *k,int m){
    if(k -> top - k -> base >= k -> stacksize) return 0;
    *(k -> top) = m;
    k -> top++;
    return 1;
}

int PopStack(SqStack *k,int *n){
    if(k -> top == k ->base) return 0;
    k -> top--;
    *n = *(k -> top);
    return 1;
}
int main()
{
    SqStack k;
    InitStack(&k);
    int num;
    while(1){
        scanf("%d",&num);
        if(num == -1) break;
        if(!PushStack(&k, num)){
        printf("栈已满，无法继续压入");
        break;
        }
    }
    printf("出栈:\n");
    while(PopStack(&k, &num)){
        printf("%d ", num);
    }
    return 0;
}