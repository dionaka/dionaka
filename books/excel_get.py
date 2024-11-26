import csv
import pandas as pd
import numpy as np


def tran(url, title1, title2, finds):
    data = pd.read_excel(url)
    #print(data.columns.tolist())
    book_name = data[title1].copy()
    book_url = data[title2].copy()
    dic = {}
    for i in range(len(book_name)):
        #print(book_name[i])
        if finds in str(book_name[i]):
            dic[book_name[i]] = book_url[i]
    print(dic)


def main():
    url = r"C:\Users\hp\Desktop\books\zlibrary2300万本书籍资源下载汇聚.xlsx"
    title1 = "Unnamed: 1"
    title2 = "Unnamed: 2"
    name = "电"
    tran(url, title1, title2, name)


main()
