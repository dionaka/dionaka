/*
将编号为0和1的两个栈存放于一个数组空间V[m]中，栈底分别处于数组的两端。当第0号栈的栈顶指针top[0]等于-1时该栈为空，当第1号栈的栈顶指针top[1]等于m时该栈为空。两个栈均从两端向中间增长。试编写双栈初始化，判断栈空、栈满、进栈和出栈等算法的函数。
双栈数据结构的定义如下：
Typedef struct{
int top[2],bot[2];//栈顶和栈底指针
SElemType *V;//栈数组 
int m;//栈最大可容纳元素个数
}DblStack
*/
//思路:栈满条件top[0] + 1 == top[1],相遇.top[0]初始化为-1表示栈为空 top[1]初始化为m表示栈为空.用数组V[m]存储两栈元素,栈0从左端(下标0)向右,栈1从右端(下标1)向左,题指针类型为int,即数组索引

#include<stdio.h>
#define SElemType char*

typedef struct{
    int top[2],bot[2];
    SElemType *V;
    int m;
}DblStack;

//初始化双栈
void InitDblStack(DblStack *k,int m){
    k->V = (SElemType*)malloc(m * sizeof(SElemType));
    k->m = m;//☆我把这步漏了,导致输出null...
    k->top[0] = -1;
    k->bot[0] = 0;
    k->top[1] = m;
    k->bot[1] = m-1;
}

//判断栈空
int IsEmpty(DblStack *k,int i){
    if(i==0) return k->top[0]==-1;
    else if(i==1) return k->top[1]==k->m;
    else return -1;
}

//判断栈满
int IsFull(DblStack *k){
    return k->top[0]+1==k->top[1];
}

//进栈
int Push(DblStack *k,int i,SElemType v){
    if(IsFull(k)){printf("栈满, %s 无法入栈\n",v);return 0;}
    if(i==0){
        k->V[++k->top[0]] = v;
        return 1;
    }
    else if(i==1){
        k->V[--k->top[1]] = v;
        return 1;
    }
    return 0;
}

//出栈
int Pop(DblStack *k,int i,SElemType *v){
    if(IsEmpty(k,i)) return 0;
    if(i==0){
        *v = k->V[k->top[0]--];
        return 1;
    }
    else if(i==1){
        *v = k->V[k->top[1]++];
        return 1;
    }
    return 0;
}

//附加
//清空栈
void ClearStack(DblStack *k,int i){
    if(i==0){
        while(k->top[0] != -1)
            free(k->V[k->top[0]--]);
    }
    else if(i==1){
        while(k->top[1] != k->m)
            free(k->V[k->top[0]++]);
    }
    else printf("error");
}

//释放内存
void Free(DblStack *k){
    ClearStack(k,0);
    ClearStack(k,1);
    free(k->V);
}
int main()
{
    DblStack stack;
    int m=200;
    InitDblStack(&stack,m);
    Push(&stack,1,"impact");
    Push(&stack,1,"genshin");
    Push(&stack,0,"impact");
    Push(&stack,0,"genshin");
    printf("栈0: ");
    while(!IsEmpty(&stack,0)){
        SElemType v;
        Pop(&stack,0,&v);
        printf("%s ",v);
    }
    printf("\n");
    printf("栈1: ");
    while(!IsEmpty(&stack,1)){
        SElemType v;
        Pop(&stack,1,&v);
        printf("%s ",v);
    }
    Free(&stack);
    return 0;
}