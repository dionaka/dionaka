#include<stdio.h>

typedef struct Complex{
    float realpart;
    float imagepart;
} complex;

complex assign(float real,float image){
    complex c;
    c.realpart = real;
    c.imagepart = image;
    return c;
}

float getreal(complex c){
    return c.realpart;
}

float getimage(complex c){
    return c.imagepart;
}

//计算和
complex add(complex c1,complex c2){
    complex c;
    c.realpart = c1.realpart +c2.realpart;
    c.imagepart = c1.imagepart +c2.imagepart;
    return c;
}

//计算差
complex diff(complex c1,complex c2){
    complex c;
    c.realpart = c1.realpart -c2.realpart;
    c.imagepart = c1.imagepart -c2.imagepart;
    return c;
}

//%.2f指定两位小数
int main()
{    
    complex c1,c2,c3,c4;
    c1 = assign(1.1,3.25);
    c2 = assign(2.1,4.55);
    c3 = add(c1,c2);
    c4 = diff(c1,c2);
    printf("c1 = %.2f + %.2fi\n",getreal(c1),getimage(c1));
    printf("c2 = %.2f + %.2fi\n",getreal(c2),getimage(c2));
    printf("复数和为: %.2f + %.2fi\n",getreal(c3),getimage(c3));
    printf("复数差为: %.2f + %.2fi\n",getreal(c4),getimage(c4));
    return 0;
}