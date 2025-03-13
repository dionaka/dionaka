//哈希曼编码
#include<stdio.h>


//哈夫曼树结点结构
typedef struct HaffmanNode{
    char data;
    float freq;
    struct HaffmanNode *rightnode;
    struct HaffmanNode *leftnode;
}HaffmanNode;

//优先队列结点结构
typedef struct MinheapNode{
    HaffmanNode* haffmannode;
    struct MinheapNode* nextnode;
}MinheapNode;

//定义优先队列
typedef struct Minheap{
    MinheapNode* head;//头结点
}Minheap;

//创建哈夫曼结点
HaffmanNode* CreateHaffcharNode(char data,float freq){
    HaffmanNode* node = (HaffmanNode*)malloc(sizeof(HaffmanNode));
    node->data = data;
    node->freq = freq;
    node->leftnode = NULL;
    node->rightnode = NULL;
    return node;
};

//创建优先队列结点
MinheapNode* CreatMinheapNode(HaffmanNode* haffmanNode){
    MinheapNode* node = (MinheapNode*)malloc(sizeof(MinheapNode));
    node->haffmannode = haffmanNode;
    node->nextnode = NULL;
    return node;
};

//初始化优先队列
Minheap* CreateMinheap(){
    Minheap* heap = (Minheap*)malloc(sizeof(Minheap));
    heap->head = NULL;
    return heap;
}

//插入一个结点进入优先队列,频率从小到大
void insertMinheap(Minheap* minheap,HaffmanNode* haffmanNode){
    MinheapNode* node = CreatMinheapNode(haffmanNode);
    if(minheap->head == NULL || minheap->head->haffmannode->freq >= haffmanNode->freq){
        node->nextnode = minheap->head;
        minheap->head = node;
    }
    else{
        MinheapNode* current = minheap->head;
        while(current->nextnode != NULL && current->nextnode->haffmannode->freq < haffmanNode->freq){
            current = current->nextnode;
        }
        node->nextnode = current->nextnode;
        current->nextnode = node;
    }
}

//优先队列中取出频率最小结点
HaffmanNode* MinNode(Minheap* heap){
    if(heap->head == NULL) return 0;
    else{
        MinheapNode* temp = heap->head;
        HaffmanNode* node = temp->haffmannode;
        heap->head = heap->head->nextnode;
        free(temp);
        return node;
    }
}

//构造哈夫曼树
HaffmanNode* CreateHaffmanTree(char data[],float freq[],int size){
    Minheap* heap = CreateMinheap();
    //所有字符与频率插入优先队列
    for(int i=0;i<size;i++)
        insertMinheap(heap,CreateHaffcharNode(data[i],freq[i]));
    //构造哈夫曼树
    while(heap->head->nextnode){
        HaffmanNode* left = MinNode(heap);
        HaffmanNode* right = MinNode(heap);
        HaffmanNode* newnode = CreateHaffcharNode('\0',left->freq + right->freq);
        newnode->rightnode = right;
        newnode->leftnode = left;
        insertMinheap(heap,newnode);
    }    
    //返回哈夫曼树根结点
    return MinNode(heap);
};

//生成哈夫曼编码
//root:当前遍历哈夫曼树结点
//code:用于存储当前路径的字符数组。
//top:表示当前路径的深度（即编码的长度)。
//huffmanCode :存储最终哈夫曼编码的数组。
void CreateCodes(HaffmanNode* root,char* code,int top,char** huffmanCode){
    if(root->leftnode){
        code[top] = '0';
        CreateCodes(root->leftnode,code,top+1,huffmanCode);
    }
    if(root->rightnode){
        code[top] = '1';
        CreateCodes(root->rightnode,code,top+1,huffmanCode);
    }
    if(root->leftnode == NULL && root->rightnode == NULL){
        code[top] = '\0';
        huffmanCode[root->data] = strdup(code);
    }
}

//打印哈夫曼编码
void PrintCodes(char** huffmanCode,char data[],int size){
    for(int i = 0;i<size;i++){
        if(huffmanCode[data[i]] != NULL)
            printf("%c:%s\n",data[i],huffmanCode[data[i]]);
    }
}

int main()
{
    char data[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
    float freq[] = {8.19,1.47,3.83,3.91,12.25,2.26,1.71,4.57,7.10,0.14,0.41,3.77,3.34,7.06,7.26,2.89,0.99,6.85,6.36,9.41,2.58,1.09,1.59,0.21,1.58,0.08};
    int size = sizeof(data) / sizeof(data[0]);
    printf("%d\n",size);
    //构造哈夫曼树
    HaffmanNode* root = CreateHaffmanTree(data,freq,size);
    //哈夫曼编码
    char* huffmanCode[256] = {NULL};
    char code[100];
    CreateCodes(root,code,0,huffmanCode);
    PrintCodes(huffmanCode,data,size);
    return 0;
}