import pandas as pd
import numpy as np


def tran(url,title):
    data = pd.read_excel(url)
    data_copy = data[title].copy()
    print(data_copy)


def main():
    url = ""
    title = ""
    tran(url,title)


main
