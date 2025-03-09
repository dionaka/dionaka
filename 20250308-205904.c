#include<stdio.h>
#include<stdlib.h>
#define MAXSIZE 1000
//顺序栈
typedef struct{
    char *top;
    char *base;
    int stacksize;
}SqStack;

int InitStack(SqStack *k){
    k->base = (char*)malloc(MAXSIZE*sizeof(char));
    if(!(k->base)) return 0;
    k ->top = k->base;
    k ->stacksize = MAXSIZE;
    return 1;
}

int LenStack(SqStack k){
    return (int)(k.top - k.base);
}

//压栈
int PushStack(SqStack *k,char m){
    if(k->top - k->base >= k->stacksize) return 0;
    *(k->top) = m;
    k->top++;
    return 1;
}

int PopStack(SqStack *k,char *m){
    if(k->top == k->base) return 0;
    k->top--;
    *m = *(k->top);
    return 1;
}

int main()
{
    SqStack stack;
    InitStack(&stack);
    return 0;
}