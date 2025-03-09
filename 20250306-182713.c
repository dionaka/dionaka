#include<stdio.h>
#include<stdlib.h>

typedef struct y{
    char data;
    struct y* next;//指针域
}Node,*LinkList;

int InitList(LinkList* l){
    *l = (LinkList)malloc(sizeof(Node));
    if(*l == NULL){
        printf("头结点创建失败\n");
        return 0;
    }
    (*l) -> next = NULL;
    return 1;
}

int IsEmpty(LinkList l){
    if(l->next) return 0;
    else return 1;
}

//销毁单链表
int DestroyList(LinkList *l){
    if(*l == NULL){
        printf("单链表不存在\n");
        return 0;
    }
    LinkList current = *l;
    LinkList next;
    while(current){
        next = current->next;
        free(current);
        current = next;
    }
    *l = NULL;
    return 1;
}

//清除单链表
int ClearList(LinkList l){
    if(l == NULL){
        printf("单链表不存在\n");
        return 0;
    }
    LinkList current =l->next;
    LinkList next;
    while(current){
        next = current->next;
        free(current);
        current = next;
    }
    l->next= NULL;
    return 1;
}

//单链表长度
int ListLength(LinkList l){
    int i=0;
    LinkList p = l->next;
    while(p){
        i+=1;
        p = p->next;
    }
    return i;
}

//单链表读取数据
int GetItem(LinkList l,int n,char *s){
    LinkList p = l->next;
    int i=1;
    while(p && i<n){
        i++;
        p=p->next;
    }
    if(!p || i>n) return 0;
    *s = p->data;
    return 1;
}

//单链表查找数据
int FindElem(LinkList l,char s){
    LinkList p =l->next;
    int i=1;
    while(p){
        if(p->data == s) return i;
        i++;
        p = p->next;
    }
    return 0;
}

//单链表插入数据
int InsertElem(LinkList l,int n,char s){
    int i = 1;
    while(l && i<n-1){
        l = l->next;
        i++;
    }
    if(!l) return 0;
    LinkList b = (LinkList)malloc(sizeof(Node));
    if(!b) return 0;
    b->data=s;
    b->next=l->next;
    l->next=b;
    return 1;
}

//删除节点数据:找n-1结点
int DeleteElem(LinkList l,int n){
    int i = 1;
    while(l && i<n-1){
        l = l->next;
        i++;
    }
    if(!l) return 0;
    LinkList q;
    q = l->next;
    l->next = q->next;
    free(q);
    return 1;
}

//头插法建立单链表
void CreateList_H(LinkList* l,int n){
    *l = (LinkList)malloc(sizeof(Node));//创建头结点
    (*l)->next = NULL;
    for(int i=1;i<=n;i++){
        LinkList p = (LinkList)malloc(sizeof(Node));
        printf("输入第%d项数据\n",i);
        scanf(" %c",&p->data);
        p->next = (*l)->next;
        (*l)->next = p;
    }
}

//尾插法建立单链表
void CreateList_R(LinkList* l,int n){
    *l = (LinkList)malloc(sizeof(Node));//创建头结点
    (*l)->next = NULL;
    LinkList r = *l;//☆尾指针指向头结点(记)
    for(int i=1;i<=n;i++){
        LinkList p = (LinkList)malloc(sizeof(Node));
        printf("输入第%d项数据\n",i);
        scanf(" %c",&p->data);
        p->next = NULL;
        r->next = p;
        r = p;
    }
}

int main()
{
    Node l;
    return 0;
}
//1.->优先级高于*,应用括号
//2.DestroyList :从头结点开始释放。clearlist:从头结点的nenext开始释放,保留头结点。