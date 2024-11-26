import selenium
import requests
import os


def get_name(num):
    names = {}
    count = 1606563775
    for i in range(1, num + 1):
        url = f"https://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={count}"
        response = requests.get(url)
        if response.status_code == 200:
            data_b = response.content
            data = data_b.decode("utf-8")
            data_core_eval = eval(data.split("(", 1)[1].rsplit(")", 1)[0])[str(count)]
            name = data_core_eval[-2]
            names[str(count)] = name
        else:
            print(f"Error: {response.status_code}")
            break
        count += 1
    print(names)
    names0 = [[x, y] for x, y in names.items()]
    names1 = [x for x in names.keys()]
    names2 = [x for x in names.values()]


def save_name(names, names0, names1, names2):
    os.mkdir("../names_folder")
    with open("../names_folder/names.txt", "w") as f:
        f.writelines(names)
        print("names:保存成功")
        f.close()
    with open("../names_folder/names0.txt", "w") as f:
        f.writelines(names0)
        print("names0:保存成功")
        f.close()
    with open("../names_folder/names1.txt", "w") as f:
        f.writelines(names1)
        print("names1:保存成功")
        f.close()
    with open("../names_folder/names2.txt", "w") as f:
        f.writelines(names2)
        print("names2:保存成功")
        f.close()
