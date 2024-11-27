import json
import pandas as pd
import numpy as np
import pickle
import pprint


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
    #print(type(dic))


    ################################
    # dict to txt/csv file:
    ## way 1
    """
    data=pd.DataFrame(list(dic.items()), columns=["名称","链接"])
    data.to_csv("books.csv", index=False, encoding="utf-8")
    data.to_csv("books.txt", index=False, encoding="utf-8")
    """
    ## way 2
    
    with open("books.txt","w", encoding="utf-8", newline="") as file:
        for key, value in dic.items():
            file.write(f"{key}\t{value}\n")
    
    ## way 3
    """
    with open("books.txt","w",encoding="utf-8") as f:
        f.write(json.dumps(dic))
    """
    ## way 4
    """
    with open("books.txt", "wb") as f:
        pickle.dump(dic, f)

    with open("books.txt","rb") as f:
        pikle_data = pickle.load(f)
    print(type(pikle_data))
    """



def main():
    url = r"C:\Users\hp\Desktop\books\zlibrary2300万本书籍资源下载汇聚.xlsx"
    title1 = "Unnamed: 1"
    title2 = "Unnamed: 2"
    name = "电"
    tran(url, title1, title2, name)


main()
