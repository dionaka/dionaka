#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAXSIZE 10000

typedef struct{
    int length;
    char *elem;
}sqList;

int InitList(sqList *b){
    b->elem = (char *)malloc(sizeof(char)*MAXSIZE);
    if(!(b->elem)){
        printf("内存分配失败\n");
        return 0;
        }
    b->length = 0;
    return 1;
}

void DestroyList(sqList *b){
    if(b == NULL) return;
    free(b->elem);
    b->elem = NULL;
    b->length = 0;
}

//顺序查找
int ElemLocate(sqList b,char e){
    for(int i=0;i<b.length;i++){
        if(b.elem[i]==e)
            return i+1;
    }        
    return 0; 
}

//赋值(sqList)
void Assignment(sqList *b,const char *e){
    strcpy(b->elem,e);
    b->length = strlen(e);
}

//插入元素(输入顺序表指针,插入位置(第几个而非索引),字符长度,字符)
void InsertList(sqList *b,int e,int c,const char *a){
    if(e >= 1 && e <= b->length+1 && c <= MAXSIZE - b->length && c == strlen(a)){
        for(int j = b->length+c-1;j>=e+c-1;j--){
            b->elem[j] = b->elem[j-c];
        }
        for(int i=0;i<c;i++){
            b->elem[e+i-1] = a[i];
        }
        b->length = strlen(b->elem);
    }
    else printf("Insert Error\n");
}

int main(){
    //创建顺序表
    sqList b;
    if(InitList(&b) == 0){
        printf("表初始化失败");
        return 1;
        }
    Assignment(&b,"diona");
    printf("%d\n",ElemLocate(b,'a'));    
    InsertList(&b,6,11," i love you");
    printf("%s\n",b.elem);
    DestroyList(&b);
    return 0;
}
//python和js打多了，以下是C语言一些总结
//1.单双引号要区分，""是字符串const char*类型，''是char类型
