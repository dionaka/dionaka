import pandas as pd
import numpy as np


def tran(url,title):
    data = pd.read_excel(url)
    data_copy = data[title].copy()
    print(data_copy)


def main():
    url = "https://docs.qq.com/sheet/DSHV2Uk9OQXdCSU91"
    title = "书名"
    tran(url,title)


main()