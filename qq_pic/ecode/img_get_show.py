import requests
import matplotlib.pyplot as plt
import cv2
from compare import *
from time import sleep

def get_img(num):
    qq_count = "1606563775"
    for i in range(1, num+1):
        src = f"https://q4.qlogo.cn/g?b=qq&nk={qq_count}&s=640"
        response = requests.get(src)
        if response.status_code == 200:
            with open(f'../img/qq({i}).jpg', 'wb') as f:
                f.write(response.content)
        qq_count = int(qq_count) + 1
        print(qq_count, "已保存")


def read_img(num):
    lines = int(num**0.5)
    rows = -(-num//lines)

    for i in range(1, num+1):
        img = cv2.imread(f'../img/qq({i}).jpg')
        # 注意：cv2读取的图片是BGR格式，需要转换为RGB格式才能在matplotlib中正确显示
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换成RGB格式
        plt.subplot(lines, rows, i)
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        #plt.title(f'qq({i}).jpg')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()


def main(num):
    sum=0
    for i in range(1,num+1):
        result=compare_pixel(img1_path="../img/qq(2).jpg", img2_path=f"../img/qq({i}).jpg")#1.47kb
        result1=compare_pixel(img1_path="../img/qq(8).jpg", img2_path=f"../img/qq({i}).jpg")#971b  
        result2=compare_pixel(img1_path="../img/qq(147).jpg", img2_path=f"../img/qq({i}).jpg")#1.58kb
        if result == 1 or result1 == 1 or result2 == 1:
            sum+=1    
    print(sum)
    sleep(20)


times = 1000
#get_img(times)
#read_img(times)
main(times)

